#!/usr/bin/env python3
"""Compare retrieval engines on frozen, synthetic relevance cases, not copy quality."""
import argparse,hashlib,json,math,time
from pathlib import Path
from rag_corpus import ROOT,public_entries
from rag_search import Retriever
from retrieve import retrieve,load_entries
MODES=['metadata_original','metadata_expanded','lexical','semantic','hybrid']

def summarize(rows):
    positive=[r for r in rows if r['expected']];negative=[r for r in rows if not r['expected']]
    n=len(positive)
    def ratio(value,total):return round(value/total,4) if total else None
    return dict(positive_cases=n,negative_cases=len(negative),hit1=ratio(sum(r['rank']==1 for r in positive),n),hit3=ratio(sum(r['rank'] is not None and r['rank']<=3 for r in positive),n),hit5=ratio(sum(r['rank'] is not None and r['rank']<=5 for r in positive),n),mrr5=ratio(sum(1/r['rank'] if r['rank'] and r['rank']<=5 else 0 for r in positive),n),ndcg5=ratio(sum(r['ndcg5'] for r in positive),n),negative_empty=ratio(sum(not r['top'] for r in negative),len(negative)),filter_violations=sum(r['filter_violations'] for r in rows),fallbacks=sum(bool(r['fallback']) for r in rows))

def evaluate(fixture,root=ROOT,modes=MODES):
    fixture=Path(fixture).resolve();root=Path(root).resolve();data=json.loads(fixture.read_text());start=time.monotonic()
    entries=public_entries(root);lookup={e['id']:e for e in entries};retriever=Retriever(root)
    expanded_metadata=[e for e in entries if not e.get('extraction_path')]
    original=load_entries(root=root);rows=[]
    for item in data['queries']:
        if not set(item['expected'])<=set(lookup):raise ValueError('expected source absent')
        for mode in modes:
            if mode.startswith('metadata'):
                hits=retrieve(item['query'],original if mode=='metadata_original' else expanded_metadata,item['route'],'benchmark-isolado',use=item.get('use'),limit=5,root=root);fallback=None;engine='metadata'
            else:
                payload=retriever.search(item['query'],item['route'],'benchmark-isolado',item.get('use'),5,mode)
                hits=payload['results'];fallback=payload['fallback_reason'];engine=payload['engine_used']
            ids=[r['id'] for r in hits];expected=set(item['expected'])
            rank=next((i+1 for i,did in enumerate(ids) if did in expected),None)
            dcg=sum((1/math.log2(i+2)) for i,did in enumerate(ids) if did in expected)
            ideal=sum(1/math.log2(i+2) for i in range(min(5,len(expected))))
            violations=sum(bool(lookup[r['id']]['client']!='*' or item['route'] not in lookup[r['id']]['routes'] or (item.get('use') and item['use']!=lookup[r['id']]['use'])) for r in hits)
            rows.append(dict(id=item['id'],query=item['query'],route=item['route'],expected=item['expected'],mode=mode,engine_used=engine,rank=rank,ndcg5=dcg/ideal if ideal else 0,filter_violations=violations,fallback=fallback,top=[dict(id=r['id'],section=r.get('section'),score=r['score'],similarity=r.get('semantic_similarity')) for r in hits]))
    report=dict(fixture=fixture.relative_to(root).as_posix(),fixture_sha256=hashlib.sha256(fixture.read_bytes()).hexdigest(),labeling=data['labeling'],documents=len(entries),expanded_metadata_documents=len(expanded_metadata),metadata_scope='Legacy text-reference comparator; audited originals evaluated separately.',chunks=len(retriever.chunks),source_fingerprint=retriever.fingerprint,elapsed_seconds=round(time.monotonic()-start,2),summary={m:summarize([r for r in rows if r['mode']==m]) for m in modes},by_route={m:{route:summarize([r for r in rows if r['mode']==m and r['route']==route]) for route in ['ads','lp','social','direct']} for m in modes},rows=rows)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--fixture',type=Path,default=ROOT/'evals/retrieval/development.json');p.add_argument('--out',type=Path);a=p.parse_args()
    report=evaluate(a.fixture)
    if a.out:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'summary':report['summary'],'elapsed_seconds':report['elapsed_seconds']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
