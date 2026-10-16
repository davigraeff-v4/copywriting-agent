#!/usr/bin/env python3
"""Validate curated repertoire integrity and attribution; not editorial scoring."""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
ROUTES={'ads','lp','social','direct'}
BATCHES={
    'lote-01': {'units':60,'sources':50,'kinds':Counter(metodo=20,exemplo=30,revisao=10)},
    'lote-02': {'units':40,'sources':40,'kinds':Counter(exemplo=40)},
}
COMPLETE_SCOPES={
    'single_static_creative':'observed_static_creative',
    'commercial_page_text':'observed_commercial_page',
    'archived_email':'observed_archived_email',
}

def validate_repertoire(root=ROOT):
    root=Path(root).resolve();base=root/'knowledge/repertorio';errors=[]
    try:
        entries=json.loads((base/'catalogo.json').read_text())
        sources=json.loads((base/'fontes.json').read_text())
        if not isinstance(entries,list) or not isinstance(sources,list):
            raise ValueError('catalog and sources must be lists')
    except (OSError,ValueError) as exc:
        return {'status':'failed','errors':[str(exc)]}
    ids=set();paths=set();hashes=set();source_map={};kinds=Counter();routes=Counter()
    source_urls=set();batch_units=Counter();batch_sources=Counter();batch_kinds={b:Counter() for b in BATCHES}
    complete_scopes=Counter();quotes_by_source=Counter()
    for s in sources:
        if not isinstance(s,dict):errors.append('invalid source record');continue
        sid=s.get('id');u=urlparse(s.get('url',''))
        if not sid or sid in source_map:errors.append('missing/duplicate source id '+str(sid))
        source_map[sid]=s
        url=s.get('url','')
        if url in source_urls:errors.append('duplicate external source URL '+str(sid))
        source_urls.add(url)
        batch_sources[s.get('batch','lote-01')]+=1
        if u.scheme!='https' or not u.hostname or u.username or u.password:errors.append('invalid HTTPS source '+str(sid))
        if u.hostname!=s.get('publisher_domain'):errors.append('source domain mismatch '+str(sid))
        if s.get('verified') is not True or not s.get('accessed_at') or not s.get('locator') or not s.get('rights'):errors.append('incomplete provenance '+str(sid))
        if s.get('security_flags')!=[] or s.get('security_review') not in {'manual_scope_review_and_heuristic_scan','manual_visible_text_scope_review','pdf_static_and_extracted_text_review'} or not s.get('security_scope'):errors.append('source security review missing/flagged '+str(sid))
        if s.get('not_client_evidence') is not True:errors.append('source not isolated '+str(sid))
    for item in entries:
        if not isinstance(item,dict):errors.append('invalid unit record');continue
        sid=item.get('id');kind=item.get('kind');primary=item.get('primary_route');rel=item.get('path','')
        if not sid or sid in ids:errors.append('missing/duplicate unit id '+str(sid))
        ids.add(sid)
        path=(root/rel).resolve()
        if path in paths:errors.append('duplicate indexed file '+str(sid))
        paths.add(path)
        if not path.is_relative_to(base) or path.suffix!='.md' or not path.is_file():
            errors.append('missing/outside repertoire path '+str(sid));continue
        content=path.read_text();digest=hashlib.sha256(path.read_bytes()).hexdigest()
        if digest!=item.get('sha256'):errors.append('content hash mismatch '+str(sid))
        if digest in hashes:errors.append('duplicate content '+str(sid))
        hashes.add(digest)
        if kind not in {'metodo','exemplo','revisao'}:errors.append('invalid kind '+str(sid))
        kinds[kind]+=1;routes[primary]+=1
        batch=item.get('batch')
        batch_units[batch]+=1
        if batch in batch_kinds:batch_kinds[batch][kind]+=1
        declared=item.get('routes',[])
        if primary not in ROUTES or primary not in declared or not set(declared)<=ROUTES:errors.append('invalid routes '+str(sid))
        if item.get('client')!='*' or item.get('authority')!='referencia_de_mercado':errors.append('invalid global scope/authority '+str(sid))
        if item.get('status')!='active' or item.get('editorial_review')!='agent_curated_human_review_pending':errors.append('invalid study status '+str(sid))
        if item.get('human_approved') is not False or item.get('performance_verified') is not False:errors.append('unearned approval/performance '+str(sid))
        if item.get('use')!={'metodo':'guidance','exemplo':'positive','revisao':'structure'}.get(kind):errors.append('invalid retrieval use '+str(sid))
        if not item.get('summary') or not item.get('tags'):errors.append('missing search metadata '+str(sid))
        if not item.get('source_ids') or any(i not in source_map for i in item.get('source_ids',[])):errors.append('missing source '+str(sid))
        for heading in ['## Critério de revisão','## Limites de uso','## Proveniência']:
            if heading not in content:errors.append('missing section '+str(sid)+' '+heading)
        try:
            body=content[content.index('##'):content.index('\n## Limites de uso')]
            n=len(re.findall(r'\S+',body))
            if n<180 or n!=item.get('body_word_count'):errors.append('thin/inconsistent body '+str(sid))
        except ValueError:errors.append('cannot locate unit body '+str(sid))
        if len(re.findall(r'\S+',content))!=item.get('word_count'):errors.append('word count mismatch '+str(sid))
        quotes=' '.join(line[2:] for line in content.splitlines() if line.startswith('> '))
        quoted=len(re.findall(r'\S+',quotes))
        if quoted>25 or quoted!=item.get('quoted_words'):errors.append('quote budget mismatch '+str(sid))
        for source_id in item.get('source_ids',[]):quotes_by_source[source_id]+=quoted
        if kind=='revisao':
            if item.get('synthetic') is not True or 'Exercício sintético criado pelo Codex' not in content:errors.append('unlabeled synthetic revision '+str(sid))
            for h in ['## Briefing e fatos fictícios','## Antes:','## Depois:','## Diagnóstico editorial']:
                if h not in content:errors.append('incomplete revision '+str(sid))
        elif item.get('synthetic') is not False:errors.append('wrong provenance type '+str(sid))
        if batch not in BATCHES:errors.append('unexpected batch '+str(sid))
        if batch=='lote-02':
            scope=item.get('completeness_scope');complete_scopes[scope]+=1
            if item.get('complete_piece') is not True or scope not in COMPLETE_SCOPES:
                errors.append('incomplete/unknown piece scope '+str(sid))
            if item.get('evidence_kind')!=COMPLETE_SCOPES.get(scope) or not item.get('format'):
                errors.append('inconsistent piece evidence '+str(sid))
            components=item.get('components',[])
            if not isinstance(components,list) or len(components)<3 or any(not isinstance(c,str) or not c.strip() for c in components):
                errors.append('incomplete component map '+str(sid))
            elif len(components)!=item.get('component_count') or any(f'{i}. {c}' not in content for i,c in enumerate(components,1)):
                errors.append('component map mismatch '+str(sid))
            try:
                observed=content.split('## Mapa completo da peça\n\n',1)[1].split('\n## Aplicação autoral ao processo',1)[0]
                limits=content.split('## Limites de uso\n\n',1)[1].split('\n\nA fonte ensina',1)[0]
                # Includes headings and ordinal numbers as a conservative derivation count.
                source_words=len(re.findall(r'\S+',observed+' '+limits+' '+quotes))
                declared_words=item.get('source_specific_word_count',0)
                if not isinstance(declared_words,int) or not 0<declared_words<=200 or source_words>200 or source_words!=declared_words:
                    errors.append('source derivation budget exceeded '+str(sid))
            except (IndexError,TypeError):errors.append('missing observation/analysis boundaries '+str(sid))
            if item.get('independent_delivery_verified') is not False:
                errors.append('unearned independent delivery '+str(sid))
            for source_id in item.get('source_ids',[]):
                source=source_map.get(source_id,{})
                if source.get('batch')!=batch or source.get('completeness_scope')!=scope or source.get('independent_delivery_verified') is not False:
                    errors.append('piece provenance mismatch '+str(sid))
                if scope in {'single_static_creative','archived_email'}:
                    asset=urlparse(source.get('observed_asset_url',''))
                    if asset.scheme!='https' or not asset.hostname or asset.username or asset.password:
                        errors.append('missing observed integral asset '+str(sid))
            for heading in ['## Peça observada e escopo','## Mapa completo da peça','## Argumento e progressão','## Voz e execução','## Evidência e fragilidades','## Aplicação autoral ao processo']:
                if heading not in content:errors.append('missing complete study section '+str(sid)+' '+heading)
    for batch,spec in BATCHES.items():
        if batch_units[batch]!=spec['units'] or batch_sources[batch]!=spec['sources'] or batch_kinds[batch]!=spec['kinds']:
            errors.append('batch composition mismatch '+batch)
    if set(batch_sources)-set(BATCHES):errors.append('unexpected source batch')
    if complete_scopes!=Counter(single_static_creative=20,commercial_page_text=12,archived_email=8):errors.append('complete piece coverage mismatch')
    if any(n>25 for n in quotes_by_source.values()):errors.append('aggregate source quote budget exceeded')
    if set(routes)!=ROUTES or routes['ads']+routes['lp']<=len(entries)/2:errors.append('route coverage/priority mismatch')
    used={s for i in entries if isinstance(i,dict) for s in i.get('source_ids',[])}
    if used!=set(source_map):errors.append('unreferenced/missing source records')
    return dict(status='failed' if errors else 'passed',units=len(entries),sources=len(sources),by_kind=dict(kinds),by_primary_route=dict(routes),by_batch=dict(batch_units),complete_piece_scopes=dict(complete_scopes),errors=errors)

if __name__=='__main__':
    report=validate_repertoire();print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(bool(report['errors']))
