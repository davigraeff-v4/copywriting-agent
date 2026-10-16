#!/usr/bin/env python3
"""Frozen, multi-scenario RAG evaluation. Computes transparent grades; never tunes ranking."""
from __future__ import annotations
import argparse,hashlib,json,math,statistics,time
from collections import Counter
from pathlib import Path
from rag_corpus import ROOT
from rag_search import Retriever
ENGINES=('lexical','semantic','hybrid')

def is_positive(q):return bool(q['expected']) and q['category']!='authority_limits'
def section_matches(text,labels):return any(label in text for label in labels)
def grade(value):return round(10*value,2) if value is not None else None
def fraction(count,total):return count/total if total else None

def summarize(rows):
    positive=[r for r in rows if r['positive']];neg=[r for r in rows if r['category']=='out_of_domain'];pages=[r for r in positive if r['page_labeled']];sections=[r for r in positive if r['section_labeled']]
    n=len(positive);hit1=fraction(sum(r['rank']==1 for r in positive),n);hit3=fraction(sum(r['rank'] is not None and r['rank']<=3 for r in positive),n);hit5=fraction(sum(r['rank'] is not None and r['rank']<=5 for r in positive),n)
    mrr=fraction(sum(1/r['rank'] if r['rank'] else 0 for r in positive),n)
    result=dict(cases=len(rows),positive_cases=n,negative_cases=len(neg),hit1=hit1,hit3=hit3,hit5=hit5,mrr5=mrr,first_result_grade=grade(hit1),availability_grade=grade(hit3),recovery_grade=grade(.6*mrr+.4*hit3) if n else None,
        negative_empty=fraction(sum(not r['top'] for r in neg),len(neg)),abstention_grade=grade(fraction(sum(not r['top'] for r in neg),len(neg))),page_cases=len(pages),page_first=fraction(sum(r['page_first'] for r in pages),len(pages)),page_within_target=fraction(sum(r['page_target'] for r in pages),len(pages)),page_among_top3_passages=fraction(sum(r['page_passages'] for r in pages),len(pages)),page_grade=grade(fraction(sum(r['page_first'] for r in pages),len(pages))),section_cases=len(sections),section_first=fraction(sum(r['section_first'] for r in sections),len(sections)),section_within_target=fraction(sum(r['section_target'] for r in sections),len(sections)),section_among_top3_passages=fraction(sum(r['section_passages'] for r in sections),len(sections)),section_grade=grade(fraction(sum(r['section_first'] for r in sections),len(sections))),scope_violations=sum(r['scope_violations'] for r in rows),locator_errors=sum(r['locator_errors'] for r in rows),authority_errors=sum(r['authority_errors'] for r in rows),fallbacks=sum(bool(r['fallback']) for r in rows),channel_warnings=sum(bool(r['channel_warning']) for r in rows))
    timings=sorted(r['elapsed_ms'] for r in rows)
    if timings:result['latency_ms']=dict(median=round(statistics.median(timings),2),p95=round(timings[max(0,math.ceil(.95*len(timings))-1)],2),max=round(max(timings),2))
    return result

def evaluate(fixture,root=ROOT,shard=None):
    root=Path(root).resolve();fixture=Path(fixture).resolve();data=json.loads(fixture.read_text());cases=data['queries'];start=time.monotonic();r=Retriever(root)
    if shard is not None:
        families={'catalog':{'curated_guidance','curated_positive','curated_structure','situational_method'},'originals':{'pdf_chapter','txt_chapter','image_reference'},'stress':{'out_of_domain','robustness','short_query','authority_limits','known_source_section'}}
        cases=[q for q in cases if q['category'] in families[shard]]
    rows=[]
    for number,q in enumerate(cases,1):
        if not set(q['expected'])<=set(r.docs):raise ValueError('expected source absent')
        for mode in ENGINES:
            scopes=['source_assisted'] if q.get('source_filter') else ['global','source_assisted'] if q.get('use')=='original' else ['global']
            for scope in scopes:
                begun=time.monotonic();payload=r.search(q['query'],q['route'],'benchmark-isolado',use=q.get('use'),limit=5,engine=mode,source_ids=q.get('source_filter') or (q['expected'] if scope=='source_assisted' else None))
                ms=(time.monotonic()-begun)*1000;hits=payload['results'];expected=set(q['expected']);target=next((h for h in hits if h['id'] in expected),None)
                rank=next((i+1 for i,h in enumerate(hits) if h['id'] in expected),None)
                pages=q.get('expected_pages',[]);sections=q.get('expected_sections',[]);first=hits[0] if hits else None
                source_first=first is not None and first['id'] in expected
                page_first=bool(source_first and pages and first['locator']['page'] in pages)
                section_first=bool(source_first and sections and section_matches(first['section'],sections))
                page_target=bool(target and pages and target['locator']['page'] in pages);section_target=bool(target and sections and section_matches(target['section'],sections))
                candidates=[p for h in hits[:3] if h['id'] in expected for p in h.get('matched_passages',[])[:3]]
                page_passages=bool(pages and any(p['page'] in pages for p in candidates));section_passages=bool(sections and any(section_matches(p['section'],sections) for p in candidates))
                scope_bad=loc_bad=authority_bad=0;top=[]
                for h in hits:
                    d=r.docs[h['id']];c=next(c for c in r.chunks if c['id']==h['chunk_id']);source=r.document_data[h['id']];locator=h['locator']
                    scope_bad+=int(d['client']!='*' or q['route'] not in d['routes'] or bool(q.get('use') and q['use']!=d['use']) or bool(scope=='source_assisted' and h['id'] not in (q.get('source_filter') or q['expected'])))
                    loc_bad+=int(source['text'][locator['start_char']:locator['end_char']]!=h['excerpt'] or h['source_sha256']!=d['sha256'] or c['page']!=locator['page'] or c['section']!=h['section'])
                    for p in h.get('matched_passages',[]):loc_bad+=int(source['text'][p['start_char']:p['end_char']]!=p['excerpt'])
                    g=h['guards'];authority_bad+=int(g['client_evidence'] is not False or g['external_content_is_data'] is not True or g['requires_full_read'] is not True or g.get('human_approved')!=d.get('human_approved',False) or g.get('performance_verified')!=d.get('performance_verified',False))
                    top.append(dict(id=h['id'],path=h['path'],section=h['section'],page=locator.get('page'),chapter=locator.get('chapter_number'),chunk_id=h['chunk_id'],source_sha256=h['source_sha256'],score=h['score'],semantic_similarity=h['semantic_similarity'],lexical_score=h['lexical_score'],excerpt=h['excerpt'][:380],passages=[dict(section=p['section'],page=p['page']) for p in h.get('matched_passages',[])],guards=g))
                score=round(10/rank,2) if rank else 0 if is_positive(q) else 10 if q['category']=='out_of_domain' and not hits else 0 if q['category']=='out_of_domain' else None
                rows.append(dict(id=q['id'],category=q['category'],query=q['query'],route=q['route'],use=q.get('use'),language=q.get('language','pt'),variant=q.get('variant'),base_case=q.get('base_case'),engine=mode,engine_used=payload['engine_used'],scope=scope,positive=is_positive(q),expected=q['expected'],expected_paths=[r.docs[x]['path'] for x in q['expected']],expected_pages=pages,expected_sections=sections,rank=rank,case_grade=score,page_labeled=bool(pages),section_labeled=bool(sections),page_first=page_first,section_first=section_first,page_target=page_target,section_target=section_target,page_passages=page_passages,section_passages=section_passages,scope_violations=scope_bad,locator_errors=loc_bad,authority_errors=authority_bad,fallback=payload['fallback_reason'],channel_warning=payload.get('semantic_channel_warning'),semantic_channel=payload.get('semantic_channel'),elapsed_ms=round(ms,3),top=top))
        if number%10==0 or number==len(cases):print(f'{shard or "all"}: {number}/{len(cases)} cases; {len(rows)} engine executions',flush=True)
    return dict(fixture=fixture.relative_to(root).as_posix(),fixture_sha256=hashlib.sha256(fixture.read_bytes()).hexdigest(),labeling=data['labeling'],grading=data['grading'],shard=shard,source_fingerprint=r.fingerprint,index_generation=r.generation.name if r.generation else None,documents=len(r.entries),chunks=len(r.chunks),case_count=len(cases),execution_count=len(rows),elapsed_seconds=round(time.monotonic()-start,2),rows=rows)

def merge(reports):
    first=reports[0];rows=[row for p in reports for row in p['rows']]
    for p in reports:
        if any(p[k]!=first[k] for k in ['fixture_sha256','source_fingerprint','index_generation','documents','chunks']):raise ValueError('incompatible evaluation shards')
    if len({(r['id'],r['engine'],r['scope']) for r in rows})!=len(rows):raise ValueError('duplicate evaluation rows')
    summary={}
    for mode in ENGINES:
        summary[mode]={scope:summarize([r for r in rows if r['engine']==mode and r['scope']==scope]) for scope in ['global','source_assisted']}
    by_category={c:{mode:summarize([r for r in rows if r['engine']==mode and r['scope']=='global' and r['category']==c]) for mode in ENGINES} for c in sorted({r['category'] for r in rows})}
    by_route={route:{mode:summarize([r for r in rows if r['engine']==mode and r['scope']=='global' and r['route']==route]) for mode in ENGINES} for route in ['ads','lp','social','direct']}
    by_language={lang:{mode:summarize([r for r in rows if r['engine']==mode and r['scope']=='global' and r['category']=='pdf_chapter' and r['language']==lang]) for mode in ENGINES} for lang in ['pt','en']}
    return {k:v for k,v in first.items() if k not in {'rows','shard','case_count','execution_count','elapsed_seconds'}}|dict(case_count=len({r['id'] for r in rows}),execution_count=len(rows),shard_elapsed_seconds={p['shard']:p['elapsed_seconds'] for p in reports},summary=summary,by_category=by_category,by_route=by_route,pdf_by_language=by_language,rows=rows)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--fixture',type=Path,default=ROOT/'evals/retrieval/broad-suite-v1.json');p.add_argument('--shard',choices=['catalog','originals','stress']);p.add_argument('--out',type=Path,required=True);a=p.parse_args();report=evaluate(a.fixture,shard=a.shard);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
