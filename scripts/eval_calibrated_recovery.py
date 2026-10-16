#!/usr/bin/env python3
"""Compare engines on frozen mixed source/page/section relevance cases."""
import argparse,hashlib,json,time
from pathlib import Path
from rag_corpus import ROOT
from rag_search import Retriever

def evaluate(fixture,root=ROOT):
    fixture=Path(fixture).resolve();root=Path(root).resolve();data=json.loads(fixture.read_text());r=Retriever(root);rows=[];start=time.monotonic()
    for q in data['queries']:
        for mode in ['lexical','semantic','hybrid']:
            scopes=[False,True] if q.get('use')=='original' else [False]
            for scoped in scopes:
                payload=r.search(q['query'],q['route'],'benchmark-isolado',use=q.get('use'),limit=5,engine=mode,source_ids=q['expected'] if scoped else None)
                hits=payload['results'];target=next((h for h in hits if h['id'] in q['expected']),None)
                rank=next((i+1 for i,h in enumerate(hits) if h['id'] in q['expected']),None)
                pages=q.get('expected_pages');section=q.get('expected_section');passages=target.get('matched_passages',[]) if target else []
                rows.append(dict(id=q['id'],engine=mode,scoped=scoped,positive=bool(q['expected']),rank=rank,expected=q['expected'],page_labeled=bool(pages),section_labeled=bool(section),page_ok=bool(target and pages and target['locator']['page'] in pages),section_ok=bool(target and section and section in target['section']),passage_page_ok=bool(target and pages and any(x['page'] in pages for x in passages)),passage_section_ok=bool(target and section and any(section in x['section'] for x in passages)),violations=sum(h['guards']['client_evidence'] or r.docs[h['id']]['client']!='*' or q['route'] not in r.docs[h['id']]['routes'] or bool(q.get('use') and q['use']!=h['use']) or bool(scoped and h['id'] not in q['expected']) for h in hits),fallback=payload['fallback_reason'],top=[dict(id=h['id'],page=h['locator']['page'],section=h['section']) for h in hits]))
    summary={}
    for mode in ['lexical','semantic','hybrid']:
        for scoped in [False,True]:
            items=[x for x in rows if x['engine']==mode and x['scoped']==scoped];pos=[x for x in items if x['positive']];neg=[x for x in items if not x['positive']];pages=[x for x in pos if x['page_labeled']];sections=[x for x in pos if x['section_labeled']]
            summary[mode+('_scoped' if scoped else '_global')]=dict(positives=len(pos),negatives=len(neg),hit1=sum(x['rank']==1 for x in pos),hit3=sum(x['rank'] is not None and x['rank']<=3 for x in pos),mrr5=round(sum(1/x['rank'] if x['rank'] else 0 for x in pos)/max(1,len(pos)),4),negative_empty=sum(not x['top'] for x in neg),page_cases=len(pages),correct_page=sum(x['page_ok'] for x in pages),correct_page_in_passages=sum(x['passage_page_ok'] for x in pages),section_cases=len(sections),correct_section=sum(x['section_ok'] for x in sections),correct_section_in_passages=sum(x['passage_section_ok'] for x in sections),violations=sum(x['violations'] for x in items),fallbacks=sum(bool(x['fallback']) for x in items))
    return dict(fixture=fixture.relative_to(root).as_posix(),fixture_sha256=hashlib.sha256(fixture.read_bytes()).hexdigest(),labeling=data['labeling'],source_fingerprint=r.fingerprint,elapsed_seconds=round(time.monotonic()-start,2),summary=summary,rows=rows)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--fixture',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();report=evaluate(a.fixture);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report['summary'],indent=2))
