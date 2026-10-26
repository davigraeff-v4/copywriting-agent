#!/usr/bin/env python3
"""Local, dependency-free editorial checks. Semantic review is supplied, not inferred."""
import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

from client_paths import resolve_reference

ROOT = Path(__file__).resolve().parents[1]
GATE_VERSION = '2026-10-09-objective-v1'
WORD_BUDGET_EXCLUSIONS = {'cta', 'form_label', 'form_option'}


def validator_digest():
    return digest({name: hashlib.sha256((ROOT / 'scripts' / name).read_bytes()).hexdigest()
                   for name in ('copycheck.py', 'client_paths.py')})


def word_count(doc):
    return sum(len(re.findall(r'\w+', f['text'], flags=re.UNICODE))
               for f in doc['fields'] if f['role'] not in WORD_BUDGET_EXCLUSIONS)


def constraint_fields(constraint, fields):
    """Machine selectors define scope; free-text scope never guesses a target."""
    selector = constraint.get('applies_to')
    if selector is None:
        if constraint.get('required_terms') or constraint.get('forbidden_terms'):
            scope = normalize(constraint['scope'])
            if scope not in {'global', 'cliente', 'client', 'campanha', 'campaign', 'entrega', 'delivery'}:
                raise ValueError('constraint ' + constraint['id'] + ': scoped terms need applies_to')
        return fields
    allowed = {'field_ids', 'sections', 'roles', 'piece_ids'}
    if not isinstance(selector, dict) or not selector or set(selector) - allowed:
        raise ValueError('constraint ' + constraint['id'] + ': invalid applies_to')
    keys = {'field_ids': 'id', 'sections': 'section', 'roles': 'role', 'piece_ids': 'piece_id'}
    for key, values in selector.items():
        if not isinstance(values, list) or not values or not all(isinstance(v, str) and v for v in values):
            raise ValueError('constraint ' + constraint['id'] + ': invalid selector ' + key)
        if not set(values) <= {f.get(keys[key]) for f in fields}:
            raise ValueError('constraint ' + constraint['id'] + ': unknown selector target ' + key)
    selected = [f for f in fields if all(f.get(keys[key]) in values for key, values in selector.items())]
    if not selected:
        raise ValueError('constraint ' + constraint['id'] + ': selector has no fields')
    return selected


def constraint_groups(constraint, fields):
    selected = constraint_fields(constraint, fields)
    selector = constraint.get('applies_to', {})
    if 'roles' in selector or 'field_ids' in selector:
        return [[normalize(f['text'])] for f in selected]
    key = 'piece_id' if 'piece_ids' in selector else 'section' if 'sections' in selector else None
    if key:
        return [[normalize(f['text']) for f in selected if f.get(key) == value]
                for value in dict.fromkeys(f[key] for f in selected)]
    return [[normalize(f['text']) for f in selected]]


def load(path):
    path = Path(path)
    if not path.is_file():
        path = resolve_reference(str(path), ROOT)
    return json.loads(path.read_text(encoding="utf-8"))


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()


def normalize(text):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text).casefold()).strip()


def placeholder_allowances(doc):
    """Exact human constraints may authorize product-template markers, never facts."""
    for name in ('fields', 'constraints', 'claims', 'facts'):
        if not isinstance(doc.get(name), list) or any(not isinstance(item, dict) for item in doc[name]):
            raise ValueError('placeholder allowances need valid delivery collections')
    fields = {field['id']: field for field in doc['fields']}
    allowed = {}
    for constraint in doc['constraints']:
        entries = constraint.get('placeholder_allowances')
        if entries is None:
            continue
        selector = constraint.get('applies_to')
        if (constraint.get('status') != 'active' or not isinstance(entries, list) or not entries
                or not isinstance(selector, dict) or set(selector) != {'field_ids'}):
            raise ValueError('placeholder allowance needs an active constraint with explicit field_ids')
        selected = {field['id'] for field in constraint_fields(constraint, doc['fields'])}
        covered = set()
        for entry in entries:
            if not isinstance(entry, dict) or set(entry) != {'field_id', 'token', 'purpose', 'direction_id'}:
                raise ValueError('invalid placeholder allowance')
            field_id, token = entry['field_id'], entry['token']
            if (entry['purpose'] != 'product_data_pending'
                    or not isinstance(entry['direction_id'], str) or not entry['direction_id']
                    or entry['direction_id'] != doc.get('context', {}).get('approved_direction_id')
                    or not isinstance(field_id, str) or field_id not in selected
                    or not isinstance(token, str) or not re.fullmatch(r'\[[A-ZÀ-ÖØ-Ý _,/()\-]{3,160}\]', token)
                    or token not in fields[field_id]['text']):
                raise ValueError('placeholder allowance must identify an exact pending product marker')
            if any(claim.get('field_id') == field_id for claim in doc['claims']):
                raise ValueError('a placeholder allowance cannot waive a factual claim')
            if any(token in fact.get('statement', '') for fact in doc['facts']):
                raise ValueError('a pending marker cannot serve as factual evidence')
            allowed.setdefault(field_id, set()).add(token)
            covered.add(field_id)
        if covered != selected:
            raise ValueError('placeholder allowance must cover exactly its selected fields')
    return allowed


def scan(fields, policy, allowed_placeholders=None):
    issues = []

    def issue(field, rule, quote, level="error"):
        issues.append(dict(field_id=field, rule=rule, quote=quote, level=level))

    for f in fields:
        text = f["text"]
        norm = normalize(text)
        for token in policy["forbidden_tokens"]:
            if re.search(r"(?<!\w)" + re.escape(token) + r"(?!\w)", norm):
                issue(f["id"], "abbreviation", token)
        for char in policy["forbidden_characters"]:
            if char in text:
                issue(f["id"], "dash", char)
        for phrase in policy["forbidden_phrases"]:
            if phrase in norm:
                issue(f["id"], "forbidden_phrase", phrase)
        # Detect the unwanted rhetorical construction, including sentence breaks.
        contrast = re.search(r"\bnão (?:é|são)\b[^.!?\n]{1,200}(?:[.,;:—–]\s*)(?:[EeÉé]\s+)?(?:é|são)\b", norm)
        if contrast:
            issue(f["id"], "false_contrast", contrast.group())
        contrast2 = re.search(r"\bmenos\b[^.!?]{1,100}[.!;]\s*mais\b", norm)
        if contrast2:
            issue(f["id"], "mechanical_contrast", contrast2.group(), "warning")
        pending = text
        for token in (allowed_placeholders or {}).get(f['id'], ()):
            pending = pending.replace(token, '')
        pending = normalize(pending)
        if re.search(r"\[(?:h\b|confirmar|a confirmar|valor|dado|inserir)|\{\{", pending):
            issue(f["id"], "placeholder", text)
        if f.get("max_chars") is not None and len(text) > f["max_chars"]:
            issue(f["id"], "length", str(len(text)))
        for phrase in policy["warning_phrases"]:
            if phrase in norm:
                issue(f["id"], "editorial_expression", phrase, "warning")
        run = 0
        for sentence in re.split(r"[.!?]+\s*", text):
            words = re.findall(r"\w+", sentence)
            run = run + 1 if 0 < len(words) <= policy["thresholds"]["short_sentence_words"] else 0
            if run == policy["thresholds"]["short_sentence_run"]:
                issue(f["id"], "telegraphic_sequence", text, "warning")
    # Compare fields within a piece/section; repeated CTA/form labels can be intentional.
    for i, a in enumerate(fields):
        if a["role"] in ("cta", "form_label"):
            continue
        for b in fields[i + 1:]:
            if b["role"] in ("cta", "form_label") or a["section"] != b["section"]:
                continue
            sa = set(re.findall(r"\w+", normalize(a["text"])))
            sb = set(re.findall(r"\w+", normalize(b["text"])))
            if min(len(sa), len(sb)) >= 4 and len(sa & sb) / len(sa | sb) >= policy["thresholds"]["similarity"]:
                issue(b["id"], "repeated_field", a["id"], "warning")
    return issues


def validate(doc):
    errors = []
    def require(ok, message):
        if not ok:
            errors.append(message)
    require(isinstance(doc, dict), "delivery must be an object")
    if not isinstance(doc, dict):
        return errors
    require(doc.get("schema_version") == 2, "schema_version must be 2")
    for key in ("client", "campaign", "version", "route"):
        require(isinstance(doc.get(key), str) and bool(doc[key].strip()), f"missing {key}")
    require(doc.get("route") in ("lp", "social", "ads", "direct"), "invalid route")
    context = doc.get("context", {})
    if not isinstance(context, dict):
        return errors + ["context must be an object"]
    for key in ("objective", "audience", "barrier", "value", "voice"):
        require(isinstance(context.get(key), str) and bool(context[key].strip()), f"missing context.{key}")
    require(isinstance(context.get("hypotheses"), list), "context.hypotheses must be a list")
    require(isinstance(context.get("constraints_confirmed"), bool) and context["constraints_confirmed"], "constraints must be confirmed")
    if doc.get("route") in ("lp", "ads"):
        require(bool(context.get("offer")), "commercial route needs offer")
    collections = {}
    for name in ("fields", "sources", "facts", "claims", "constraints", "outline"):
        entries = doc.get(name)
        require(isinstance(entries, list), f"{name} must be a list")
        if not isinstance(entries, list):
            entries = []
        ids = [v.get("id") for v in entries if isinstance(v, dict)]
        require(len(ids) == len(entries) and all(isinstance(v, str) and v for v in ids), f"{name}: each entry needs id")
        require(len(ids) == len(set(v for v in ids if isinstance(v, str))), f"{name}: duplicate ids")
        collections[name] = {v["id"]: v for v in entries if isinstance(v, dict) and isinstance(v.get("id"), str)}
    fields, sources, facts = (collections[n] for n in ("fields", "sources", "facts"))
    require(bool(fields), "no publishable fields")
    require(bool(sources), "no sources")
    for s in sources.values():
        require(all(isinstance(s.get(k), str) and s[k].strip() for k in ("locator", "excerpt")), f"source {s['id']}: locator/excerpt required")
    for f in facts.values():
        require(f.get("status") in ("confirmed", "hypothesis", "superseded"), f"fact {f['id']}: invalid status")
        require(isinstance(f.get("statement"), str) and bool(f["statement"].strip()), f"fact {f['id']}: no statement")
        refs = f.get("source_ids", [])
        require(isinstance(refs, list) and bool(refs) and all(isinstance(r, str) and r in sources for r in refs), f"fact {f['id']}: invalid source references")
    for f in fields.values():
        require(all(isinstance(f.get(k), str) and f[k].strip() for k in ("text", "section", "role")), f"field {f['id']}: text/section/role required")
        limit = f.get("max_chars")
        require(limit is None or (type(limit) is int and limit > 0), f"field {f['id']}: invalid max_chars")
    for c in collections["claims"].values():
        f = fields.get(c.get("field_id", ""), {})
        require(bool(c.get("quote")) and isinstance(c.get("quote"), str) and c["quote"] in f.get("text", ""), f"claim {c['id']}: quote not in field")
        refs = c.get("fact_ids", [])
        require(isinstance(refs, list) and bool(refs) and all(isinstance(r, str) and facts.get(r, {}).get("status") == "confirmed" for r in refs), f"claim {c['id']}: needs confirmed facts")
        require(bool(c.get("limit")), f"claim {c['id']}: state scope/limit")
    for c in collections["constraints"].values():
        require(all(isinstance(c.get(k), str) and c[k].strip() for k in ("rule", "scope", "source")), f"constraint {c['id']}: rule/scope/source required")
        for key in ("forbidden_terms", "required_terms"):
            require(isinstance(c.get(key, []), list) and all(isinstance(v, str) and v for v in c.get(key, [])), f"constraint {c['id']}: invalid {key}")
        if all(isinstance(c.get(k), str) and c[k].strip() for k in ('rule', 'scope', 'source')):
            try:
                constraint_fields(c, list(fields.values()))
            except ValueError as exc:
                errors.append(str(exc))
    sections = {f.get("section") for f in fields.values()}
    try:
        placeholder_allowances(doc)
    except (ValueError, TypeError, KeyError) as exc:
        errors.append(str(exc))
    if doc.get("route") == "lp":
        insight_keys = {
            "current_situation", "trigger", "desired_outcome", "alternative",
            "barrier", "decision_criteria", "observed_language",
        }
        insights = context.get("buyer_insights")
        require(isinstance(insights, dict) and set(insights) == insight_keys, "lp context.buyer_insights incomplete")
        if isinstance(insights, dict) and set(insights) == insight_keys:
            useful = 0
            for key, value in insights.items():
                ok = isinstance(value, dict) and value.get("status") in ("confirmed", "inferred", "missing")
                ok = ok and isinstance(value.get("text"), str) and bool(value["text"].strip())
                refs = value.get("source_ids", []) if isinstance(value, dict) else []
                ok = ok and isinstance(refs, list) and all(isinstance(ref, str) and ref in sources for ref in refs)
                require(ok, f"lp buyer_insights.{key} invalid")
                if ok and value["status"] != "missing":
                    useful += 1
            require(useful >= 4, "lp needs at least four usable buyer insights")
        require(isinstance(context.get("narrative_thesis"), str) and bool(context["narrative_thesis"].strip()), "lp context.narrative_thesis required")
        headline_ids = []
        seen_sections = set()
        for field in doc.get("fields", []):
            if field.get("section") not in seen_sections:
                section_headlines = [f["id"] for f in doc.get("fields", []) if f.get("section") == field.get("section") and f.get("role") == "headline"]
                require(len(section_headlines) == 1, f"lp section {field.get('section')}: exactly one headline required")
                if len(section_headlines) == 1:
                    headline_ids.append(section_headlines[0])
                seen_sections.add(field.get("section"))
        require(context.get("title_ladder") == headline_ids, "lp context.title_ladder must match headline ids in section order")
    for o in collections["outline"].values():
        require(o["id"] in sections, f"outline {o['id']}: no fields")
        route_fields = ()
        if doc.get("route") == "social":
            route_fields = ("source_ids", "asset", "feasibility", "audience_value")
        elif doc.get("route") == "lp":
            route_fields = ("function", "evidence", "transition", "action")
        required = ("question", "new_information") + route_fields
        require(all(bool(o.get(k)) for k in required), f"outline {o['id']}: incomplete function/value/production")
        if doc.get("route") == "social":
            refs = o.get("source_ids", [])
            require(isinstance(refs, list) and all(isinstance(r, str) and r in sources for r in refs), f"outline {o['id']}: invalid sources")
    if doc.get("route") in ("lp", "social"):
        require(sections == set(collections["outline"]), "every section/post needs an outline entry")
    requirements = doc.get("requirements", {})
    require(isinstance(requirements, dict), "requirements must be an object")
    if isinstance(requirements, dict):
        if "sections" in requirements:
            require(type(requirements["sections"]) is int and len(sections) == requirements["sections"], "section count differs from briefing")
        for section, labels in requirements.get("forms", {}).items():
            actual = [f.get("text") for f in fields.values() if f.get("section") == section and f.get("role") == "form_label"]
            require(actual == labels, f"form {section}: labels/order differ from briefing")
        if doc.get("route") == "lp":
            budget = requirements.get("prose_word_budget", 300)
            require(type(budget) is int and budget > 0, "lp prose_word_budget must be a positive integer")
            if type(budget) is int and budget > 300:
                require(isinstance(requirements.get("prose_word_budget_reason"), str) and bool(requirements["prose_word_budget_reason"].strip()), "lp prose_word_budget above 300 needs a reason")
            if type(budget) is int and budget > 0:
                actual_words = word_count(doc)
                require(actual_words <= budget, f"lp prose exceeds word budget: {actual_words}/{budget}")
    return errors


def review_template(doc):
    rubric = load(ROOT / "quality/rubric.json")
    return dict(delivery_sha256=digest(doc), gate_version=GATE_VERSION, validator_sha256=validator_digest(), rubric_version=rubric["version"],
                rubric_sha256=digest(rubric), policy_sha256=digest(load(ROOT / "quality/editorial-policy.json")), reviewer="",
                general={k: dict(score=None, field_id="", quote="", reason="") for k in rubric["general"]},
                humanization={k: dict(score=None, field_id="", quote="", reason="") for k in rubric["humanization"]},
                claim_checks={c["id"]: dict(status="pending", reason="") for c in doc["claims"]},
                constraint_checks={c["id"]: dict(status="pending", reason="") for c in doc["constraints"]},
                claim_inventory=dict(status="pending", reason=""),
                field_checks={f['id']: dict(status='pending', claim_ids=[], reason='') for f in doc['fields']},
                source_checks={s['id']: dict(status='pending', path='', sha256='', reason='') for s in doc['sources']},
                readings=[], warning_resolutions=[], limitations=[], critical_issues=[])


def check_review(doc, review, warnings):
    errors, scores = [], {}
    rubric = load(ROOT / "quality/rubric.json")
    if review.get("delivery_sha256") != digest(doc):
        errors.append("stale review: delivery/context changed")
    if review.get("rubric_version") != rubric["version"]:
        errors.append("rubric version mismatch")
    if not isinstance(review.get("reviewer"), str) or not review["reviewer"].strip():
        errors.append("missing reviewer")
    if review.get("rubric_sha256") != digest(rubric):
        errors.append("rubric changed: renew review")
    if review.get("policy_sha256") != digest(load(ROOT / "quality/editorial-policy.json")):
        errors.append("editorial policy changed: renew review")
    fields = {f["id"]: f for f in doc["fields"]}
    if review.get('gate_version') != GATE_VERSION or review.get('validator_sha256') != validator_digest():
        errors.append('objective validator changed or legacy review: renew validation')
    field_checks = review.get('field_checks', {})
    claims = {c['id']: c for c in doc['claims']}
    if not isinstance(field_checks, dict) or set(field_checks) != set(fields):
        errors.append('field_checks: inventory must cover every public field')
    else:
        for field_id, item in field_checks.items():
            if not isinstance(item, dict) or not isinstance(item.get('reason'), str) or not item['reason'].strip():
                errors.append('field_checks.' + field_id + ': missing factual decision/reason')
                continue
            linked = {c['id'] for c in doc['claims'] if c['field_id'] == field_id}
            refs = item.get('claim_ids')
            if not isinstance(refs, list) or not all(isinstance(x, str) for x in refs) or len(set(refs)) != len(refs):
                errors.append('field_checks.' + field_id + ': invalid claim_ids')
            elif item.get('status') == 'mapped':
                if not refs or set(refs) != linked or any(x not in claims for x in refs):
                    errors.append('field_checks.' + field_id + ': claims do not cover mapped field')
            elif item.get('status') == 'no_factual_claim':
                if refs or linked:
                    errors.append('field_checks.' + field_id + ': factual claims cannot be waived')
            else:
                errors.append('field_checks.' + field_id + ': unresolved factual decision')
    sources = {s['id']: s for s in doc['sources']}
    source_checks = review.get('source_checks', {})
    if not isinstance(source_checks, dict) or set(source_checks) != set(sources):
        errors.append('source_checks: each source needs a preserved file or snapshot')
    else:
        for source_id, item in source_checks.items():
            try:
                if not isinstance(item, dict) or item.get('status') != 'pass' or not isinstance(item.get('reason'), str) or not item['reason'].strip():
                    raise ValueError('unresolved source check')
                path = resolve_reference(item.get('path'), ROOT)
                raw = path.read_bytes()
                if item.get('sha256') != hashlib.sha256(raw).hexdigest():
                    raise ValueError('source changed: renew source check')
                if normalize(sources[source_id]['excerpt']) not in normalize(raw.decode('utf-8')):
                    raise ValueError('source excerpt not present in preserved text')
            except (OSError, ValueError, TypeError, UnicodeError) as exc:
                errors.append('source_checks.' + source_id + ': ' + str(exc))
    for group in ("general", "humanization"):
        entries = review.get(group, {})
        if not isinstance(entries, dict) or set(entries) != set(rubric[group]):
            errors.append(f"{group}: incomplete criteria")
            continue
        numbers = []
        for key, item in entries.items():
            if not isinstance(item, dict):
                errors.append(f"{group}.{key}: invalid review entry")
                continue
            score = item.get("score")
            valid = type(score) is int and 0 <= score <= 10 and (group != "humanization" or score in (0, 5, 10))
            if not valid:
                errors.append(f"{group}.{key}: invalid score")
            else:
                numbers.append(score)
                if group == "general" and key in rubric["critical"] and score < rubric["minimum"]:
                    errors.append(f"critical criterion failed: {key}")
            quote = item.get("quote")
            if not isinstance(quote, str) or not quote or quote not in fields.get(item.get("field_id"), {}).get("text", "") or not item.get("reason"):
                errors.append(f"{group}.{key}: missing exact text evidence/reason")
        if len(numbers) == len(rubric[group]):
            scores[group] = round(sum(numbers) / len(numbers), 3)
            if scores[group] < rubric["minimum"]:
                errors.append(f"{group}: below minimum")
    for group, items in (("claim_checks", doc["claims"]), ("constraint_checks", doc["constraints"])):
        checks = review.get(group, {})
        if not isinstance(checks, dict) or set(checks) != {i["id"] for i in items}:
            errors.append(f"{group}: incomplete checks")
            continue
        if any(not isinstance(v, dict) or v.get("status") != "pass" or not v.get("reason") for v in checks.values()):
            errors.append(f"{group}: unresolved check")
    inventory = review.get("claim_inventory", {})
    if not isinstance(inventory, dict) or inventory.get("status") != "pass" or not inventory.get("reason"):
        errors.append("claim inventory not reviewed (includes non-numeric assertions)")
    if review.get("critical_issues") != []:
        errors.append("critical issues missing or unresolved")
    resolutions = review.get("warning_resolutions", [])
    for w in warnings:
        if not any(isinstance(r, dict) and r.get("field_id") == w["field_id"] and r.get("rule") == w["rule"] and r.get("reason") for r in resolutions):
            errors.append(f"unresolved warning: {w['field_id']}/{w['rule']}")
    readings = review.get("readings", [])
    required = [
        ("production", "knowledge/vicios-ia-humanizacao.md", True),
        ("review", "knowledge/vicios-ia-humanizacao.md", True),
        # README is a routing index. Editorial additions to its catalog must not
        # invalidate an otherwise current campaign review.
        ("context", "knowledge/README.md", False),
        ("context", "knowledge/metodologia-thamy.md", True),
        ("context", f"knowledge/rotas/{doc['route']}.md", True),
    ]
    if doc.get("route") == "lp":
        required.append(("context", "knowledge/narrativa-lp.md", True))
    for phase, path, strict_hash in required:
        sha = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        if not any(
            isinstance(r, dict)
            and r.get("phase") == phase
            and r.get("path") == path
            and (not strict_hash or r.get("sha256") == sha)
            and r.get("read_at")
            for r in readings
        ):
            errors.append(f"missing/current reading receipt: {phase}/{path}")
    return errors, scores


def _check(doc, review=None):
    errors = validate(doc)
    if errors:
        return dict(status="blocked", errors=errors, issues=[], sha256=digest(doc))
    issues = scan(doc["fields"], load(ROOT / "quality/editorial-policy.json"), placeholder_allowances(doc))
    mapped = {c["field_id"] for c in doc["claims"]}
    for field in doc["fields"]:
        if re.search(r"\d", field["text"]) and field["id"] not in mapped and field["role"] not in ("form_label",):
            issues.append(dict(field_id=field["id"], rule="unmapped_number", quote=field["text"], level="warning"))
    for c in doc["constraints"]:
        selected = constraint_fields(c, doc['fields'])
        texts = [normalize(f['text']) for f in selected]
        for term in c.get("forbidden_terms", []):
            if any(re.search(r"(?<!\w)" + re.escape(normalize(term)) + r"(?!\w)", text) for text in texts):
                errors.append(f"constraint {c['id']}: forbidden {term}")
        for term in c.get("required_terms", []):
            groups = constraint_groups(c, doc['fields'])
            pattern = r'(?<!\w)' + re.escape(normalize(term)) + r'(?!\w)'
            if any(not any(re.search(pattern, text) for text in group) for group in groups):
                errors.append(f"constraint {c['id']}: missing {term}")
    errors += [f"{i['field_id']}: {i['rule']} ({i['quote']})" for i in issues if i["level"] == "error"]
    scores = {}
    if review is not None:
        review_errors, scores = check_review(doc, review, [i for i in issues if i["level"] == "warning"])
        errors += review_errors
    return dict(status="blocked" if errors else "ready_for_human_approval" if review is not None else "needs_editorial_review",
                sha256=digest(doc), errors=errors, issues=issues, scores=scores,
                word_count=word_count(doc), gate_version=GATE_VERSION,
                limitation="Checks verify structure and review evidence, not factual truth, grammar completeness or human preference.")


def check(doc, review=None):
    """Malformed inputs fail closed with a report, including nested invalid types."""
    try:
        return _check(doc, review)
    except (ValueError, TypeError, KeyError, AttributeError, OSError) as exc:
        return dict(status="blocked", errors=[f"invalid input: {exc}"], issues=[])


def render(doc):
    lines = [f"# {doc['client']} | {doc['campaign']} | {doc['version']}", ""]
    previous = None
    for f in doc["fields"]:
        if f["section"] != previous:
            lines += [f"## {f['section']}", ""]
            previous = f["section"]
        lines += [f"**{f['role']}:** {f['text']}", ""]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("delivery")
    p.add_argument("--review")
    p.add_argument("--review-template", action="store_true")
    p.add_argument("--render", type=Path, help="Write exact copy only when every gate passes; never overwrite")
    a = p.parse_args()
    try:
        doc = load(a.delivery)
        if a.review_template:
            errors = validate(doc)
            if errors:
                raise ValueError("; ".join(errors))
            result = review_template(doc)
        else:
            result = check(doc, load(a.review) if a.review else None)
            if a.render:
                if result["status"] != "ready_for_human_approval":
                    result["errors"].append("render requires valid current review")
                    result["status"] = "blocked"
                else:
                    with a.render.open("x", encoding="utf-8") as out:
                        out.write(render(doc))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result.get("status") == "blocked" else 0
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as e:
        print(json.dumps(dict(status="blocked", errors=[str(e)]), ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())
