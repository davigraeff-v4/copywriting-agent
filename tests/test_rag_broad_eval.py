import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from eval_rag_broad import summarize

def row(**changes):
 r=dict(positive=True,category='curated_positive',rank=1,top=[{}],page_labeled=False,section_labeled=False,page_first=False,section_first=False,page_target=False,section_target=False,page_passages=False,section_passages=False,scope_violations=0,locator_errors=0,authority_errors=0,fallback=None,channel_warning=None,elapsed_ms=10)
 r.update(changes);return r
class BroadGrades(unittest.TestCase):
 def test_grade_distinguishes_first_result_from_late_recovery(self):
  result=summarize([row(rank=1),row(rank=3),row(rank=None,top=[])])
  self.assertAlmostEqual(result['hit1'],1/3);self.assertAlmostEqual(result['hit3'],2/3)
  self.assertEqual(result['recovery_grade'],5.33)
 def test_unlabeled_pages_and_negative_cases_do_not_inflate_page_grades(self):
  result=summarize([row(page_labeled=True,page_first=False,page_target=True,page_passages=True),row(positive=False,category='out_of_domain',rank=None,top=[]),row()])
  self.assertEqual(result['page_cases'],1);self.assertEqual(result['page_grade'],0);self.assertEqual(result['page_within_target'],1);self.assertEqual(result['abstention_grade'],10)
 def test_no_applicable_denominator_is_null_instead_of_ten(self):
  result=summarize([row(positive=False,category='authority_limits',rank=None,top=[])])
  for key in ['recovery_grade','page_grade','section_grade','abstention_grade']:self.assertIsNone(result[key])
if __name__=='__main__':unittest.main()
