#!/usr/bin/env python3
"""Read a complete indexed page or section, with source identity and data boundaries."""
import argparse,json
from rag_corpus import ROOT,public_entries,document_data
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--id',required=True);p.add_argument('--page',type=int);p.add_argument('--section');p.add_argument('--max-chars',type=int,default=0);a=p.parse_args()
 if a.max_chars<0 or (a.page is not None and a.page<1):p.error('page must be positive; max-chars must be nonnegative')
 entry=next((e for e in public_entries() if e['id']==a.id),None)
 if not entry:p.error('unknown source')
 data=document_data(entry);segments=[s for s in data['segments'] if (a.page is None or s.get('page')==a.page) and (not a.section or a.section.casefold() in s['section'].casefold())]
 if not segments:p.error('page/section not found; no substitute source was selected')
 text='\n\n'.join(s['text'] for s in segments)
 print(json.dumps(dict(id=entry['id'],source=entry['path'],sha256=entry['sha256'],reference_data_only=True,page=a.page,sections=[s['section'] for s in segments],text=text[:a.max_chars] if a.max_chars else text,truncated=bool(a.max_chars and len(text)>a.max_chars)),ensure_ascii=False,indent=2))
