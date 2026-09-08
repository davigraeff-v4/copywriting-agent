#!/usr/bin/env python3
"""Prepare blind copy comparisons and summarize human votes. Does not run a model."""
import argparse
import hashlib
import json
import random
from pathlib import Path


def sha(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()


def prepare(records, seed=20260908):
    groups={}; identities=set()
    for r in records:
        for k in ('case_id','repetition','system','model_id','effort','prompt_sha256','context_sha256','system_prompt_sha256','text'):
            if k not in r or r[k] in ('',None): raise ValueError('Missing '+k)
        identity=(r['case_id'],r['repetition'],r['system'])
        if identity in identities: raise ValueError('Duplicate output')
        identities.add(identity)
        groups.setdefault((r['case_id'],r['repetition']),[]).append(r)
    rng=random.Random(seed); blind=[]; key=[]
    for i,(group,items) in enumerate(sorted(groups.items()),1):
        if len(items)<2: raise ValueError('Each comparison needs at least two systems')
        for k in ('model_id','effort','prompt_sha256','context_sha256'):
            if len({r[k] for r in items})!=1: raise ValueError('Uncontrolled comparison: '+k)
        shuffled=list(items); rng.shuffle(shuffled)
        comparison=f'comparison-{i:03}'
        options=[]
        for j,r in enumerate(shuffled):
            label=chr(65+j); options.append(dict(label=label,text=r['text']))
            metadata={k:v for k,v in r.items() if k!='text'}
            key.append(dict(comparison_id=comparison,label=label,output_sha256=sha(r['text']),metadata=metadata))
        blind.append(dict(comparison_id=comparison,case_id=group[0],repetition=group[1],options=options))
    votes=[dict(comparison_id=b['comparison_id'],rater='',winner='',reason='',hard_failures=[],edit_minutes={}) for b in blind]
    return dict(seed=seed,comparisons=blind),dict(seed=seed,entries=key),votes


def summarize(key,votes):
    entries=key['entries']; mapping={(r['comparison_id'],r['label']):r for r in entries}
    expected={r['comparison_id'] for r in entries}; seen=set(); wins={}; casewins={}; ties=0; failures={}
    for r in entries: wins.setdefault(r['metadata']['system'],0); failures.setdefault(r['metadata']['system'],0)
    for vote in votes:
        cid=vote.get('comparison_id'); winner=vote.get('winner')
        if cid not in expected or cid in seen: raise ValueError('Unknown/duplicate comparison')
        if not vote.get('rater') or not vote.get('reason') or not winner: raise ValueError('Incomplete human evaluation')
        seen.add(cid)
        if winner=='tie': ties+=1
        elif (cid,winner) not in mapping: raise ValueError('Invalid winner')
        else:
            meta=mapping[cid,winner]['metadata']; system=meta['system']; wins[system]+=1
            bycase=casewins.setdefault(meta['case_id'],{}); bycase[system]=bycase.get(system,0)+1
        for fail in vote.get('hard_failures',[]):
            if not isinstance(fail,dict) or (cid,fail.get('label')) not in mapping or not fail.get('reason'): raise ValueError('Invalid failure evidence')
            system=mapping[cid,fail['label']]['metadata']['system']; failures[system]+=1
    total=len(seen)
    return dict(evaluated=total,expected=len(expected),pending=len(expected-seen),ties=ties,wins=wins,
                win_share={s:round(n/total,4) if total else None for s,n in wins.items()},hard_failures=failures,case_wins=casewins,
                limitation='Human preference on this sample only; repetitions of a briefing are not independent clients. No conversion lift inferred.')


def main():
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='command',required=True)
    a=sub.add_parser('prepare'); a.add_argument('records'); a.add_argument('--out',required=True,type=Path); a.add_argument('--seed',type=int,default=20260908)
    a=sub.add_parser('summarize'); a.add_argument('key'); a.add_argument('votes')
    args=p.parse_args()
    if args.command=='prepare':
        blind,key,votes=prepare(json.loads(Path(args.records).read_text()),args.seed)
        args.out.mkdir(parents=True,exist_ok=False)
        for name,data in [('blind.json',blind),('key-private.json',key),('votes.json',votes)]:
            (args.out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps(dict(status='prepared',comparisons=len(blind['comparisons']),directory=str(args.out))))
    else:
        print(json.dumps(summarize(json.loads(Path(args.key).read_text()),json.loads(Path(args.votes).read_text())),ensure_ascii=False,indent=2))

if __name__=='__main__': main()
