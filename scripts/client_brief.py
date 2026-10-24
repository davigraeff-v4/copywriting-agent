#!/usr/bin/env python3
"""Read one client's state and list versions and literal feedback, without inferring approval."""
import argparse
import json
import re
import uuid
from pathlib import Path
from client_paths import ROOT, client_dir


def brief(slug, root=ROOT):
    root = Path(root).resolve()
    base = client_dir(slug, root)
    if base != root / 'clients' / slug:
        raise ValueError('client directory identity changed')
    profile = base / 'CLIENTE.md'
    lessons = base / 'APRENDIZADOS.md'
    marker = base / '.central-identity.json'
    automatic = False
    if marker.exists():
        if marker.is_symlink() or base.is_symlink() or base != root / 'clients' / slug:
            raise ValueError('automatic client path changed')
        identity = json.loads(marker.read_text(encoding='utf-8'))
        if set(identity) != {'schema_version','client_id','binding_id','project_id','client_slug'} or identity['schema_version'] != 1:
            raise ValueError('invalid automatic client identity')
        for name in ('client_id','binding_id','project_id'):
            if str(uuid.UUID(identity[name])) != identity[name]:
                raise ValueError('invalid automatic client identity')
        if identity['client_slug'] != slug or slug != 'central-' + identity['client_id'].replace('-', ''):
            raise ValueError('automatic client identity mismatch')
        automatic = True
        for candidate in (profile, lessons):
            if candidate.is_symlink():
                raise ValueError('automatic memory symlink refused')
    if automatic:
        profile_paths = [p for p in (profile, lessons) if p.is_file()]
        campaigns = base / 'campanhas'
        layout = 'automatic_client'
    elif profile.is_file():
        profile_paths = [profile, lessons] if lessons.is_file() else [profile]
        campaigns = base / 'campanhas'
        layout = 'client_folder'
    else:
        profile_paths = [p for p in (root / f'clients/current/{slug}.md', root / f'clients/{slug}.md') if p.is_file()]
        campaigns = root / 'campaigns' / slug
        layout = 'legacy'
    if not profile_paths and not automatic:
        raise FileNotFoundError('client profile not found: ' + slug)
    def relative(path):
        if automatic:
            if not path.resolve().is_relative_to(base):
                raise ValueError('automatic material belongs to another client')
            for candidate in (path, *path.parents):
                if candidate.is_symlink():
                    raise ValueError('automatic material symlink refused')
        if not path.resolve().is_relative_to(root):
            raise ValueError('client material outside project')
        return path.relative_to(root).as_posix()
    if automatic and campaigns.exists():
        relative(campaigns)
    records = []
    for campaign in sorted(campaigns.iterdir()) if campaigns.exists() else []:
        if not campaign.is_dir():
            continue
        if automatic:
            relative(campaign)
        versions = []
        for version in sorted(campaign.glob('v*'), key=lambda p: int(p.name[1:]) if re.fullmatch(r'v\d+', p.name) else -1):
            if not version.is_dir():
                continue
            feedback = version / 'feedback.md'
            versions.append(dict(version=version.name, path=relative(version),
                files=[p.name for p in sorted(version.iterdir()) if p.is_file()],
                feedback=dict(path=relative(feedback), literal=feedback.read_text(encoding='utf-8')) if feedback.is_file() else None))
        records.append(dict(campaign=campaign.name, versions=versions, latest_version=versions[-1]['version'] if versions else None))
    return dict(client=slug, layout=layout, memory_available=bool(profile_paths),
        context=[dict(path=relative(p), content=p.read_text(encoding='utf-8')) for p in profile_paths],
        campaigns=records, note='Feedback é literal. Score ou existência de final.md não significam aprovação, publicação ou performance. Fatos antigos precisam de validade para a tarefa atual.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('client')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    try:
        result = brief(args.client)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            for item in result['context']:
                print(item['path'] + '\n\n' + item['content'])
            for campaign in result['campaigns']:
                print('\nCampanha: ' + campaign['campaign'] + ' | última versão: ' + str(campaign['latest_version']))
                for version in campaign['versions']:
                    print(version['path'])
                    if version['feedback']:
                        print(version['feedback']['path'] + '\n' + version['feedback']['literal'])
            print('\n' + result['note'])
        return 0
    except (OSError, ValueError) as error:
        print(json.dumps(dict(status='blocked', errors=[str(error)]), ensure_ascii=False))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
