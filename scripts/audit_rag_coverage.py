#!/usr/bin/env python3
"""Measure indexed coverage of extracted content, without asserting perfect OCR."""
import argparse,json
from collections import Counter,defaultdict
from pathlib import Path
from rag_corpus import ROOT,document_data,digest_bytes
from rag_config import INDEX_REL

def audit(root=ROOT):
 root=Path(root).resolve();idx=root/INDEX_REL;gen=json.loads((idx/'current.json').read_text())['generation'];payload=json.loads((idx/gen/'chunks.json').read_text())
 grouped=defaultdict(list)
 for c in payload['chunks']:grouped[c['document_id']].append(c)
 rows=[];errors=[]
 for d in payload['documents']:
  data=document_data(d,root);text=data['text'];intervals=sorted((c['start_char'],c['end_char']) for c in grouped[d['id']]);merged=[]
  for a,b in intervals:
   if merged and a<=merged[-1][1]:merged[-1][1]=max(merged[-1][1],b)
   else:merged.append([a,b])
  gaps=[];last=0
  for a,b in merged:
   if text[last:a].strip():gaps.append([last,a])
   last=b
  if text[last:].strip():gaps.append([last,len(text)])
  missing=sum(sum(not char.isspace() for char in text[a:b]) for a,b in gaps);total=sum(not char.isspace() for char in text)
  pages={s['page'] for s in data['segments'] if s.get('page') is not None and s['text'].strip()};indexed_pages={c['page'] for c in grouped[d['id']] if c.get('page') is not None}
  if missing or pages-indexed_pages:errors.append(d['id'])
  rows.append(dict(id=d['id'],path=d['path'],format=Path(d['path']).suffix.lower(),chunks=len(grouped[d['id']]),extracted_nonwhitespace_characters=total,missing_nonwhitespace_characters=missing,coverage=1-missing/max(total,1),source_segments=len(data['segments']),pages_with_text=sorted(pages),indexed_pages=sorted(indexed_pages),quality=d.get('quality',{}),fidelity='Coverage is over extracted text/observed descriptions; not proof of exact OCR or full visual semantics.'))
 return dict(status='passed' if not errors else 'failed',documents=len(rows),chunks=len(payload['chunks']),by_format=dict(Counter(r['format'] for r in rows)),all_extracted_text_indexed=not errors,errors=errors,rows=rows)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path);a=p.parse_args();report=audit()
 if a.out:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k!='rows'},ensure_ascii=False,indent=2));raise SystemExit(bool(report['errors']))
