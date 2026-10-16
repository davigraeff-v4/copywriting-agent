#!/usr/bin/env python3
"""Prepare blind copy comparisons and summarize human votes. Does not run a model."""
import argparse
import hashlib
import json
import math
import random
import statistics
from pathlib import Path

ROUTES = {'lp', 'ads', 'social', 'direct'}
DIMENSIONS = ('argumento', 'especificidade', 'voz', 'progressao', 'portugues', 'utilidade')
STAGES = {'contexto_evidencia', 'recuperacao', 'direcao', 'escrita', 'revisao', 'indeterminada'}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def measured(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0


def aggregate(values):
    return dict(n=len(values), mean=round(statistics.mean(values), 4) if values else None,
                median=round(statistics.median(values), 4) if values else None)


def sha(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()


def prepare(records, seed=20260908):
    if not isinstance(records, list) or not records: raise ValueError('Expected non-empty output list')
    groups={}; identities=set()
    for r in records:
        for k in ('case_id','repetition','system','model_id','effort','prompt_sha256','context_sha256','system_prompt_sha256','text'):
            if k not in r or r[k] in ('',None): raise ValueError('Missing '+k)
        for k in ('case_id','system','model_id','effort','prompt_sha256','context_sha256','system_prompt_sha256','text'):
            if not nonempty(r[k]): raise ValueError('Invalid '+k)
        if type(r['repetition']) is not int or r['repetition'] < 1: raise ValueError('Invalid repetition')
        if 'route' in r or 'briefing' in r:
            if r.get('route') not in ROUTES or not nonempty(r.get('briefing')):
                raise ValueError('route and briefing must be supplied together')
        identity=(r['case_id'],r['repetition'],r['system'])
        if identity in identities: raise ValueError('Duplicate output')
        identities.add(identity)
        groups.setdefault((r['case_id'],r['repetition']),[]).append(r)
    rng=random.Random(seed); blind=[]; key=[]; expected_systems=None
    for i,(group,items) in enumerate(sorted(groups.items()),1):
        if not 2 <= len(items) <= 26: raise ValueError('Each comparison needs two to 26 systems')
        systems={r['system'] for r in items}
        if expected_systems is None: expected_systems=systems
        elif systems != expected_systems: raise ValueError('Missing/different systems across comparisons')
        for k in ('model_id','effort','prompt_sha256','context_sha256'):
            if len({r[k] for r in items})!=1: raise ValueError('Uncontrolled comparison: '+k)
        for k in ('route', 'briefing'):
            if len({r.get(k) for r in items}) != 1: raise ValueError('Uncontrolled comparison: '+k)
        shuffled=list(items); rng.shuffle(shuffled)
        comparison=f'comparison-{i:03}'
        options=[]
        for j,r in enumerate(shuffled):
            label=chr(65+j); options.append(dict(label=label,text=r['text']))
            metadata={k:v for k,v in r.items() if k!='text'}
            key.append(dict(comparison_id=comparison,label=label,output_sha256=sha(r['text']),metadata=metadata))
        row=dict(comparison_id=comparison,case_id=group[0],repetition=group[1],options=options)
        if 'briefing' in items[0]: row.update(briefing=items[0]['briefing'],route=items[0]['route'])
        blind.append(row)
    votes=[dict(comparison_id=b['comparison_id'],rater='',winner='',reason='',hard_failures=[],edit_minutes={},
                assessments={},diagnoses={}) for b in blind]
    return dict(seed=seed,comparisons=blind),dict(seed=seed,entries=key),votes


def summarize(key,votes):
    entries=key['entries']; mapping={(r['comparison_id'],r['label']):r for r in entries}
    expected={r['comparison_id'] for r in entries}; seen=set(); wins={}; casewins={}; ties=0; failures={}
    minutes={}; ratings={}; diagnoses={}; routes={}
    for r in entries:
        system=r['metadata']['system']; wins.setdefault(system,0); failures.setdefault(system,0)
        minutes.setdefault(system,[]); ratings.setdefault(system,{d:[] for d in DIMENSIONS}); diagnoses.setdefault(system,{})
        route=r['metadata'].get('route','unspecified')
        routes.setdefault(route,dict(expected=set(),evaluated=0,ties=0,wins={}))
        routes[route]['expected'].add(r['comparison_id']); routes[route]['wins'].setdefault(system,0)
    for vote in votes:
        cid=vote.get('comparison_id'); winner=vote.get('winner')
        if cid not in expected or cid in seen: raise ValueError('Unknown/duplicate comparison')
        if not nonempty(vote.get('rater')) or not nonempty(vote.get('reason')) or not winner: raise ValueError('Incomplete human evaluation')
        seen.add(cid)
        first=next(r for r in entries if r['comparison_id']==cid)
        route=first['metadata'].get('route','unspecified'); routes[route]['evaluated']+=1
        if winner=='tie': ties+=1
        elif (cid,winner) not in mapping: raise ValueError('Invalid winner')
        else:
            meta=mapping[cid,winner]['metadata']; system=meta['system']; wins[system]+=1
            routes[route]['wins'][system]+=1
            bycase=casewins.setdefault(meta['case_id'],{}); bycase[system]=bycase.get(system,0)+1
        if winner=='tie': routes[route]['ties']+=1
        for fail in vote.get('hard_failures',[]):
            if not isinstance(fail,dict) or (cid,fail.get('label')) not in mapping or not fail.get('reason'): raise ValueError('Invalid failure evidence')
            system=mapping[cid,fail['label']]['metadata']['system']; failures[system]+=1
        for group in ('edit_minutes','assessments','diagnoses'):
            values=vote.get(group,{})
            if not isinstance(values,dict): raise ValueError('Invalid '+group)
            for label,value in values.items():
                if (cid,label) not in mapping: raise ValueError('Invalid label in '+group)
                system=mapping[cid,label]['metadata']['system']
                if group=='edit_minutes':
                    if not measured(value): raise ValueError('Invalid edit minutes')
                    minutes[system].append(value)
                elif group=='assessments':
                    if not isinstance(value,dict) or not value or set(value)-set(DIMENSIONS): raise ValueError('Invalid assessment dimensions')
                    for dimension,item in value.items():
                        if (not isinstance(item,dict) or type(item.get('score')) is not int
                                or not 1 <= item['score'] <= 5 or not nonempty(item.get('quote'))
                                or not nonempty(item.get('reason'))): raise ValueError('Invalid human assessment evidence')
                        ratings[system][dimension].append(item['score'])
                else:
                    if not isinstance(value,dict) or value.get('stage') not in STAGES or not nonempty(value.get('reason')):
                        raise ValueError('Invalid failure diagnosis')
                    stage=value['stage']; diagnoses[system][stage]=diagnoses[system].get(stage,0)+1
    total=len(seen)
    byroute={}
    for route,row in routes.items():
        n=row['evaluated']
        byroute[route]=dict(expected=len(row['expected']),evaluated=n,pending=len(row['expected'])-n,
                           ties=row['ties'],wins=row['wins'],win_share={s:round(v/n,4) if n else None for s,v in row['wins'].items()})
    return dict(evaluated=total,expected=len(expected),pending=len(expected-seen),ties=ties,wins=wins,
                win_share={s:round(n/total,4) if total else None for s,n in wins.items()},hard_failures=failures,case_wins=casewins,
                by_route=byroute,edit_minutes={s:aggregate(v) for s,v in minutes.items()},
                human_assessments={s:{d:aggregate(v) for d,v in dims.items()} for s,dims in ratings.items()},
                failure_stage_reports=diagnoses,
                limitation='Human preference on this sample only; repetitions are not independent clients. Missing measurements are not zero. Ratings and diagnoses are supplied by the evaluator, not independently verified. No conversion lift inferred.')


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
