#!/usr/bin/env python3
"""Evaluate original-document and page/section recovery with and without source scope."""
import argparse,json,time
from pathlib import Path
from rag_corpus import ROOT
from rag_search import Retriever

def evaluate(root=ROOT):
 start=time.monotonic();cases=json.loads((root/'evals/retrieval/originals.json').read_text())['queries'];r=Retriever(root);rows=[]
 for q in cases:
  for mode in ['lexical','semantic','hybrid']:
   for scoped in [False,True]:
    p=r.search(q['query'],q['route'],'benchmark-isolado',use='original',limit=5,engine=mode,source_ids=q['expected'] if scoped else None)
    hits=p['results'];rank=next((i+1 for i,h in enumerate(hits) if h['id'] in q['expected']),None)
    target=next((h for h in hits if h['id'] in q['expected']),None)
    page_ok=target is not None and (not q.get('expected_pages') or target['locator']['page'] in q['expected_pages'])
    section_ok=target is not None and (not q.get('expected_section') or q['expected_section'] in target['section'])
    passages=target.get('matched_passages',[]) if target else []
    passage_page_ok=target is not None and (not q.get('expected_pages') or any(x['page'] in q['expected_pages'] for x in passages))
    passage_section_ok=target is not None and (not q.get('expected_section') or any(q['expected_section'] in x['section'] for x in passages))
    rows.append(dict(id=q['id'],language=q['language'],engine=mode,scoped=scoped,rank=rank,page_labeled=bool(q.get('expected_pages')),section_labeled=bool(q.get('expected_section')),page_ok=page_ok,section_ok=section_ok,passage_page_ok=passage_page_ok,passage_section_ok=passage_section_ok,fallback=p['fallback_reason'],top=[dict(id=h['id'],page=h['locator'].get('page'),section=h['section'],passage_pages=[x['page'] for x in h.get('matched_passages',[])],lexical=h['lexical_score'],semantic=h['semantic_similarity']) for h in hits[:3]]))
 summaries={}
 for mode in ['lexical','semantic','hybrid']:
  for scoped in [False,True]:
   subset=[x for x in rows if x['engine']==mode and x['scoped']==scoped]
   pages=[x for x in subset if x['page_labeled']];sections=[x for x in subset if x['section_labeled']]
   summaries[mode+('_scoped' if scoped else '_global')]=dict(cases=len(subset),hit1=sum(x['rank']==1 for x in subset),hit3=sum(x['rank'] is not None and x['rank']<=3 for x in subset),page_labeled_cases=len(pages),correct_page=sum(x['page_ok'] for x in pages),section_labeled_cases=len(sections),correct_section=sum(x['section_ok'] for x in sections),correct_page_in_three_passages=sum(x['passage_page_ok'] for x in pages),correct_section_in_three_passages=sum(x['passage_section_ok'] for x in sections),fallbacks=sum(bool(x['fallback']) for x in subset))
 return dict(labeling='Synthetic cases and expected ranges authored by the agent; not human editorial validation.',source_fingerprint=r.fingerprint,elapsed_seconds=round(time.monotonic()-start,2),summary=summaries,rows=rows)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True);a=p.parse_args();report=evaluate();a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report['summary'],indent=2))
