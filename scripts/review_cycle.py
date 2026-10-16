#!/usr/bin/env python3
"""Bounded local review lifecycle. The agent supplies text and judgment; Python enforces history and budgets."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

import copycheck

MAX_REWRITES = 2
MAX_REVIEW_REPAIRS = 2
TERMINAL = {'ready_for_human_approval', 'needs_input', 'needs_direction', 'needs_review_decision'}
CATEGORIES = {'writing', 'direction', 'evidence', 'context', 'review'}


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def content_digest(delivery):
    # Version labels, notes and claim mapping alone cannot masquerade as a rewrite.
    return digest({k: delivery.get(k) for k in ('client', 'campaign', 'route', 'fields', 'context', 'sources', 'facts', 'constraints', 'outline', 'requirements')})


def start(case_id, direction_id):
    if not isinstance(case_id, str) or not case_id.strip() or not isinstance(direction_id, str) or not direction_id.strip():
        raise ValueError('case_id and authorized direction_id required')
    return dict(schema_version=1, case_id=case_id, direction_id=direction_id,
                status='awaiting_initial_review', rewrites=0, review_repairs=0, attempts=[],
                next_action='Produce the initial version and review it against the same source packet.', human_approval=False)


def validate_history(state):
    if state.get('schema_version') != 1 or state.get('human_approval') is not False:
        raise ValueError('Invalid lifecycle state; this controller cannot record human approval')
    previous = None
    for attempt in state['attempts']:
        item = {k: v for k, v in attempt.items() if k != 'event_sha256'}
        if attempt.get('previous_event_sha256') != previous or digest(item) != attempt.get('event_sha256'):
            raise ValueError('Attempt history changed')
        previous = attempt['event_sha256']
    if state['attempts']:
        last = state['attempts'][-1]
        for key in ('status', 'rewrites', 'review_repairs', 'next_action'):
            if state.get(key) != last[key]:
                raise ValueError('State disagrees with preserved attempt history')
        if state['direction_id'] != last['direction_id'] or state['case_id'] != last['case_id']:
            raise ValueError('Direction/case reset is not allowed within a cycle')
    elif state != start(state['case_id'], state['direction_id']):
        raise ValueError('Initial lifecycle state changed')


def validate_diagnosis(diagnosis, delivery):
    if not isinstance(diagnosis, dict) or diagnosis.get('category') not in CATEGORIES:
        raise ValueError('Blocked attempt needs a classified diagnosis')
    for key in ('reason', 'next_step'):
        if not isinstance(diagnosis.get(key), str) or not diagnosis[key].strip():
            raise ValueError('Diagnosis requires concrete reason and next_step')
    if type(diagnosis.get('can_fix_with_available_context')) is not bool:
        raise ValueError('Diagnosis must declare whether available context is sufficient')
    if not isinstance(diagnosis.get('changes'), list) or not diagnosis['changes'] or any(not isinstance(x, str) or not x.strip() for x in diagnosis['changes']):
        raise ValueError('Diagnosis requires proposed changes or a concrete resolution')
    ids = {f.get('id') for f in delivery.get('fields', []) if isinstance(f, dict)}
    if not isinstance(diagnosis.get('field_ids'), list) or any(x not in ids for x in diagnosis['field_ids']):
        raise ValueError('Diagnosis references an unknown field')
    missing = diagnosis.get('missing_information', [])
    if not isinstance(missing, list) or any(not isinstance(x, str) or not x.strip() for x in missing):
        raise ValueError('Invalid missing_information')
    if not diagnosis['can_fix_with_available_context'] and not missing:
        raise ValueError('A stop needs the specific missing information or decision')


def record_attempt(state, delivery, review, diagnosis=None, *, direction_id=None, resolution=None):
    validate_history(state)
    resuming = state['status'] == 'needs_input' and resolution is not None
    if state['status'] in TERMINAL and not resuming:
        raise ValueError('Cycle already ended; no automatic restart or extra rewrite')
    if resuming:
        if not isinstance(resolution, dict) or resolution.get('kind') != 'new_information' or not isinstance(resolution.get('reason'), str) or not resolution['reason'].strip():
            raise ValueError('Resumption requires concrete new information, not a direction reset')
        ids = resolution.get('source_ids')
        sources = {x['id']: digest(x) for x in delivery.get('sources', [])}
        prior_sources = state['attempts'][-1].get('source_snapshot', {})
        if not isinstance(ids, list) or not ids or any(x not in sources for x in ids) or not any(sources[x] != prior_sources.get(x) for x in ids):
            raise ValueError('Resumption requires a new or updated preserved source')
        if state['rewrites'] >= MAX_REWRITES:
            raise ValueError('New information cannot reset an exhausted rewrite budget')
    if direction_id is not None and direction_id != state['direction_id']:
        raise ValueError('New direction requires an explicit new authorization; budget cannot reset silently')
    state = copy.deepcopy(state)
    content_sha = content_digest(delivery)
    prior = state['attempts'][-1] if state['attempts'] else None
    if prior:
        changed = content_sha != prior['content_sha256']
        if prior['status'] in {'needs_revision', 'needs_input'}:
            if not changed:
                raise ValueError('A rewrite must change text/context; rerating unchanged copy cannot consume or bypass the cycle')
            state['rewrites'] += 1
        elif prior['status'] == 'needs_review_repair':
            if changed:
                raise ValueError('Review repair cannot hide a text/context change')
            state['review_repairs'] += 1
        else:
            raise ValueError('Invalid previous state')
    if state['rewrites'] > MAX_REWRITES or state['review_repairs'] > MAX_REVIEW_REPAIRS:
        raise ValueError('Lifecycle budget exceeded')
    result = copycheck.check(delivery, review)
    if result['status'] == 'ready_for_human_approval':
        status = 'ready_for_human_approval'
        action = 'Render this exact version with its current review and request human approval. Publication is not authorized.'
    else:
        # Missing review is a review repair, never success or permission to skip judgment.
        if review is None and diagnosis is None:
            diagnosis = dict(category='review', reason='Editorial review absent.', field_ids=[], changes=['Create the missing review using exact evidence.'], next_step='Complete the review without changing the text.', can_fix_with_available_context=True, missing_information=[])
        validate_diagnosis(diagnosis, delivery)
        category = diagnosis['category']
        if not diagnosis['can_fix_with_available_context']:
            status = 'needs_direction' if category == 'direction' else 'needs_review_decision' if category == 'review' else 'needs_input'
            action = diagnosis['next_step']
        elif category == 'review':
            status = 'needs_review_repair' if state['review_repairs'] < MAX_REVIEW_REPAIRS else 'needs_review_decision'
            action = diagnosis['next_step'] if status == 'needs_review_repair' else 'Review-repair limit reached. Present the exact disputed evidence and a concrete decision request: ' + diagnosis['next_step']
        elif state['rewrites'] < MAX_REWRITES:
            status = 'needs_revision'
            action = diagnosis['next_step']
        else:
            status = 'needs_direction'
            action = 'Two rewrites used. Present the remaining failure and a concrete alternative direction or missing datum: ' + diagnosis['next_step']
    state.update(status=status, next_action=action)
    event = dict(number=len(state['attempts']) + 1, case_id=state['case_id'], direction_id=state['direction_id'],
                 delivery_sha256=copycheck.digest(delivery), content_sha256=content_sha,
                 review_sha256=digest(review), source_snapshot={x['id']: digest(x) for x in delivery.get('sources', [])}, resolution=resolution, previous_event_sha256=prior['event_sha256'] if prior else None,
                 result=result, diagnosis=diagnosis, status=status, rewrites=state['rewrites'],
                 review_repairs=state['review_repairs'], next_action=action)
    event['event_sha256'] = digest(event)
    state['attempts'].append(event)
    return state


def load(path):
    return json.loads(Path(path).read_text())


def save_new(path, value):
    with Path(path).open('x') as handle:
        handle.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def persist_attempt(folder, state, delivery, review, diagnosis=None, *, direction_id=None, resolution=None):
    """Append immutable snapshots; do not mutate prior artifacts or create a new cycle on exhaustion."""
    folder = Path(folder)
    if folder.exists() and any(folder.iterdir()):
        latest = sorted(folder.glob('attempt-*/state.json'))
        if not latest or load(latest[-1]) != state:
            raise ValueError('Supplied state is not the latest persisted state')
        for old in latest:
            snapshot = load(old)
            event = snapshot['attempts'][-1]
            if copycheck.digest(load(old.parent/'delivery.json')) != event['delivery_sha256'] or digest(load(old.parent/'review.json')) != event['review_sha256']:
                raise ValueError('Preserved delivery or review changed')
    updated = record_attempt(state, delivery, review, diagnosis, direction_id=direction_id, resolution=resolution)
    target = folder / ('attempt-%02d' % len(updated['attempts']))
    target.mkdir(parents=True, exist_ok=False)
    for name, value in [('delivery.json', delivery), ('review.json', review), ('diagnosis.json', diagnosis), ('check.json', updated['attempts'][-1]['result']), ('state.json', updated)]:
        save_new(target/name, value)
    return updated


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    parser.add_argument('--case-id')
    parser.add_argument('--direction-id')
    parser.add_argument('--delivery', type=Path)
    parser.add_argument('--review', type=Path)
    parser.add_argument('--diagnosis', type=Path)
    parser.add_argument('--resolution', type=Path, help='Resume needs_input with new/updated source_ids and reason; does not reset budget')
    args = parser.parse_args()
    try:
        history = sorted(args.folder.glob('attempt-*/state.json'))
        state = load(history[-1]) if history else start(args.case_id, args.direction_id)
        if args.delivery:
            state = persist_attempt(args.folder, state, load(args.delivery), load(args.review) if args.review else None, load(args.diagnosis) if args.diagnosis else None, direction_id=args.direction_id, resolution=load(args.resolution) if args.resolution else None)
        print(json.dumps(state, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, TypeError, KeyError, OSError) as error:
        print(json.dumps(dict(status='error', error=str(error)), ensure_ascii=False))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
