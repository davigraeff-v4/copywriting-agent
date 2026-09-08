#!/usr/bin/env python3
"""Local, dependency-free editorial checks. Semantic review is supplied, not inferred."""
import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()


def normalize(text):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text).casefold()).strip()


def scan(fields, policy):
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
        if re.search(r"\[(?:h\b|confirmar|a confirmar|valor|dado|inserir)|\{\{", norm):
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
    sections = {f.get("section") for f in fields.values()}
    for o in collections["outline"].values():
        require(o["id"] in sections, f"outline {o['id']}: no fields")
        required = ("question", "new_information") + (("source_ids", "asset", "feasibility", "audience_value") if doc.get("route") == "social" else ())
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
    return errors


def review_template(doc):
    rubric = load(ROOT / "quality/rubric.json")
    return dict(delivery_sha256=digest(doc), rubric_version=rubric["version"],
                rubric_sha256=digest(rubric), policy_sha256=digest(load(ROOT / "quality/editorial-policy.json")), reviewer="",
                general={k: dict(score=None, field_id="", quote="", reason="") for k in rubric["general"]},
                humanization={k: dict(score=None, field_id="", quote="", reason="") for k in rubric["humanization"]},
                claim_checks={c["id"]: dict(status="pending", reason="") for c in doc["claims"]},
                constraint_checks={c["id"]: dict(status="pending", reason="") for c in doc["constraints"]},
                claim_inventory=dict(status="pending", reason=""),
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
    required = [("production", "knowledge/vicios-ia-humanizacao.md"), ("review", "knowledge/vicios-ia-humanizacao.md"), ("context", "knowledge/README.md"), ("context", "knowledge/metodologia-thamy.md"), ("context", f"knowledge/rotas/{doc['route']}.md")]
    for phase, path in required:
        sha = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        if not any(isinstance(r, dict) and r.get("phase") == phase and r.get("path") == path and r.get("sha256") == sha and r.get("read_at") for r in readings):
            errors.append(f"missing/current reading receipt: {phase}/{path}")
    return errors, scores


def _check(doc, review=None):
    errors = validate(doc)
    if errors:
        return dict(status="blocked", errors=errors, issues=[], sha256=digest(doc))
    issues = scan(doc["fields"], load(ROOT / "quality/editorial-policy.json"))
    mapped = {c["field_id"] for c in doc["claims"]}
    for field in doc["fields"]:
        if re.search(r"\d", field["text"]) and field["id"] not in mapped and field["role"] not in ("form_label",):
            issues.append(dict(field_id=field["id"], rule="unmapped_number", quote=field["text"], level="warning"))
    alltext = normalize("\n".join(f["text"] for f in doc["fields"]))
    for c in doc["constraints"]:
        for term in c.get("forbidden_terms", []):
            if re.search(r"(?<!\w)" + re.escape(normalize(term)) + r"(?!\w)", alltext):
                errors.append(f"constraint {c['id']}: forbidden {term}")
        for term in c.get("required_terms", []):
            if normalize(term) not in alltext:
                errors.append(f"constraint {c['id']}: missing {term}")
    errors += [f"{i['field_id']}: {i['rule']} ({i['quote']})" for i in issues if i["level"] == "error"]
    scores = {}
    if review is not None:
        review_errors, scores = check_review(doc, review, [i for i in issues if i["level"] == "warning"])
        errors += review_errors
    return dict(status="blocked" if errors else "ready_for_human_approval" if review is not None else "needs_editorial_review",
                sha256=digest(doc), errors=errors, issues=issues, scores=scores,
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
