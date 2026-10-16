import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from context_trace import catalog, skill_read, source_read, append_event, audit_usage, audit_redundancy


class ContextTraceTests(unittest.TestCase):
    def setUp(self):
        self.events = [dict(event='source_read', id='method', text='Cada etapa acrescenta informação.', truncated=False),
                       dict(event='skill_read', id='07')]
        self.output = dict(fields=[dict(id='h', text='Escolha os itens'), dict(id='b', text='Confira endereço e taxa')],
                           skill_decisions=[dict(skill_id='07', decision='used')],
                           reference_uses=[dict(reference_id='method', decision='applied',
                                                source_quote='Cada etapa acrescenta informação.',
                                                application='Separar escolha de conferência.',
                                                field_ids=['b'], output_quote='Confira endereço',
                                                limitation='Não importar fatos da fonte.')])

    def test_real_catalog_discovers_fourteen_and_reads_full_skill(self):
        items = catalog()
        self.assertEqual(len(items), 14)
        read = skill_read('07', 'context', 'Pesquisar repertório')
        self.assertEqual(read['text'], (Path(__file__).resolve().parents[1] / read['path']).read_text())
        self.assertFalse(read['truncated'])

    def test_skill_selector_does_not_accept_paths(self):
        with self.assertRaises(ValueError):
            skill_read('../../secret', 'context', 'invalid')

    def test_used_reference_is_linked_to_read_source_and_public_field(self):
        self.assertEqual(audit_usage(self.events, self.output)['errors'], [])

    def test_excerpt_only_is_not_a_complete_read(self):
        self.events[0]['event'] = 'search'
        self.assertTrue(audit_usage(self.events, self.output)['errors'])

    def test_wrong_or_truncated_source_is_rejected(self):
        for key, value in [('id', 'other'), ('truncated', True), ('text', 'Algo diferente')]:
            events = copy.deepcopy(self.events)
            events[0][key] = value
            self.assertTrue(audit_usage(events, self.output)['errors'])

    def test_invented_target_or_output_quote_is_rejected(self):
        for key, value in [('field_ids', ['absent']), ('output_quote', 'Uma promessa inventada')]:
            output = copy.deepcopy(self.output)
            output['reference_uses'][0][key] = value
            self.assertTrue(audit_usage(self.events, output)['errors'])

    def test_used_skill_requires_observed_read(self):
        self.output['skill_decisions'][0]['skill_id'] = '08'
        self.assertTrue(audit_usage(self.events, self.output)['errors'])

    def test_non_selected_candidate_does_not_require_fictitious_application(self):
        self.output['reference_uses'] = [dict(reference_id='other', decision='not_deepened')]
        self.assertEqual(audit_usage(self.events, self.output)['errors'], [])

    def test_trace_appends_without_erasing_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'trace.jsonl'
            append_event(path, self.events[0])
            append_event(path, self.events[1])
            self.assertEqual([json.loads(s)['event'] for s in path.read_text().splitlines()],
                             ['source_read', 'skill_read'])

    def test_source_unknown_or_absent_locator_has_no_substitute(self):
        with self.assertRaises(ValueError):
            source_read('not-a-real-source')
        with self.assertRaises(ValueError):
            source_read('narrativa-lp', page=999)

    def pair(self, classification):
        return dict(a_field='h', a_quote='Escolha os itens', b_field='b', b_quote='Confira endereço',
                    classification=classification, reason='Funções da sequência.', effect='Impacto no desenvolvimento.')

    def test_functional_repetition_does_not_justify_penalty(self):
        pair = self.pair('functional')
        self.assertEqual(audit_redundancy(self.output['fields'], 10, [pair]), [])
        self.assertTrue(audit_redundancy(self.output['fields'], 5, [pair]))

    def test_penalty_requires_exact_pair_and_material_reason(self):
        self.assertTrue(audit_redundancy(self.output['fields'], 5, []))
        pair = self.pair('avoidable')
        self.assertEqual(audit_redundancy(self.output['fields'], 5, [pair]), [])
        pair['b_quote'] = 'Absent'
        self.assertTrue(audit_redundancy(self.output['fields'], 5, [pair]))

    def test_no_penalty_and_no_material_repetition_is_valid(self):
        self.assertEqual(audit_redundancy(self.output['fields'], 10, []), [])
        self.assertTrue(audit_redundancy(self.output['fields'], 10, [self.pair('avoidable')]))

    def test_identical_occurrence_cannot_be_its_own_pair(self):
        pair = self.pair('avoidable')
        pair.update(b_field=pair['a_field'], b_quote=pair['a_quote'])
        self.assertTrue(audit_redundancy(self.output['fields'], 5, [pair]))


if __name__ == '__main__':
    unittest.main()
