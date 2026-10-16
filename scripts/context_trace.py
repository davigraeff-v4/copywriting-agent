#!/usr/bin/env python3
"""Expose skills and local RAG with an observable, session-local usage trace.

No model calls, ranking changes, client indexing or semantic-quality certification.
"""
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def normalized(text):
    return ' '.join(text.split())


def catalog(root=ROOT):
    items = []
    for path in sorted((root / 'skills').glob('*/SKILL.md')):
        text = path.read_text()
        front = text.split('---', 2)[1] if text.startswith('---\n') else ''
        name = re.search(r'^name:\s*(.+)$', front, re.M)
        description = re.search(r'^description:\s*(.+)$', front, re.M)
        if not name or not description:
            raise ValueError('Skill metadata absent: ' + str(path.relative_to(root)))
        items.append(dict(id=path.parent.name[:2], name=name[1].strip('"\''),
                          description=description[1].strip('"\''),
                          path=path.relative_to(root).as_posix()))
    return items


def skill_read(identifier, phase, reason, root=ROOT):
    matches = [s for s in catalog(root) if identifier in (s['id'], s['name'])]
    if len(matches) != 1:
        raise ValueError('Unknown or ambiguous skill: ' + identifier)
    item = matches[0]
    text = (root / item['path']).read_text()
    return dict(event='skill_read', **item, phase=phase, reason=reason,
                sha256=sha(text), text=text, truncated=False)


def source_read(identifier, page=None, section=None, root=ROOT):
    from rag_corpus import public_entries, document_data
    entry = next((e for e in public_entries(root) if e['id'] == identifier), None)
    if not entry:
        raise ValueError('Unknown public source: ' + identifier)
    data = document_data(entry, root)
    segments = [s for s in data['segments']
                if (page is None or s.get('page') == page)
                and (not section or section.casefold() in s['section'].casefold())]
    if not segments:
        raise ValueError('Page/section absent; no substitute selected')
    text = '\n\n'.join(s['text'] for s in segments)
    return dict(event='source_read', id=identifier, path=entry['path'],
                source_sha256=entry['sha256'], text_sha256=sha(text),
                reference_data_only=True, text=text, truncated=False,
                locator=[{k: s.get(k) for k in ('section', 'page', 'start_char', 'end_char')}
                         for s in segments])


def append_event(path, event):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    record = dict(event, recorded_at=datetime.now(timezone.utc).isoformat())
    with path.open('a') as stream:
        stream.write(json.dumps(record, ensure_ascii=False) + '\n')


def audit_usage(events, output):
    """Validate observable links; reasons/semantic fit still require judgment."""
    errors = []
    fields = {f['id']: f for f in output.get('fields', [])}
    reads = [e for e in events if e.get('event') == 'source_read']
    skills = {e['id'] for e in events if e.get('event') == 'skill_read'}
    for decision in output.get('skill_decisions', []):
        if decision.get('decision') == 'used' and decision.get('skill_id') not in skills:
            errors.append('Skill declared used without full read: ' + decision.get('skill_id', ''))
    for use in output.get('reference_uses', []):
        if use.get('decision') != 'applied':
            continue
        identifier = use.get('reference_id', '')
        quote = use.get('source_quote', '')
        if not quote or not any(e['id'] == identifier and not e.get('truncated')
                                and normalized(quote) in normalized(e['text']) for e in reads):
            errors.append('Reference quote absent from complete source read: ' + identifier)
        ids = use.get('field_ids', [])
        target = use.get('output_quote', '')
        if not ids or any(i not in fields for i in ids) or not target or not any(
                target in fields.get(i, {}).get('text', '') for i in ids):
            errors.append('Application absent from exact public fields: ' + identifier)
        if not use.get('application') or not use.get('limitation'):
            errors.append('Application/transfer limit absent: ' + identifier)
    return dict(status='failed' if errors else 'passed', errors=errors,
                skill_reads=len(skills), source_reads=len(reads),
                searches=sum(e.get('event') == 'search' for e in events),
                note='Access and textual links only; no certification of relevance or improvement.')


def audit_redundancy(fields, score, comparisons):
    errors = []
    by_id = {f['id']: f['text'] for f in fields}
    avoidable = []
    if type(score) is not int or score not in (0, 5, 10):
        errors.append('Invalid redundancy score')
    for pair in comparisons:
        valid = True
        for side in ('a', 'b'):
            quote = pair.get(side + '_quote', '')
            if not quote or quote not in by_id.get(pair.get(side + '_field'), ''):
                errors.append('Redundancy comparison lacks exact paired evidence')
                valid = False
        if pair.get('a_field') == pair.get('b_field') and pair.get('a_quote') == pair.get('b_quote'):
            errors.append('Same occurrence cannot establish repetition')
            valid = False
        if pair.get('classification') not in {'functional', 'avoidable', 'insufficient_context'}:
            errors.append('Unknown repetition classification')
            valid = False
        if not pair.get('reason') or not pair.get('effect'):
            errors.append('Repetition function/effect absent')
            valid = False
        if valid and pair['classification'] in {'avoidable', 'insufficient_context'}:
            avoidable.append(pair)
    if score in (0, 5) and not avoidable:
        errors.append('Penalty lacks paired evidence of material redundancy')
    if score == 10 and avoidable:
        errors.append('Score 10 contradicts declared material redundancy')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('catalog')
    skill = sub.add_parser('skill')
    skill.add_argument('id')
    skill.add_argument('--phase', choices=('context', 'direction', 'production', 'review', 'delivery'), required=True)
    skill.add_argument('--reason', required=True)
    search = sub.add_parser('search')
    search.add_argument('--query', required=True)
    search.add_argument('--route', choices=('lp', 'social', 'ads', 'direct'), required=True)
    search.add_argument('--client', required=True)
    search.add_argument('--use', choices=('guidance', 'positive', 'negative', 'structure', 'original'))
    search.add_argument('--limit', type=int, default=5)
    search.add_argument('--purpose', required=True)
    search.add_argument('--source', action='append')
    source = sub.add_parser('source')
    source.add_argument('--id', required=True)
    source.add_argument('--page', type=int)
    source.add_argument('--section')
    audit = sub.add_parser('audit')
    audit.add_argument('--output', type=Path, required=True)
    for item in (skill, search, source, audit):
        item.add_argument('--trace', type=Path, required=True)
    args = parser.parse_args()
    if args.command == 'catalog':
        result = catalog()
    elif args.command == 'skill':
        result = skill_read(args.id, args.phase, args.reason)
        append_event(args.trace, result)
    elif args.command == 'source':
        if args.page is not None and args.page < 1:
            parser.error('page must be positive')
        result = source_read(args.id, args.page, args.section)
        append_event(args.trace, result)
    elif args.command == 'search':
        from rag_search import Retriever
        payload = Retriever().search(args.query, args.route, args.client, args.use,
                                     args.limit, 'auto', source_ids=args.source)
        result = dict(event='search', query=args.query, route=args.route, use=args.use,
                      purpose=args.purpose, source_filter=args.source, **payload)
        append_event(args.trace, result)
    else:
        events = [json.loads(line) for line in args.trace.read_text().splitlines() if line.strip()]
        result = audit_usage(events, json.loads(args.output.read_text()))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if isinstance(result, dict) and result.get('status') == 'failed':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
