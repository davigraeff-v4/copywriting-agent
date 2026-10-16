#!/usr/bin/env python3
"""Build public copy chunks and local embeddings, with atomic generation switching."""
from __future__ import annotations
import argparse,json,os,re,shutil,time,uuid
from pathlib import Path
from rag_config import MODEL,FASTEMBED_VERSION,DIMENSION,MAX_TOKENS,TARGET_TOKENS,MAX_WORDS,OVERLAP_WORDS,SCHEMA_VERSION,INDEX_REL
from rag_corpus import ROOT,public_entries,source_fingerprint,make_chunks,digest_bytes,canonical
from rag_model import load_model,counting_tokenizer,model_signature

def pipeline_hash(root=ROOT):
    names=['rag_config.py','rag_corpus.py','rag_model.py','rag_ingest.py','build_rag_index.py']
    return digest_bytes(b''.join((Path(root)/'scripts'/n).read_bytes() for n in names))

def reusable_vectors(out,signature):
    """Reuse only identical embedding input with verified, identical model files."""
    import numpy as np
    try:
        generation=json.loads((out/'current.json').read_text())['generation']
        if not re.fullmatch(r'[0-9a-f]{16}-[0-9a-f]{8}',generation):return {}
        folder=(out/generation).resolve()
        if not folder.is_relative_to(out.resolve()):return {}
        manifest=json.loads((folder/'manifest.json').read_text())
        if manifest.get('model')!=MODEL or manifest.get('fastembed_version')!=FASTEMBED_VERSION or manifest.get('embedding_dim')!=DIMENSION or manifest.get('model_files_sha256')!=signature or manifest.get('public_only') is not True or manifest.get('private_documents')!=0:return {}
        for name in ['chunks.json','vectors.npz']:
            p=folder/name
            if not p.resolve().is_relative_to(folder) or digest_bytes(p.read_bytes())!=manifest['files'][name]:return {}
        chunks=json.loads((folder/'chunks.json').read_text())['chunks']
        with np.load(folder/'vectors.npz',allow_pickle=False) as payload:vectors=payload['vectors'].copy()
        if vectors.shape!=(len(chunks),DIMENSION) or vectors.dtype!=np.float32 or not np.isfinite(vectors).all() or (np.linalg.norm(vectors,axis=1)<=0).any():return {}
        return {digest_bytes(c['text'].encode()):vectors[i] for i,c in enumerate(chunks)}
    except (OSError,ValueError,TypeError,KeyError):return {}

def build(root=ROOT,cache_dir=None,index_dir=None):
    root=Path(root).resolve();out=Path(index_dir) if index_dir else root/INDEX_REL
    if not out.resolve().is_relative_to(root/'.local'):raise ValueError('derived RAG artifacts must remain in project .local/')
    entries=public_entries(root);fingerprint=source_fingerprint(entries,root);current_pipeline=pipeline_hash(root)
    model=load_model(cache_dir);tokenizer=counting_tokenizer(model)
    chunks=make_chunks(entries,root,lambda text:len(tokenizer.encode(text).ids))
    if not chunks:raise ValueError('empty public corpus')
    print(f"{len(entries)} documents -> {len(chunks)} chunks; generating local embeddings",flush=True)
    import numpy as np
    texts=[c['text'] for c in chunks]
    signature=model_signature(model);previous=reusable_vectors(out,signature)
    vectors=np.empty((len(texts),DIMENSION),dtype=np.float32);missing=[]
    for i,text in enumerate(texts):
        cached=previous.get(digest_bytes(text.encode()))
        if cached is None:missing.append(i)
        else:vectors[i]=cached
    print(f'reusing {len(texts)-len(missing)} verified embeddings; generating {len(missing)}',flush=True)
    for start in range(0,len(missing),256):
        positions=missing[start:start+256]
        generated=np.asarray(list(model.embed([texts[i] for i in positions],batch_size=32)),dtype=np.float32)
        if generated.shape!=(len(positions),DIMENSION):raise ValueError('invalid generated batch')
        vectors[positions]=generated
        print(f'new embeddings {min(start+256,len(missing))}/{len(missing)}',flush=True)
    if vectors.shape!=(len(chunks),DIMENSION) or not np.isfinite(vectors).all():raise ValueError('invalid generated vectors')
    norms=np.linalg.norm(vectors,axis=1,keepdims=True)
    if (norms<=0).any():raise ValueError('zero generated vector')
    vectors/=norms
    # Refuse source changes that happened while embedding.
    if source_fingerprint(public_entries(root),root)!=fingerprint:raise ValueError('sources changed during build')
    if pipeline_hash(root)!=current_pipeline:raise ValueError('chunk pipeline changed during build')
    out.mkdir(parents=True,exist_ok=True)
    generation=fingerprint[:16]+'-'+uuid.uuid4().hex[:8]
    temp=out/('.building-'+uuid.uuid4().hex);temp.mkdir()
    try:
        payload={'documents':entries,'chunks':chunks}
        (temp/'chunks.json').write_bytes(canonical(payload))
        np.savez_compressed(temp/'vectors.npz',vectors=vectors)
        manifest=dict(schema_version=SCHEMA_VERSION,model=MODEL,fastembed_version=FASTEMBED_VERSION,embedding_dim=DIMENSION,token_limit=MAX_TOKENS,target_tokens=TARGET_TOKENS,max_chunk_tokens=max(c['token_count'] for c in chunks),max_words=MAX_WORDS,overlap_words=OVERLAP_WORDS,source_fingerprint=fingerprint,pipeline_hash=current_pipeline,document_count=len(entries),chunk_count=len(chunks),built_at=time.strftime('%Y-%m-%dT%H:%M:%S%z'),public_only=True,private_documents=0,remote_embedding_calls=0,files={p.name:digest_bytes(p.read_bytes()) for p in temp.iterdir()})
        manifest['model_files_sha256']=signature
        manifest['reused_embeddings']=len(texts)-len(missing);manifest['generated_embeddings']=len(missing)
        (temp/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
        temp.rename(out/generation)
        pointer=out/('.current-'+uuid.uuid4().hex+'.json');pointer.write_text(json.dumps({'generation':generation})+'\n');os.replace(pointer,out/'current.json')
    except BaseException:
        if temp.exists():shutil.rmtree(temp)
        raise
    return manifest

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--cache-dir',type=Path);a=p.parse_args()
    report=build(cache_dir=a.cache_dir)
    from rag_semantic_channel import build_channel
    report['semantic_channel']=build_channel()
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
