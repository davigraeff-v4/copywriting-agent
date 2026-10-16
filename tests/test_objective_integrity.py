"""Regressions for objective defects found in the October audit."""
import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import copycheck as c
from test_copycheck import fixture_review


class ObjectiveIntegrity(unittest.TestCase):
    def setUp(self):
        self.doc = c.load(c.ROOT / 'tests/fixtures/valid-delivery.json')

    def test_budget_counts_every_public_role_except_explicit_exclusions(self):
        for role in ('bullet', 'table', 'step', 'proof', 'transition', 'stat', 'new_role'):
            with self.subTest(role=role):
                d = copy.deepcopy(self.doc)
                d['fields'].append(dict(id='extra', section='dobra-1', role=role, text=' '.join(['catálogo'] * 301)))
                self.assertIn('word budget', ' '.join(c.check(d)['errors']))
        d = copy.deepcopy(self.doc)
        d['fields'].append(dict(id='option', section='dobra-1', role='form_option', text=' '.join(['nome'] * 301)))
        self.assertEqual(c.word_count(d), c.word_count(self.doc))

    def test_required_headline_term_cannot_be_satisfied_by_body(self):
        self.doc['constraints'][0].update(required_terms=['catálogo'], applies_to={'roles': ['headline']})
        self.assertEqual(c.check(self.doc)['status'], 'blocked')
        self.doc['fields'][0]['text'] = 'Consulte o catálogo de peças'
        self.assertEqual(c.check(self.doc)['status'], 'needs_editorial_review')

    def test_section_scope_does_not_consume_other_section(self):
        self.doc['route'] = 'ads'
        self.doc['fields'].append(dict(id='elsewhere', section='dobra-2', role='body', text='Informação exclusiva'))
        self.doc['requirements'].pop('sections')
        self.doc['constraints'][0].update(required_terms=['exclusiva'], applies_to={'sections': ['dobra-1']})
        self.assertEqual(c.check(self.doc)['status'], 'blocked')

    def test_forbidden_scope_and_word_boundaries(self):
        self.doc['constraints'][0].update(forbidden_terms=['catálogo'], applies_to={'roles': ['headline']})
        self.assertEqual(c.check(self.doc)['status'], 'needs_editorial_review')
        self.doc['constraints'][0].update(forbidden_terms=[], required_terms=['peça'])
        self.assertEqual(c.check(self.doc)['status'], 'blocked')

    def test_unknown_and_ambiguous_scope_fail_closed(self):
        for selector in ({'roles': ['missing']}, {'roles': []}, {'roles': ['headline'], 'sections': ['absent']}, {'bad': ['hero']}):
            d = copy.deepcopy(self.doc); d['constraints'][0]['applies_to'] = selector
            self.assertEqual(c.check(d)['status'], 'blocked')
        self.doc['constraints'][0].update(scope='headline', required_terms=['peças'])
        self.assertEqual(c.check(self.doc)['status'], 'blocked')

    def test_empty_claim_inventory_needs_decision_for_each_field(self):
        self.doc['claims'] = []
        r = fixture_review(self.doc); r.pop('field_checks')
        self.assertEqual(c.check(self.doc, r)['status'], 'blocked')

    def test_claim_cannot_be_waived_or_mapped_to_another_field(self):
        r = fixture_review(self.doc)
        r['field_checks']['body'].update(status='no_factual_claim', claim_ids=[])
        self.assertEqual(c.check(self.doc, r)['status'], 'blocked')
        r = fixture_review(self.doc)
        r['field_checks']['hero'].update(status='mapped', claim_ids=['c1'])
        self.assertEqual(c.check(self.doc, r)['status'], 'blocked')

    def test_source_missing_hash_changed_or_excerpt_fabricated_blocks(self):
        for mutation in ('missing', 'hash', 'excerpt', 'escape'):
            d = copy.deepcopy(self.doc); r = fixture_review(d)
            if mutation == 'missing': r['source_checks']['s1']['path'] = 'missing-source.txt'
            elif mutation == 'hash': r['source_checks']['s1']['sha256'] = 'changed'
            elif mutation == 'escape': r['source_checks']['s1']['path'] = '../outside.txt'
            else:
                d['sources'][0]['excerpt'] = 'A empresa garante dobrar o faturamento.'
                r['delivery_sha256'] = c.digest(d)
            with self.subTest(mutation=mutation):
                self.assertEqual(c.check(d, r)['status'], 'blocked')

    def test_changed_validator_and_legacy_review_require_new_validation(self):
        r = fixture_review(self.doc); r['validator_sha256'] = 'old'
        self.assertEqual(c.check(self.doc, r)['status'], 'blocked')
        r = fixture_review(self.doc); r.pop('gate_version')
        self.assertEqual(c.check(self.doc, r)['status'], 'blocked')

    def test_partial_render_cannot_ignore_invalid_piece(self):
        self.doc['route'] = 'ads'; self.doc['requirements'].pop('sections')
        self.doc['fields'].append(dict(id='rejected_piece', section='piece-2', role='headline', text='Direto pra sua oficina'))
        self.assertEqual(c.check(self.doc, fixture_review(self.doc))['status'], 'blocked')

    def test_source_alias_preserves_hash_and_excerpt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); path = root/'clients/a/fontes/source.txt'; path.parent.mkdir(parents=True)
            path.write_text(self.doc['sources'][0]['excerpt'])
            registry = root/'.local/client-path-map.json'; registry.parent.mkdir()
            registry.write_text(json.dumps({'paths': {'old.txt': {'destination': 'clients/a/fontes/source.txt'}}}))
            r = fixture_review(self.doc)
            r['source_checks']['s1'].update(path='old.txt', sha256=hashlib.sha256(path.read_bytes()).hexdigest())
            from client_paths import resolve_reference
            self.assertEqual(resolve_reference('old.txt', root), path.resolve())
            with patch.object(c, 'resolve_reference', side_effect=lambda ref, _: resolve_reference(ref, root)):
                self.assertEqual(c.check(self.doc, r)['status'], 'ready_for_human_approval')
                path.write_text('Fonte alterada após o registro')
                self.assertEqual(c.check(self.doc, r)['status'], 'blocked')


if __name__ == '__main__':
    unittest.main()
