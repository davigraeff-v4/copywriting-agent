"""Lifecycle regressions: real gate, bounded retries, preserved evidence and no approval forgery."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import copycheck as gate
import review_cycle as cycle
from test_copycheck import fixture_review

class ReviewCycle(unittest.TestCase):
    def setUp(self):
        self.doc=gate.load(gate.ROOT/'tests/fixtures/valid-delivery.json')
        self.state=cycle.start('case','direction-1')
        self.diag=dict(category='writing',reason='Progressão insuficiente.',field_ids=['hero'],changes=['Reorganizar o argumento.'],next_step='Reescrever a sequência preservando os fatos.',can_fix_with_available_context=True,missing_information=[])
    def bad(self,d):
        r=fixture_review(d);r['general']['progressao']['score']=7;return r
    def changed(self,i):
        d=copy.deepcopy(self.doc);d['fields'][0]['text']+=' agora'*i;return d
    def test_pass_is_readiness_never_human_approval(self):
        s=cycle.record_attempt(self.state,self.doc,fixture_review(self.doc));self.assertEqual(s['status'],'ready_for_human_approval');self.assertFalse(s['human_approval'])
    def test_failure_requests_specific_internal_correction(self):
        s=cycle.record_attempt(self.state,self.doc,self.bad(self.doc),self.diag);self.assertEqual(s['status'],'needs_revision');self.assertEqual(s['rewrites'],0);self.assertEqual(s['next_action'],self.diag['next_step'])
    def test_rewrite_can_recover_without_modifying_initial_version(self):
        s=cycle.record_attempt(self.state,self.doc,self.bad(self.doc),self.diag);initial=copy.deepcopy(s['attempts'][0]);d=self.changed(1)
        s=cycle.record_attempt(s,d,fixture_review(d));self.assertEqual(s['status'],'ready_for_human_approval');self.assertEqual(s['rewrites'],1);self.assertEqual(s['attempts'][0],initial)
    def test_two_rewrites_end_with_actionable_direction(self):
        s=cycle.record_attempt(self.state,self.doc,self.bad(self.doc),self.diag)
        for i in (1,2):
            d=self.changed(i);s=cycle.record_attempt(s,d,self.bad(d),self.diag)
        self.assertEqual(s['status'],'needs_direction');self.assertEqual(s['rewrites'],2);self.assertEqual(len(s['attempts']),3);self.assertIn(self.diag['next_step'],s['next_action'])
        with self.assertRaises(ValueError):cycle.record_attempt(s,self.changed(3),fixture_review(self.changed(3)))
    def test_same_copy_cannot_be_rerated_after_writing_failure(self):
        s=cycle.record_attempt(self.state,self.doc,self.bad(self.doc),self.diag)
        with self.assertRaises(ValueError):cycle.record_attempt(s,self.doc,fixture_review(self.doc))
    def test_version_rename_does_not_count_as_rewrite(self):
        s=cycle.record_attempt(self.state,self.doc,self.bad(self.doc),self.diag);d=copy.deepcopy(self.doc);d['version']='v999'
        with self.assertRaises(ValueError):cycle.record_attempt(s,d,fixture_review(d))
    def test_direction_label_cannot_reset_budget(self):
        with self.assertRaises(ValueError):cycle.record_attempt(self.state,self.doc,fixture_review(self.doc),direction_id='new')
    def test_missing_data_stops_with_named_question(self):
        d=dict(self.diag,category='evidence',can_fix_with_available_context=False,missing_information=['Documento da garantia.'],next_step='Confirmar o escopo da garantia ou autorizar retirada da promessa.')
        s=cycle.record_attempt(self.state,self.doc,self.bad(self.doc),d);self.assertEqual(s['status'],'needs_input');self.assertIn('garantia',s['next_action'])
    def test_missing_data_cannot_be_an_unspecified_stop(self):
        d=dict(self.diag,can_fix_with_available_context=False)
        with self.assertRaises(ValueError):cycle.record_attempt(self.state,self.doc,self.bad(self.doc),d)
    def test_missing_review_is_not_success(self):
        s=cycle.record_attempt(self.state,self.doc,None);self.assertEqual(s['status'],'needs_review_repair')
        s=cycle.record_attempt(s,self.doc,fixture_review(self.doc));self.assertEqual(s['status'],'ready_for_human_approval');self.assertEqual(s['rewrites'],0);self.assertEqual(s['review_repairs'],1)
    def test_review_repair_cannot_hide_rewrite(self):
        s=cycle.record_attempt(self.state,self.doc,None)
        with self.assertRaises(ValueError):cycle.record_attempt(s,self.changed(1),fixture_review(self.changed(1)))
    def test_review_repairs_are_bounded(self):
        s=cycle.record_attempt(self.state,self.doc,None)
        for _ in range(2):s=cycle.record_attempt(s,self.doc,None)
        self.assertEqual(s['status'],'needs_review_decision');self.assertEqual(s['review_repairs'],2)
    def test_stale_review_still_blocks_rewritten_text(self):
        s=cycle.record_attempt(self.state,self.doc,self.bad(self.doc),self.diag);d=self.changed(1)
        s=cycle.record_attempt(s,d,fixture_review(self.doc),dict(self.diag,category='review'));self.assertEqual(s['status'],'needs_review_repair');self.assertIn('stale review',' '.join(s['attempts'][-1]['result']['errors']))
    def test_tampered_state_and_history_rejected(self):
        s=cycle.record_attempt(self.state,self.doc,self.bad(self.doc),self.diag)
        for change in ['counter','event','direction','approval']:
            t=copy.deepcopy(s)
            if change=='counter':t['rewrites']=0;t['status']='awaiting_initial_review'
            elif change=='event':t['attempts'][0]['result']['status']='ready_for_human_approval'
            elif change=='direction':t['direction_id']='reset'
            else:t['human_approval']=True
            with self.subTest(change=change),self.assertRaises(ValueError):cycle.record_attempt(t,self.changed(1),fixture_review(self.changed(1)))
    def test_persistence_rejects_rollback_and_changed_snapshots(self):
        with tempfile.TemporaryDirectory() as tmp:
            s=cycle.persist_attempt(tmp,self.state,self.doc,self.bad(self.doc),self.diag)
            with self.assertRaises(ValueError):cycle.persist_attempt(tmp,self.state,self.doc,self.bad(self.doc),self.diag)
            f=Path(tmp)/'attempt-01/delivery.json';f.write_text(json.dumps(self.changed(9)))
            with self.assertRaises(ValueError):cycle.persist_attempt(tmp,s,self.changed(1),fixture_review(self.changed(1)))
    def test_ready_cycle_cannot_continue(self):
        s=cycle.record_attempt(self.state,self.doc,fixture_review(self.doc))
        with self.assertRaises(ValueError):cycle.record_attempt(s,self.changed(1),fixture_review(self.changed(1)))
    def test_new_information_resumes_without_resetting_budget(self):
        d=dict(self.diag,category='context',can_fix_with_available_context=False,missing_information=['Fonte adicional.'])
        state=cycle.record_attempt(self.state,self.doc,self.bad(self.doc),d)
        updated=copy.deepcopy(self.doc);source=copy.deepcopy(updated['sources'][0]);source['id']='additional';updated['sources'].append(source)
        resolution=dict(kind='new_information',reason='Fonte adicional preservada.',source_ids=['additional'])
        result=cycle.record_attempt(state,updated,fixture_review(updated),resolution=resolution)
        self.assertEqual(result['status'],'ready_for_human_approval');self.assertEqual(result['rewrites'],1);self.assertEqual(len(result['attempts']),2)
        self.assertEqual(result['attempts'][-1]['resolution'],resolution)
    def test_resumption_rejects_unchanged_or_unknown_source(self):
        diag=dict(self.diag,category='context',can_fix_with_available_context=False,missing_information=['Dado necessário.'])
        state=cycle.record_attempt(self.state,self.doc,self.bad(self.doc),diag)
        for ids in (['s1'],['unknown']):
            with self.subTest(ids=ids),self.assertRaises(ValueError):cycle.record_attempt(state,self.doc,fixture_review(self.doc),resolution=dict(kind='new_information',reason='Dados recebidos.',source_ids=ids))
    def test_new_source_cannot_reset_exhausted_budget(self):
        state=cycle.record_attempt(self.state,self.doc,self.bad(self.doc),self.diag)
        d=self.changed(1);state=cycle.record_attempt(state,d,self.bad(d),self.diag)
        d=self.changed(2);diag=dict(self.diag,category='context',can_fix_with_available_context=False,missing_information=['Dado necessário.'])
        state=cycle.record_attempt(state,d,self.bad(d),diag)
        self.assertEqual(state['status'],'needs_input');self.assertEqual(state['rewrites'],2)
        updated=copy.deepcopy(d);source=copy.deepcopy(updated['sources'][0]);source['id']='additional';updated['sources'].append(source)
        with self.assertRaises(ValueError):cycle.record_attempt(state,updated,fixture_review(updated),resolution=dict(kind='new_information',reason='Novo dado.',source_ids=['additional']))
    def test_failed_attempt_requires_diagnosis_and_valid_field(self):
        with self.assertRaises(ValueError):cycle.record_attempt(self.state,self.doc,self.bad(self.doc))
        with self.assertRaises(ValueError):cycle.record_attempt(self.state,self.doc,self.bad(self.doc),dict(self.diag,field_ids=['inexistente']))

if __name__=='__main__':unittest.main()
