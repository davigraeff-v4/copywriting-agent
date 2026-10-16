import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from evaluate import prepare,summarize
class Evaluation(unittest.TestCase):
    def setUp(self):
        self.records=[dict(case_id='c1',repetition=1,system=s,model_id='same-model',effort='medium',prompt_sha256='p',context_sha256='c',system_prompt_sha256=s,text='Copy '+s) for s in ['baseline','v2']]
    def test_blind_and_count(self):
        blind,key,votes=prepare(self.records)
        self.assertNotIn('system',blind['comparisons'][0]['options'][0])
        label=next(r['label'] for r in key['entries'] if r['metadata']['system']=='v2')
        votes[0].update(rater='human fixture',winner=label,reason='Test vote only')
        result=summarize(key,votes)
        self.assertEqual(result['wins']['v2'],1); self.assertEqual(result['pending'],0)
    def test_mismatch_rejected(self):
        for field in ['model_id','effort','prompt_sha256','context_sha256']:
            d=copy.deepcopy(self.records); d[1][field]='different'
            with self.assertRaises(ValueError): prepare(d)
    def test_pending_not_fabricated(self):
        b,k,v=prepare(self.records)
        self.assertEqual(summarize(k,[])['pending'],1)
        with self.assertRaises(ValueError): summarize(k,v)
    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError): prepare(self.records+[self.records[0]])
    def test_briefing_and_route_visible_without_system_key(self):
        for r in self.records: r.update(route='ads',briefing='Briefing fictício igual nas condições.')
        blind,key,votes=prepare(self.records)
        row=blind['comparisons'][0]
        self.assertEqual(row['briefing'],self.records[0]['briefing'])
        self.assertEqual(row['route'],'ads')
        self.assertTrue(all(set(o)=={'label','text'} for o in row['options']))
        self.records[1]['briefing']='Outro pedido'
        with self.assertRaises(ValueError): prepare(self.records)
    def test_incomplete_system_matrix_rejected(self):
        more=[dict(r,case_id='c2') for r in self.records]
        more[1]['system']='third'
        with self.assertRaises(ValueError): prepare(self.records+more)
    def test_edit_time_missing_is_not_zero_and_measured_zero_is_valid(self):
        blind,key,votes=prepare(self.records)
        label=next(r['label'] for r in key['entries'] if r['metadata']['system']=='v2')
        votes[0].update(rater='human fixture',winner='tie',reason='Fixture tie',edit_minutes={label:0})
        result=summarize(key,votes)
        self.assertEqual(result['edit_minutes']['v2'],dict(n=1,mean=0,median=0))
        self.assertEqual(result['edit_minutes']['baseline'],dict(n=0,mean=None,median=None))
    def test_invalid_edit_measurements_rejected(self):
        _,key,votes=prepare(self.records)
        label=key['entries'][0]['label']
        for value in (-1,True,'5',float('nan'),float('inf')):
            votes[0].update(rater='human fixture',winner='tie',reason='Fixture',edit_minutes={label:value})
            with self.subTest(value=value), self.assertRaises(ValueError): summarize(key,votes)
    def test_route_results_preserve_ties_and_pending(self):
        for r in self.records: r.update(route='ads',briefing='Fictional ads briefing')
        others=[dict(r,case_id='c2',route='lp',briefing='Fictional LP briefing') for r in self.records]
        _,key,votes=prepare(self.records+others)
        votes[0].update(rater='human fixture',winner='tie',reason='Fixture')
        result=summarize(key,votes[:1])
        self.assertEqual(result['by_route']['ads']['ties'],1)
        self.assertEqual(result['by_route']['lp']['pending'],1)
        self.assertEqual(result['by_route']['lp']['win_share'],{'baseline':None,'v2':None})
    def test_human_dimensions_and_diagnoses_need_evidence(self):
        _,key,votes=prepare(self.records)
        entry=key['entries'][0]; label=entry['label']; system=entry['metadata']['system']
        votes[0].update(rater='human fixture',winner='tie',reason='Fixture',
                        assessments={label:{'argumento':dict(score=3,quote='Copy',reason='Fixture observation')}},
                        diagnoses={label:dict(stage='direcao',reason='Fixture hypothesis')})
        result=summarize(key,votes)
        self.assertEqual(result['human_assessments'][system]['argumento']['mean'],3)
        self.assertEqual(result['human_assessments'][system]['voz']['n'],0)
        self.assertEqual(result['failure_stage_reports'][system],{'direcao':1})
        votes[0]['assessments'][label]['argumento']['quote']=' '
        with self.assertRaises(ValueError): summarize(key,votes)
    def test_unknown_labels_cannot_be_counted_as_measurements(self):
        _,key,votes=prepare(self.records)
        for group,value in [('edit_minutes',3),('assessments',{}),('diagnoses',{})]:
            bad=copy.deepcopy(votes)
            bad[0].update(rater='human fixture',winner='tie',reason='Fixture')
            bad[0][group]={'Z':value}
            with self.subTest(group=group), self.assertRaises(ValueError): summarize(key,bad)
    def test_empty_outputs_not_a_prepared_benchmark(self):
        with self.assertRaises(ValueError): prepare([])
if __name__=='__main__': unittest.main()
