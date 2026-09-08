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
if __name__=='__main__': unittest.main()
