#!/usr/bin/env python3
"""Check local instructions, executable fixtures and reference integrity."""
import ast
import json
import re
from pathlib import Path
from copycheck import validate

ROOT=Path(__file__).resolve().parents[1]

def validate_project(root=ROOT):
    errors=[]
    a=(root/'AGENTS.md').read_text().splitlines()[1:]
    b=(root/'CLAUDE.md').read_text().splitlines()[1:]
    if a!=b: errors.append('AGENTS.md and CLAUDE.md diverge')
    skills=sorted((root/'skills').glob('*/SKILL.md'))
    if len(skills)!=14: errors.append('Expected 14 skills')
    refs=0
    for p in skills:
        s=p.read_text()
        if not s.startswith('---\n') or '\n---\n' not in s[4:]: errors.append(f'{p}: missing frontmatter')
        for ref in re.findall(r'`((?:knowledge|quality|skills|scripts|briefings)/[^`]+\.(?:md|json|py))`',s):
            if any(c in ref for c in '*{}'): continue
            refs+=1
            if not (root/ref).is_file(): errors.append(f'{p.relative_to(root)}: missing {ref}')
    index=json.loads((root/'knowledge/retrieval-index.json').read_text()); ids=set()
    for item in index:
        if item['id'] in ids: errors.append('Duplicate retrieval id '+item['id'])
        ids.add(item['id'])
        path=(root/item['path']).resolve()
        if not path.is_relative_to(root) or not path.is_file(): errors.append('Missing/outside indexed path '+item['path'])
        if not set(item['routes'])<={'lp','social','ads','direct'}: errors.append('Invalid indexed route')
    for p in (root/'scripts').glob('*.py'):
        try: ast.parse(p.read_text())
        except SyntaxError as e: errors.append(f'{p.name}: {e}')
    fixture=json.loads((root/'tests/fixtures/valid-delivery.json').read_text()); errors+=validate(fixture)
    cases=json.loads((root/'evals/cases.json').read_text())
    if len({c['id'] for c in cases})!=len(cases): errors.append('Duplicate evaluation case')
    return dict(status='failed' if errors else 'passed',skills=len(skills),skill_references=refs,
                retrieval_entries=len(index),evaluation_cases=len(cases),errors=errors)

if __name__=='__main__':
    result=validate_project(); print(json.dumps(result,ensure_ascii=False,indent=2)); raise SystemExit(bool(result['errors']))
