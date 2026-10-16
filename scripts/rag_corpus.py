"""Allowlisted public corpus and section/offset chunking. Standard library only."""
from __future__ import annotations
import hashlib,json,re,unicodedata
from pathlib import Path
from rag_config import EXTRA_KNOWLEDGE,LEXICAL_WORDS,MAX_WORDS,OVERLAP_WORDS,TARGET_TOKENS,SCHEMA_VERSION
ROOT=Path(__file__).resolve().parents[1]
ROUTES={'ads','lp','social','direct'}
DENIED={'.local','evals','clients','campaigns','outputs','examples','history','.git'}
STOP=set('a ao aos as o os e ou de da das do dos um uma uns umas em no na nos nas por para com como que se sua seu suas seus esse essa isso isto este esta estes estas meu minha mais muito qual quais quanto quando onde porque pois ser são foi são tem têm ter fazer faz pode podem sobre também não sem pelo pela pelos pelas até apenas então cada entre já mesmo toda todo todas todos'.split())
STOP={''.join(c for c in unicodedata.normalize('NFD',w) if not unicodedata.combining(c)) for w in STOP}

def digest_bytes(raw):return hashlib.sha256(raw).hexdigest()
def canonical(value):return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def tokens(text):
    text=''.join(c for c in unicodedata.normalize('NFD',text.casefold()) if not unicodedata.combining(c))
    return [w for w in re.findall(r'\w{2,}',text) if w not in STOP]

def public_path(root,relative):
    root=Path(root).resolve();rel=Path(relative)
    if rel.is_absolute() or rel.parts[:1]!=('knowledge',) or any(p in DENIED or p.startswith('.') or p=='..' for p in rel.parts):
        raise ValueError('public RAG path outside allowlist')
    p=(root/rel).resolve()
    if not p.is_relative_to(root/'knowledge') or p.suffix!='.md' or not p.is_file():raise ValueError('missing/outside public RAG source')
    return p

def public_entries(root=ROOT):
    root=Path(root).resolve()
    core=json.loads((root/'knowledge/retrieval-index.json').read_text())
    for slug,(summary,tags) in EXTRA_KNOWLEDGE.items():
        path=f'knowledge/{slug}.md'
        if not any(i['path']==path for i in core):
            core.append(dict(id=slug,path=path,client='*',routes=['lp'] if slug=='narrativa-lp' else sorted(ROUTES),tags=tags.split(),status='active',use='guidance',summary=summary))
    repertoire=root/'knowledge/repertorio/catalogo.json'
    studies=json.loads(repertoire.read_text()) if repertoire.is_file() else []
    sources_path=root/'knowledge/repertorio/fontes.json'
    sources={s['id']:s for s in json.loads(sources_path.read_text())} if sources_path.is_file() else {}
    excluded={'README.md','VALIDACAO.md','RAG-RELATORIO.md','INGESTAO-RELATORIO.md'}
    known={i['path'] for i in core+studies}
    for path in sorted((root/'knowledge').rglob('*.md')):
        relative=path.relative_to(root).as_posix()
        if relative not in known and path.name not in excluded:
            core.append(dict(id='kb-'+digest_bytes(relative.encode())[:16],path=relative,client='*',routes=sorted(ROUTES),tags=['documento','metodologia'],status='active',use='guidance',summary=path.stem))
    entries=[];ids=set();paths=set()
    for item in core+studies:
        item=dict(item)
        if item.get('client')!='*':raise ValueError('public corpus cannot include private entries')
        if item.get('status')!='active':continue
        if item.get('id') in ids or item.get('path') in paths:raise ValueError('duplicate public corpus identity/path')
        if not item.get('routes') or not set(item['routes'])<=ROUTES:raise ValueError('invalid public route')
        if item.get('use') not in {'guidance','positive','negative','structure'}:raise ValueError('invalid public use')
        p=public_path(root,item['path']);raw=p.read_bytes()
        if item in studies or item.get('batch'):
            if digest_bytes(raw)!=item.get('sha256'):raise ValueError('curated source hash mismatch')
            for sid in item.get('source_ids',[]):
                source=sources.get(sid,{})
                if source.get('security_flags')!=[] or source.get('not_client_evidence') is not True or source.get('verified') is not True:
                    raise ValueError('unsafe/unisolated public source')
            if not item.get('source_ids'):raise ValueError('missing curated provenance')
            item['source_urls']=[sources[s]['url'] for s in item['source_ids']]
        else:
            item.update(authority='local_methodology',evidence_kind='local_guidance_with_historical_examples',human_approved=False,performance_verified=False,synthetic=False,source_ids=[],source_urls=[])
        item['sha256']=digest_bytes(raw)
        item['title']=next((l.lstrip('# ').strip() for l in raw.decode().splitlines() if l.startswith('# ')),item['summary'])
        ids.add(item['id']);paths.add(item['path']);entries.append(item)
    from rag_ingest import load_registry
    originals,_=load_registry(root)
    for item in originals:
        if item['id'] in ids or item['path'] in paths:raise ValueError('duplicate original identity')
        ids.add(item['id']);paths.add(item['path']);entries.append(item)
    return entries

def document_data(entry,root=ROOT):
    if entry.get('extraction_path'):
        from rag_ingest import extraction
        return extraction(entry,root)
    source=public_path(root,entry['path']);raw=source.read_bytes()
    if entry.get('sha256') and digest_bytes(raw)!=entry['sha256']:raise ValueError('source changed before chunking')
    text=raw.decode('utf-8').replace('\r\n','\n').replace('\r','\n')
    segments=[]
    matches=list(re.finditer(r'^##\s+(.+?)\s*$',text,re.M))
    starts=[0]+[m.start() for m in matches if m.start()>0]
    labels=['Apresentação']+[m.group(1) for m in matches if m.start()>0]
    for i,(a,b) in enumerate(zip(starts,starts[1:]+[len(text)])):
        segments.append(dict(id=f's{i:05d}',text=text[a:b],section=labels[i],start_char=a,end_char=b,page=None))
    return dict(text=text,segments=segments)

def source_fingerprint(entries,root=ROOT):
    records=[]
    for item in sorted(entries,key=lambda i:i['id']):
        if item.get('extraction_path'):
            from rag_ingest import safe_original
            p=safe_original(root,item['path'])
        else:p=public_path(root,item['path'])
        if digest_bytes(p.read_bytes())!=item['sha256']:raise ValueError('source changed during RAG operation')
        records.append(item)
    return digest_bytes(canonical({'schema':SCHEMA_VERSION,'entries':records}))

def sections(raw):
    matches=list(re.finditer(r'^##\s+(.+?)\s*$',raw,re.M))
    if not matches:
        first=re.search(r'^# .*$',raw,re.M);start=first.end() if first else 0
        return [('Texto',start,len(raw))]
    return [(m.group(1),m.end(),matches[i+1].start() if i+1<len(matches) else len(raw)) for i,m in enumerate(matches)]

def prefix(entry,section):
    # Long labels must not consume the model's entire input window.
    return ' '.join(entry['title'].split()[:18])+'\n'+ ' '.join(section.split()[:12])+'\n\n'

def make_chunks(entries,root=ROOT,token_count=None):
    chunks=[]
    for entry in sorted(entries,key=lambda e:e['id']):
        data=document_data(entry,root);raw=data['text'];idx=0
        for segment in data['segments']:
            section=segment['section'];a=segment['start_char'];end=segment['end_char']
            while a<end:
                while a<end and raw[a].isspace():a+=1
                if a>=end:break
                maximum=min(end,a+(1800 if token_count else 420))
                if token_count:
                    lo=a+1;hi=maximum;best=None
                    while lo<=hi:
                        mid=(lo+hi)//2
                        if token_count(prefix(entry,section)+raw[a:mid])<=TARGET_TOKENS:best=mid;lo=mid+1
                        else:hi=mid-1
                    if best is None:raise ValueError('context exceeds token budget')
                    maximum=best
                b=maximum
                if b<end:
                    boundary=max(raw.rfind(' ',a,b),raw.rfind('\n',a,b))
                    if boundary>a+max(20,(b-a)//2):b=boundary
                body=raw[a:b];text=prefix(entry,section)+body
                chunk=dict(id=f"{entry['id']}:{idx:04d}",document_id=entry['id'],path=entry['path'],section=section,start_char=a,end_char=b,line_start=raw.count('\n',0,a)+1,line_end=raw.count('\n',0,b)+1,text=text,body=body,token_count=token_count(text) if token_count else None,parent_id=segment['id'],page=segment.get('page'),chapter_number=segment.get('chapter_number'),extraction_path=entry.get('extraction_path'))
                chunks.append(chunk);idx+=1
                if b>=end:break
                # Eight complete words of overlap; a long token can still be split safely.
                words=list(re.finditer(r'\S+',raw[a:b]))
                next_a=a+words[-OVERLAP_WORDS].start() if len(words)>OVERLAP_WORDS else b
                a=max(a+1,next_a)
    return chunks
