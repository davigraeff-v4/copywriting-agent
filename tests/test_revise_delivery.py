import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import copycheck
import revise_delivery


def valid_review(doc):
    review = copycheck.review_template(doc)
    review["reviewer"] = "Synthetic test reviewer"
    field = doc["fields"][0]
    for group in ("general", "humanization"):
        for key in review[group]:
            review[group][key] = {
                "score": 10,
                "field_id": field["id"],
                "quote": field["text"],
                "reason": "Synthetic review fixture",
            }
    for group in ("claim_checks", "constraint_checks"):
        for key in review[group]:
            review[group][key] = {"status": "pass", "reason": "Synthetic review fixture"}
    review["claim_inventory"] = {"status": "pass", "reason": "Synthetic review fixture"}
    required = [
        ("context", "knowledge/README.md"),
        ("context", "knowledge/metodologia-thamy.md"),
        ("context", f"knowledge/rotas/{doc['route']}.md"),
        ("production", "knowledge/vicios-ia-humanizacao.md"),
        ("review", "knowledge/vicios-ia-humanizacao.md"),
    ]
    if doc["route"] == "lp":
        required.append(("context", "knowledge/narrativa-lp.md"))
    review["readings"] = [
        {
            "phase": phase,
            "path": path,
            "sha256": hashlib.sha256((ROOT / path).read_bytes()).hexdigest(),
            "read_at": "synthetic-test-receipt",
        }
        for phase, path in required
    ]
    return review


def fill_delta(delta, doc):
    result = copy.deepcopy(delta)
    result["reviewer"] = "Synthetic incremental reviewer"
    field = doc["fields"][0]
    for group in ("general", "humanization"):
        for key in result[group]:
            result[group][key] = {
                "score": 10,
                "field_id": field["id"],
                "quote": field["text"],
                "reason": "Synthetic incremental check",
            }
    for group in ("claim_checks", "constraint_checks"):
        for key in result[group]:
            result[group][key] = {"status": "pass", "reason": "Synthetic incremental check"}
    if result.get("claim_inventory"):
        result["claim_inventory"] = {"status": "pass", "reason": "Synthetic incremental check"}
    for warning in result["warning_resolutions"]:
        warning["reason"] = "Synthetic warning resolution"
    return result


class IncrementalRevision(unittest.TestCase):
    def setUp(self):
        self.doc = copycheck.load(ROOT / "tests/fixtures/valid-delivery.json")
        extra = {
            "id": "story_headline",
            "section": "story-1",
            "role": "headline",
            "text": "Consulte o catálogo disponível",
        }
        self.doc["fields"].append(extra)
        self.doc["context"]["title_ladder"].append("story_headline")
        self.doc["outline"].append({
            "id": "story-1",
            "question": "Como consultar?",
            "new_information": "Apresenta a consulta ao catálogo.",
            "function": "Reforçar a consulta em outro formato.",
            "evidence": "O catálogo está disponível para solicitação.",
            "transition": "Conclui a sequência de teste.",
            "action": "Solicitar catálogo.",
        })
        self.doc["requirements"]["sections"] = 2
        self.review = valid_review(self.doc)
        self.assertEqual(copycheck.check(self.doc, self.review)["status"], "ready_for_human_approval")

    def test_scope_removal_preserves_every_remaining_field(self):
        change = {
            "kind": "scope",
            "version": "v2",
            "instruction": "Somente Feed; remover Story",
            "remove_sections": ["story-1"],
        }
        revised, pending, delta, summary = revise_delivery.prepare(self.doc, self.review, change)
        self.assertEqual(revised["fields"], self.doc["fields"][:-1])
        expected_context = copy.deepcopy(self.doc["context"])
        expected_context["title_ladder"] = ["hero"]
        self.assertEqual(revised["context"], expected_context)
        self.assertEqual(revised["requirements"]["sections"], 1)
        self.assertEqual(summary["removed_fields"], 1)
        self.assertEqual(set(delta["general"]), revise_delivery.SCOPE_GENERAL)
        self.assertEqual(set(delta["humanization"]), revise_delivery.SCOPE_HUMAN)
        merged = revise_delivery.merge_review(pending, fill_delta(delta, revised))
        self.assertEqual(copycheck.check(revised, merged)["status"], "ready_for_human_approval")

    def test_localized_headline_preserves_other_fields_and_reuses_context(self):
        original_other_fields = copy.deepcopy(self.doc["fields"][1:])
        change = {
            "kind": "field",
            "version": "v2",
            "instruction": "Ajuste somente a headline da primeira peça",
            "replace_fields": {self.doc["fields"][0]["id"]: "Consulte peças pelo catálogo"},
        }
        revised, pending, delta, summary = revise_delivery.prepare(self.doc, self.review, change)
        self.assertEqual(revised["fields"][1:], original_other_fields)
        self.assertEqual(revised["context"], self.doc["context"])
        self.assertTrue(summary["research_reused"])
        self.assertTrue(delta["general"])
        self.assertEqual(set(delta["humanization"]), revise_delivery.ALL_HUMAN)
        merged = revise_delivery.merge_review(pending, fill_delta(delta, revised))
        self.assertEqual(copycheck.check(revised, merged)["status"], "ready_for_human_approval")

    def test_scope_cannot_silently_change_text(self):
        change = {
            "kind": "scope",
            "version": "v2",
            "instruction": "Somente Feed",
            "remove_sections": ["story-1"],
            "replace_fields": {self.doc["fields"][0]["id"]: "Texto novo"},
        }
        with self.assertRaises(ValueError):
            revise_delivery.prepare(self.doc, self.review, change)

    def test_invalid_parent_cannot_be_inherited(self):
        stale = copy.deepcopy(self.review)
        stale["delivery_sha256"] = "stale"
        change = {
            "kind": "scope",
            "version": "v2",
            "instruction": "Remover Story",
            "remove_sections": ["story-1"],
        }
        with self.assertRaises(ValueError):
            revise_delivery.prepare(self.doc, stale, change)

    def test_claim_text_change_needs_valid_claim_update(self):
        claim_field = self.doc["claims"][0]["field_id"]
        change = {
            "kind": "field",
            "version": "v2",
            "instruction": "Alterar campo com claim",
            "replace_fields": {claim_field: "Novo texto sem o claim registrado"},
        }
        with self.assertRaises(ValueError):
            revise_delivery.prepare(self.doc, self.review, change)

    def test_merge_requires_only_pending_keys_and_reviewer(self):
        change = {
            "kind": "scope",
            "version": "v2",
            "instruction": "Remover Story",
            "remove_sections": ["story-1"],
        }
        revised, pending, delta, _ = revise_delivery.prepare(self.doc, self.review, change)
        complete = fill_delta(delta, revised)
        missing = copy.deepcopy(complete)
        missing["general"].pop(next(iter(missing["general"])))
        with self.assertRaises(ValueError):
            revise_delivery.merge_review(pending, missing)
        complete["reviewer"] = ""
        with self.assertRaises(ValueError):
            revise_delivery.merge_review(pending, complete)

    def test_cli_creates_small_delta_without_overwriting_parent(self):
        change = {
            "kind": "scope",
            "version": "v2",
            "instruction": "Somente Feed",
            "remove_sections": ["story-1"],
        }
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            delivery_path = tmp_path / "parent-delivery.json"
            review_path = tmp_path / "parent-review.json"
            change_path = tmp_path / "change.json"
            output = tmp_path / "v2"
            delivery_path.write_text(json.dumps(self.doc), encoding="utf-8")
            review_path.write_text(json.dumps(self.review), encoding="utf-8")
            change_path.write_text(json.dumps(change), encoding="utf-8")
            command = [
                sys.executable,
                str(ROOT / "scripts/revise_delivery.py"),
                "prepare",
                str(delivery_path),
                str(review_path),
                str(change_path),
                str(output),
            ]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((output / "review-delta.json").is_file())
            self.assertLess((output / "review-delta.json").stat().st_size, review_path.stat().st_size)
            second = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(second.returncode, 0)
            self.assertEqual(json.loads(delivery_path.read_text()), self.doc)


if __name__ == "__main__":
    unittest.main()
