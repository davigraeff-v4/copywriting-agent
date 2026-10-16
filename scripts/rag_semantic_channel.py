"""Verified local body-context channel; base chunks and source contents are immutable."""
from __future__ import annotations
import json,os,re,time,uuid
from collections import Counter
from pathlib import Path
from rag_config import MODEL,FASTEMBED_VERSION,DIMENSION,TARGET_TOKENS
from rag_corpus import ROOT,canonical,digest_bytes,source_fingerprint,public_entries
from rag_model import load_model,counting_tokenizer,model_signature
CHANNEL_REL='.local/rag/semantic-channel'

def encoder_hash():return digest_bytes(Path(__file__).read_bytes())

def inputs_for(r,tokenizer):
    inputs=[];repeated={}
    for did,d in r.docs.items():
        counts=Counter(line.strip() for s in r.document_data[did]['segments'] for line in s['text'].splitlines() if line.strip())
        repeated[did]={line for line,n in counts.items() if n>=10 and len(line)<120} if d.get('format')=='.pdf' else set()
    for c in r.chunks:
        data=r.document_data[c['document_id']];parent=next(s for s in data['segments'] if s['id']==c['parent_id'])
        start=max(parent['start_char'],c['start_char']-160);end=min(parent['end_char'],c['end_char']+160)
        text='\n'.join(line for line in data['text'][start:end].splitlines() if line.strip() not in repeated[c['document_id']])
        if len(tokenizer.encode(text).ids)>TARGET_TOKENS:
            start=c['start_char'];lo=c['end_char'];hi=end;best=lo
            while lo<=hi:
                mid=(lo+hi)//2
                if len(tokenizer.encode(data['text'][start:mid]).ids)<=TARGET_TOKENS:best=mid;lo=mid+1
                else:hi=mid-1
            end=best;text=data['text'][start:end]
        text=text.strip() or c['body'];count=len(tokenizer.encode(text).ids)
        if count>TARGET_TOKENS:raise ValueError('body channel exceeds token budget')
        inputs.append(dict(chunk_id=c['id'],document_id=c['document_id'],parent_id=c['parent_id'],start_char=start,end_char=end,text=text,text_sha256=digest_bytes(text.encode()),token_count=count))
    return inputs

def channel_stamp(root):
    try:
        out=Path(root).resolve()/CHANNEL_REL;pointer=out/'current.json';raw=pointer.read_bytes();key=json.loads(raw)['generation']
        if not re.fullmatch(r'[0-9a-f]{16}-[0-9a-f]{8}',key):return None
        folder=(out/key).resolve()
        if not folder.is_relative_to(out.resolve()):return None
        return (digest_bytes(raw),encoder_hash(),tuple((name,(folder/name).stat().st_mtime_ns,(folder/name).stat().st_size) for name in ['manifest.json','inputs.json','vectors.npz']))
    except (OSError,ValueError,KeyError,TypeError):return None

def inspect_channel(root,fingerprint,chunks,signature,base_chunks_sha):
    root=Path(root).resolve();out=root/CHANNEL_REL
    if not out.resolve().is_relative_to(root/'.local'):raise ValueError('body channel outside project derived directory')
    generation=json.loads((out/'current.json').read_text())['generation']
    if not re.fullmatch(r'[0-9a-f]{16}-[0-9a-f]{8}',generation):raise ValueError('invalid body channel pointer')
    folder=(out/generation).resolve()
    if not folder.is_relative_to(out.resolve()):raise ValueError('body channel path escape')
    manifest=json.loads((folder/'manifest.json').read_text())
    if manifest.get('source_fingerprint')!=fingerprint or manifest.get('encoder_hash')!=encoder_hash() or manifest.get('base_chunks_sha256')!=base_chunks_sha:raise ValueError('body channel stale')
    if manifest.get('model')!=MODEL or manifest.get('fastembed_version')!=FASTEMBED_VERSION or manifest.get('model_files_sha256')!=signature or manifest.get('dimensions')!=DIMENSION or manifest.get('private_documents')!=0:raise ValueError('body channel configuration mismatch')
    for name in ['inputs.json','vectors.npz']:
        p=folder/name
        if not p.resolve().is_relative_to(folder) or digest_bytes(p.read_bytes())!=manifest['files'][name]:raise ValueError('body channel artifact corrupt')
    inputs=json.loads((folder/'inputs.json').read_text())
    if len(inputs)!=len(chunks) or manifest.get('chunk_count')!=len(chunks):raise ValueError('body channel row mismatch')
    for c,p in zip(chunks,inputs):
        if p['chunk_id']!=c['id'] or p['document_id']!=c['document_id'] or p['parent_id']!=c['parent_id'] or p['text_sha256']!=digest_bytes(p['text'].encode()) or not 0<p['token_count']<=TARGET_TOKENS or not 0<=p['start_char']<=c['start_char']<c['end_char']<=p['end_char']:raise ValueError('body channel identity mismatch')
    return folder,manifest

def load_channel(root,fingerprint,chunks,signature,base_chunks_sha):
    import numpy as np
    folder,manifest=inspect_channel(root,fingerprint,chunks,signature,base_chunks_sha)
    with np.load(folder/'vectors.npz',allow_pickle=False) as raw:v=raw['vectors'].copy()
    if v.shape!=(len(chunks),DIMENSION) or v.dtype!=np.float32 or not np.isfinite(v).all():raise ValueError('invalid body channel vectors')
    norms=np.linalg.norm(v,axis=1,keepdims=True)
    if (norms<=0).any():raise ValueError('zero body channel vector')
    return v/norms,manifest

def build_channel(root=ROOT,prototype=None):
    # Late import avoids a cycle in the runtime retriever.
    from rag_search import Retriever
    import numpy as np
    root=Path(root).resolve();r=Retriever(root);model=load_model();signature=model_signature(model);tokenizer=counting_tokenizer(model);inputs=inputs_for(r,tokenizer)
    if not r.generation:raise ValueError('valid base index required before semantic channel build')
    out=root/CHANNEL_REL;vectors=None;reused=0
    try:vectors,_=load_channel(root,r.fingerprint,r.chunks,signature,r.manifest['files']['chunks.json']);reused=len(inputs)
    except (OSError,ValueError,KeyError,TypeError):pass
    if vectors is None and prototype:
        prototype=Path(prototype);meta=json.loads((prototype/'body-manifest.json').read_text())
        if meta['source_fingerprint']!=r.fingerprint or meta['model_files_sha256']!=signature or meta['chunk_ids']!=[x['id'] for x in r.chunks] or [x['text_sha256'] for x in meta['locations']]!=[x['text_sha256'] for x in inputs]:raise ValueError('prototype does not match verified semantic inputs')
        with np.load(prototype/'body-vectors.npz',allow_pickle=False) as raw:vectors=raw['vectors'].copy()
        reused=len(inputs)
    if vectors is None:
        texts=[p['text'] for p in inputs];unique=list(dict.fromkeys(texts));lookup={text:i for i,text in enumerate(unique)};rows=[]
        for start in range(0,len(unique),256):
            rows.extend(model.embed(unique[start:start+256],batch_size=32));print(f'body embeddings {len(rows)}/{len(unique)}',flush=True)
        raw=np.asarray(rows,dtype=np.float32);vectors=raw[[lookup[text] for text in texts]]
    if vectors.shape!=(len(inputs),DIMENSION) or vectors.dtype!=np.float32 or not np.isfinite(vectors).all():raise ValueError('invalid generated body vectors')
    norms=np.linalg.norm(vectors,axis=1,keepdims=True)
    if (norms<=0).any():raise ValueError('zero generated body vector')
    vectors/=norms
    if source_fingerprint(public_entries(root),root)!=r.fingerprint:raise ValueError('sources changed during semantic channel build')
    out.mkdir(parents=True,exist_ok=True);generation=r.fingerprint[:16]+'-'+uuid.uuid4().hex[:8];folder=out/('.building-'+uuid.uuid4().hex);folder.mkdir()
    (folder/'inputs.json').write_bytes(canonical(inputs));np.savez_compressed(folder/'vectors.npz',vectors=vectors)
    manifest=dict(schema=1,model=MODEL,fastembed_version=FASTEMBED_VERSION,dimensions=DIMENSION,source_fingerprint=r.fingerprint,base_chunks_sha256=r.manifest['files']['chunks.json'],encoder_hash=encoder_hash(),model_files_sha256=signature,chunk_count=len(inputs),max_tokens=max(p['token_count'] for p in inputs),private_documents=0,remote_embedding_calls=0,reused_embeddings=reused,files={name:digest_bytes((folder/name).read_bytes()) for name in ['inputs.json','vectors.npz']},built_at=time.strftime('%Y-%m-%dT%H:%M:%S%z'))
    (folder/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');folder.rename(out/generation)
    pointer=out/('.current-'+uuid.uuid4().hex);pointer.write_text(json.dumps(dict(generation=generation))+'\n');os.replace(pointer,out/'current.json')
    return manifest
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--reuse-prototype',type=Path);a=p.parse_args();print(json.dumps(build_channel(prototype=a.reuse_prototype),indent=2))
