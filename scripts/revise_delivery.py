#!/usr/bin/env python3
"""Create a small, reviewable revision from an already validated delivery."""
import argparse
import copy
import json
from pathlib import Path

from copycheck import check, digest, load


GENERAL_BY_ROLE = {
    "headline": {"objetivo", "barreira", "especificidade", "relevancia", "voz", "formato", "coerencia"},
    "title": {"objetivo", "barreira", "especificidade", "relevancia", "voz", "formato", "coerencia"},
    "support": {"especificidade", "progressao", "evidencia", "mecanismo", "voz", "formato", "coerencia", "utilidade"},
    "primary_text": {"objetivo", "barreira", "especificidade", "progressao", "relevancia", "evidencia", "mecanismo", "voz", "acao", "coerencia", "utilidade"},
    "cta": {"objetivo", "formato", "acao", "coerencia"},
}
DEFAULT_GENERAL = {"especificidade", "progressao", "evidencia", "mecanismo", "formato", "coerencia", "utilidade"}
ALL_HUMAN = {"portugues", "sintaxe", "registro", "ritmo", "redundancia", "entrada", "vocabulario", "naturalidade"}
SCOPE_GENERAL = {"progressao", "formato", "coerencia", "utilidade"}
SCOPE_HUMAN = {"redundancia"}


def fail(message):
    raise ValueError(message)


def pending_entry():
    return {"score": None, "field_id": "", "quote": "", "reason": ""}


def inspect_delivery(doc):
    sections = []
    for field in doc.get("fields", []):
        if field.get("section") not in sections:
            sections.append(field.get("section"))
    return {
        "client": doc.get("client"),
        "campaign": doc.get("campaign"),
        "version": doc.get("version"),
        "route": doc.get("route"),
        "sections": [
            {
                "id": section,
                "fields": [
                    {"id": f["id"], "role": f["role"]}
                    for f in doc.get("fields", []) if f.get("section") == section
                ],
            }
            for section in sections
        ],
    }


def prepare(parent, parent_review, change):
    parent_result = check(parent, parent_review)
    if parent_result.get("status") != "ready_for_human_approval":
        fail("parent delivery needs a current valid review")
    if not isinstance(change, dict):
        fail("change must be an object")
    allowed = {"kind", "version", "campaign", "instruction", "remove_sections",
               "remove_field_ids", "replace_fields", "claim_updates"}
    unknown = set(change) - allowed
    if unknown:
        fail("unsupported change keys: " + ", ".join(sorted(unknown)))
    kind = change.get("kind")
    if kind not in ("scope", "field"):
        fail("kind must be scope or field")
    if not isinstance(change.get("version"), str) or not change["version"].strip():
        fail("version is required")
    if not isinstance(change.get("instruction"), str) or not change["instruction"].strip():
        fail("instruction is required")
    remove_sections = set(change.get("remove_sections", []))
    remove_fields = set(change.get("remove_field_ids", []))
    replacements = change.get("replace_fields", {})
    claim_updates = change.get("claim_updates", {})
    if not all(isinstance(v, str) and v for v in remove_sections | remove_fields):
        fail("removed section and field ids must be non-empty strings")
    if not isinstance(replacements, dict) or not all(isinstance(k, str) and isinstance(v, str) and v.strip() for k, v in replacements.items()):
        fail("replace_fields must map field ids to non-empty text")
    if not isinstance(claim_updates, dict):
        fail("claim_updates must be an object")
    if kind == "scope" and (replacements or claim_updates):
        fail("scope revisions cannot change text or claims")
    if kind == "field" and (remove_sections or remove_fields):
        fail("field revisions cannot remove scope")
    if not (remove_sections or remove_fields or replacements):
        fail("revision contains no change")

    old_fields = {f["id"]: f for f in parent["fields"]}
    old_sections = {f["section"] for f in parent["fields"]}
    if not remove_sections <= old_sections:
        fail("unknown sections: " + ", ".join(sorted(remove_sections - old_sections)))
    if not remove_fields <= set(old_fields):
        fail("unknown fields: " + ", ".join(sorted(remove_fields - set(old_fields))))
    if not set(replacements) <= set(old_fields):
        fail("unknown replacement fields: " + ", ".join(sorted(set(replacements) - set(old_fields))))

    doc = copy.deepcopy(parent)
    doc["version"] = change["version"]
    if "campaign" in change:
        if not isinstance(change["campaign"], str) or not change["campaign"].strip():
            fail("campaign must be non-empty")
        doc["campaign"] = change["campaign"]
    removed_ids = {
        f["id"] for f in doc["fields"]
        if f["section"] in remove_sections or f["id"] in remove_fields
    }
    doc["fields"] = [f for f in doc["fields"] if f["id"] not in removed_ids]
    if not doc["fields"]:
        fail("revision cannot remove every publishable field")
    changed_ids = set(replacements)
    if isinstance(doc.get("context", {}).get("title_ladder"), list):
        doc["context"]["title_ladder"] = [field_id for field_id in doc["context"]["title_ladder"] if field_id not in removed_ids]
    for field in doc["fields"]:
        if field["id"] in replacements:
            field["text"] = replacements[field["id"]]

    doc["claims"] = [c for c in doc["claims"] if c.get("field_id") not in removed_ids]
    claims = {c["id"]: c for c in doc["claims"]}
    if not set(claim_updates) <= set(claims):
        fail("claim_updates can only modify existing claims")
    for claim_id, update in claim_updates.items():
        if not isinstance(update, dict) or not set(update) <= {"quote", "fact_ids", "limit"}:
            fail("invalid claim update: " + claim_id)
        claims[claim_id].update(copy.deepcopy(update))

    remaining_sections = {f["section"] for f in doc["fields"]}
    doc["outline"] = [o for o in doc["outline"] if o["id"] in remaining_sections]
    requirements = doc.get("requirements", {})
    if isinstance(requirements, dict):
        if "sections" in requirements:
            requirements["sections"] = len(remaining_sections)
        if isinstance(requirements.get("forms"), dict):
            requirements["forms"] = {k: v for k, v in requirements["forms"].items() if k in remaining_sections}
    doc["revision"] = {
        "parent_delivery_sha256": digest(parent),
        "parent_review_sha256": digest(parent_review),
        "kind": kind,
        "instruction": change["instruction"],
        "removed_sections": sorted(remove_sections),
        "removed_field_ids": sorted(removed_ids),
        "changed_field_ids": sorted(changed_ids),
        "context_reused": True,
    }

    draft_result = check(doc)
    if draft_result.get("status") == "blocked":
        fail("revised delivery is invalid: " + "; ".join(draft_result.get("errors", [])))

    review = copy.deepcopy(parent_review)
    review["delivery_sha256"] = digest(doc)
    review["revision"] = copy.deepcopy(doc["revision"])
    review["claim_checks"] = {
        k: v for k, v in review.get("claim_checks", {}).items() if k in claims
    }
    pending_general = set()
    pending_human = set()
    if kind == "scope":
        pending_general |= SCOPE_GENERAL
        pending_human |= SCOPE_HUMAN
    else:
        roles = {old_fields[field_id].get("role") for field_id in changed_ids}
        for role in roles:
            pending_general |= GENERAL_BY_ROLE.get(role, DEFAULT_GENERAL)
        pending_human |= ALL_HUMAN
    for group, pending in (("general", pending_general), ("humanization", pending_human)):
        for key, item in review.get(group, {}).items():
            if item.get("field_id") in removed_ids or item.get("field_id") in changed_ids:
                pending.add(key)
        for key in pending:
            review[group][key] = pending_entry()

    changed_claims = {c["id"] for c in doc["claims"] if c.get("field_id") in changed_ids}
    for claim_id in changed_claims:
        review["claim_checks"][claim_id] = {"status": "pending", "reason": ""}
    if kind == "field":
        review["constraint_checks"] = {
            c["id"]: {"status": "pending", "reason": ""} for c in doc["constraints"]
        }
        review["claim_inventory"] = {"status": "pending", "reason": ""}
    else:
        review["claim_inventory"] = {
            "status": "pass",
            "reason": "A revisão removeu campos sem alterar o conteúdo preservado; a remoção não introduz novos claims.",
        }

    existing_resolutions = {
        (r.get("field_id"), r.get("rule"))
        for r in review.get("warning_resolutions", []) if isinstance(r, dict)
    }
    new_warnings = [
        {"field_id": issue["field_id"], "rule": issue["rule"], "quote": issue["quote"], "reason": ""}
        for issue in draft_result.get("issues", [])
        if issue.get("level") == "warning"
        and (issue.get("field_id"), issue.get("rule")) not in existing_resolutions
    ]
    delta = {
        "reviewer": "",
        "general": {k: pending_entry() for k in sorted(pending_general)},
        "humanization": {k: pending_entry() for k in sorted(pending_human)},
        "claim_checks": {k: {"status": "pending", "reason": ""} for k in sorted(changed_claims)},
        "constraint_checks": copy.deepcopy(review["constraint_checks"]) if kind == "field" else {},
        "claim_inventory": copy.deepcopy(review["claim_inventory"]) if kind == "field" else {},
        "warning_resolutions": new_warnings,
        "limitations": [],
    }
    summary = {
        "kind": kind,
        "removed_sections": sorted(remove_sections),
        "removed_fields": len(removed_ids),
        "changed_fields": sorted(changed_ids),
        "preserved_fields": len(doc["fields"]),
        "pending_general": sorted(pending_general),
        "pending_humanization": sorted(pending_human),
        "pending_claim_checks": sorted(changed_claims),
        "pending_warnings": len(new_warnings),
        "research_reused": True,
    }
    return doc, review, delta, summary


def merge_review(pending, delta):
    review = copy.deepcopy(pending)
    if not isinstance(delta.get("reviewer"), str) or not delta["reviewer"].strip():
        fail("delta reviewer is required")
    for group in ("general", "humanization", "claim_checks", "constraint_checks"):
        supplied = delta.get(group, {})
        if not isinstance(supplied, dict):
            fail(group + " delta must be an object")
        if group in ("general", "humanization"):
            expected = {
                key for key, value in review.get(group, {}).items()
                if isinstance(value, dict) and value.get("score") is None
            }
        else:
            expected = {
                key for key, value in review.get(group, {}).items()
                if isinstance(value, dict) and value.get("status") == "pending"
            }
        if set(supplied) != expected:
            fail(group + " delta keys differ from pending review")
        for key, value in supplied.items():
            review[group][key] = value
    inventory = review.get("claim_inventory", {})
    if isinstance(inventory, dict) and inventory.get("status") == "pending":
        supplied = delta.get("claim_inventory")
        if not isinstance(supplied, dict) or supplied.get("status") == "pending":
            fail("claim_inventory delta is incomplete")
        review["claim_inventory"] = supplied
    review["warning_resolutions"] = review.get("warning_resolutions", []) + delta.get("warning_resolutions", [])
    review["limitations"] = review.get("limitations", []) + delta.get("limitations", [])
    return review


def write_new(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    inspect_cmd = sub.add_parser("inspect")
    inspect_cmd.add_argument("delivery")
    prepare_cmd = sub.add_parser("prepare")
    prepare_cmd.add_argument("parent_delivery")
    prepare_cmd.add_argument("parent_review")
    prepare_cmd.add_argument("change")
    prepare_cmd.add_argument("out_dir", type=Path)
    merge_cmd = sub.add_parser("merge")
    merge_cmd.add_argument("pending_review")
    merge_cmd.add_argument("delta")
    merge_cmd.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "inspect":
            result = inspect_delivery(load(args.delivery))
        elif args.command == "prepare":
            out = args.out_dir
            if out.exists():
                fail("output directory already exists")
            doc, review, delta, result = prepare(load(args.parent_delivery), load(args.parent_review), load(args.change))
            out.mkdir(parents=True)
            write_new(out / "delivery.json", doc)
            write_new(out / "review.pending.json", review)
            write_new(out / "review-delta.json", delta)
            readings = review.get("readings", [])
            write_new(out / "readings.json", readings)
        else:
            result = merge_review(load(args.pending_review), load(args.delta))
            write_new(args.output, result)
            result = {"status": "merged", "output": str(args.output)}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        print(json.dumps({"status": "blocked", "errors": [str(exc)]}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
