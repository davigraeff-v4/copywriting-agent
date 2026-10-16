#!/usr/bin/env python3
"""Check derived public RAG freshness and provenance without importing the model."""
import argparse,json
from pathlib import Path
from rag_corpus import ROOT,public_entries
from rag_config import INDEX_REL
from rag_search import Retriever

def validate_rag(root=ROOT,required=False,body_required=False):
    root=Path(root).resolve();errors=[]
    if not (root/INDEX_REL/'current.json').is_file():
        return dict(status='not_built' if not required else 'failed',errors=['RAG index missing'] if required else [])
    try:
        r=Retriever(root)
        if r.index_error:errors.append('RAG index invalid: '+r.index_error)
        manifest=r.manifest or {}
        from rag_semantic_channel import inspect_channel,CHANNEL_REL
        channel=dict(status='not_built')
        if (root/CHANNEL_REL/'current.json').is_file() and r.manifest:
            try:
                _,body=inspect_channel(root,r.fingerprint,r.chunks,manifest['model_files_sha256'],manifest['files']['chunks.json'])
                channel=dict(status='passed',chunks=body['chunk_count'],dimensions=body['dimensions'],max_tokens=body['max_tokens'])
            except (OSError,ValueError,KeyError,TypeError) as exc:errors.append('Body semantic channel invalid: '+str(exc));channel=dict(status='failed')
        elif body_required:errors.append('Body semantic channel missing')
        if any(d['client']!='*' or (not d.get('extraction_path') and not d['path'].startswith('knowledge/')) for d in r.entries):errors.append('RAG contains non-public source')
        return dict(status='failed' if errors else 'passed',documents=len(r.entries),chunks=manifest.get('chunk_count'),model=manifest.get('model'),dimensions=manifest.get('embedding_dim'),max_chunk_tokens=manifest.get('max_chunk_tokens'),private_documents=manifest.get('private_documents'),semantic_channel=channel,errors=errors)
    except (OSError,ValueError,KeyError,TypeError) as exc:return dict(status='failed',errors=[str(exc)])
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--required',action='store_true');p.add_argument('--body-required',action='store_true');a=p.parse_args();report=validate_rag(required=a.required,body_required=a.body_required);print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(bool(report['errors']))
if __name__=='__main__':main()
