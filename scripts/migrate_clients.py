#!/usr/bin/env python3
"""Plan, apply and verify an exact-path client migration; no copy or review rewriting."""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path
from client_paths import ROOT, MAP_PATH, client_dir

PILOT = ('rastrek', 'hammertech', 'cadeira-e-cia', 'scann-up', 'viezza')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local(root, relative):
    root = Path(root).resolve()
    if not isinstance(relative, str) or Path(relative).is_absolute():
        raise ValueError('expected relative project path')
    path = (root / relative).resolve()
    if not path.is_relative_to(root) or path == root:
        raise ValueError('path outside project')
    return path


def files(path):
    return sorted(p for p in path.rglob('*') if p.is_file() and p.name != '.DS_Store') if path.is_dir() else []


def add_materials(selected, slug, material, root):
    """Explicitly assigned folders/files; paths and area remain reviewable in the manifest."""
    area = material.get('area', 'fontes')
    if area not in ('fontes', 'assets', 'historico/legado'):
        raise ValueError('invalid material area')
    source = local(root, material['path'])
    candidates = files(source) if source.is_dir() else [source] if source.is_file() else []
    if not candidates:
        raise ValueError('material missing/empty: ' + material['path'])
    for item in candidates:
        old = item.relative_to(root).as_posix()
        dest = f'clients/{slug}/{area}/{old}'
        if old in selected and selected[old] != dest:
            raise ValueError('ambiguous material: ' + old)
        selected[old] = dest


def material_plan(materials, root=ROOT):
    """Supplement existing clients without rewriting their profiles or campaign versions."""
    root = Path(root).resolve()
    moves = []
    for slug, entries in materials.items():
        if not (client_dir(slug, root) / 'CLIENTE.md').is_file():
            raise ValueError('material-only migration requires canonical profile: ' + slug)
        selected = {}
        for entry in entries:
            add_materials(selected, slug, entry, root)
        moves.extend(dict(source=old, destination=dest, client=slug, sha256=sha(root / old)) for old, dest in selected.items())
    return dict(schema_version=1, clients=list(materials), moves=moves, generated={})


def plan(clients=PILOT, root=ROOT, materials=None):
    root = Path(root).resolve()
    if set(materials or {}) - set(clients):
        raise ValueError('materials assigned to a client outside this plan')
    moves, generated = [], {}
    curated = root / 'examples/curated/index.json'
    entries = json.loads(curated.read_text()) if curated.exists() else []
    for slug in clients:
        base = client_dir(slug, root)
        if base.exists():
            raise ValueError('client folder already exists: ' + slug)
        current = root / f'clients/current/{slug}.md'
        legacy = root / f'clients/{slug}.md'
        selected = {}
        prefix = f'clients/{slug}/'

        def add(source, destination):
            rel = source.relative_to(root).as_posix()
            if rel in selected and selected[rel] != destination:
                raise ValueError('ambiguous source: ' + rel)
            local(root, rel)
            local(root, destination)
            selected[rel] = destination

        for source in (current, legacy):
            if source.is_file():
                add(source, prefix + 'historico/legado/' + source.relative_to(root).as_posix())
        for source in files(root / f'campaigns/{slug}'):
            add(source, prefix + 'campanhas/' + source.relative_to(root / f'campaigns/{slug}').as_posix())
        for parent in ('outputs', 'examples'):
            for source in files(root / parent):
                if source.name.startswith(slug + '-') or source.name == slug + '.md':
                    if source.parent.name != 'curated':
                        add(source, prefix + 'historico/legado/' + source.relative_to(root).as_posix())
        for entry in entries:
            if entry.get('client') == slug and (root / entry['path']).is_file():
                add(root / entry['path'], prefix + 'referencias/curadas/' + Path(entry['path']).name)
        # Loose materials whose filename explicitly identifies the client.
        for source in sorted(root.glob(slug + '-*')):
            if source.is_file():
                area = 'historico/legado' if source.suffix == '.md' else 'fontes'
                add(source, prefix + area + '/' + source.name)
        for material in (materials or {}).get(slug, []):
            add_materials(selected, slug, material, root)
        if slug == 'hammertech':
            for source in files(root / 'tmp/hammertech'):
                add(source, prefix + 'fontes/' + source.relative_to(root).as_posix())
        if slug == 'viezza':
            for source in sorted(root.glob('viezza-*.txt')) + sorted((root / 'tmp').glob('viezza-*')):
                if source.is_file():
                    add(source, prefix + 'fontes/' + source.relative_to(root).as_posix())
        if slug == 'scann-up':
            source = root / 'scann-up-lp-atual.txt'
            if source.is_file():
                add(source, prefix + 'fontes/' + source.name)
            for source in files(root / 'output/creatives/scann-up'):
                add(source, prefix + 'assets/creatives/' + source.relative_to(root / 'output/creatives/scann-up').as_posix())

        # Deduplicate only historical copy mirrors, within the same client.
        canonical = {}
        for old, dest in sorted(selected.items(), key=lambda x: (not x[0].startswith('campaigns/'), x[0])):
            digest = sha(root / old)
            mirror = old.endswith('.md') and old.startswith(('outputs/', 'examples/')) and '/curated/' not in old
            if mirror and digest in canonical:
                dest = canonical[digest]
            elif (old.startswith('campaigns/') and Path(old).name == 'final.md') or mirror:
                canonical.setdefault(digest, dest)
            moves.append(dict(source=old, destination=dest, sha256=digest, client=slug))

        profile = current if current.is_file() else legacy if legacy.is_file() else None
        if not selected and profile is None:
            raise ValueError('no client profile or material found: ' + slug)
        # Preserve all current paragraphs; move only campaign chronology to the lessons file.
        profile_text = profile.read_text(encoding='utf-8') if profile else (
            f'# Cliente: {slug}\n\nNão havia ficha de cliente consolidada antes desta organização. '
            'Consultar os materiais preservados em fontes e histórico para a próxima tarefa. '
            'Identidade comercial, público, voz, fatos e restrições ainda precisam de consolidação a partir dessas fontes. '
            'Copy histórica não confirma oferta vigente, aprovação ou performance.\n')
        sections = re.split(r'(?=^## )', profile_text, flags=re.M)
        history = [s for s in sections if s.startswith(('## Campanhas\n', '## Campanha e validade\n', '## Histórico'))]
        state = ''.join(s for s in sections if s not in history)
        state = state.replace(f'clients/{slug}.md', f'clients/{slug}/historico/legado/clients/{slug}.md')
        generated[prefix + 'CLIENTE.md'] = state.rstrip() + (
            '\n\n## Arquivos deste cliente\n\n'
            '- `APRENDIZADOS.md`: decisões, validade e cronologia preservadas. Ler junto desta ficha.\n'
            '- `campanhas/`: todas as versões, revisões e feedbacks.\n'
            '- `fontes/`, `referencias/`, `assets/`: materiais locais, sem confirmação adicional.\n'
            '- `historico/legado/`: fichas originais e cópias históricas.\n\n'
            'Consolidação de estrutura em 2026-10-09. Fatos e datas acima não foram reconfirmados. '
            'Restrições ativas prevalecem sobre terminologia antiga no próprio resumo e no legado.\n')
        if current.is_file() and not legacy.is_file() and f'clients/{slug}.md' in profile_text:
            generated[prefix + 'CLIENTE.md'] += (
                f'\nPendência anterior à migração: a ficha consolidada cita `clients/{slug}.md`, '
                'mas esse arquivo original não foi localizado no projeto. A ficha consolidada presente foi preservada integralmente no histórico.\n')
        chronology = ''.join(history).replace(f'campaigns/{slug}/', f'clients/{slug}/campanhas/')
        generated[prefix + 'APRENDIZADOS.md'] = (
            f'# Decisões e aprendizados: {slug}\n\n'
            'As restrições vigentes, seu escopo e origem estão em `CLIENTE.md`. '
            'Este arquivo preserva a cronologia da ficha atual, sem criar aprovação nem transformar '
            'um feedback de campanha em preferência global. Aprovação, publicação e performance são estados separados.\n\n'
            + chronology.rstrip() + '\n\n## Registro original\n\n'
            + (f'- Ficha atual antes da migração: `historico/legado/clients/current/{slug}.md`.\n' if current.is_file()
               else '- Sem ficha atual prévia; esta organização não acrescentou fatos comerciais nem aprovação.\n')
            + (f'- Histórico completo: `historico/legado/clients/{slug}.md`. Correções posteriores prevalecem.\n' if legacy.exists() else '')
            + '- Feedback literal adicional: `campanhas/*/v*/feedback.md`. Não inferir decisão pelo score.\n')
    return dict(schema_version=1, clients=list(clients), moves=moves, generated=generated)


def preflight(manifest, root=ROOT):
    root = Path(root).resolve()
    clients = set(manifest['clients'])
    for slug in clients:
        client_dir(slug, root)
    targets, sources = {}, set()
    for item in manifest['moves']:
        src, dst = local(root, item['source']), local(root, item['destination'])
        if item['client'] not in clients or not dst.is_relative_to(client_dir(item['client'], root)):
            raise ValueError('client destination mismatch')
        if item['source'] in sources:
            raise ValueError('duplicate source')
        sources.add(item['source'])
        if not src.is_file() or sha(src) != item['sha256']:
            raise ValueError('source missing or changed: ' + item['source'])
        if dst.exists():
            raise ValueError('destination already exists: ' + item['destination'])
        if item['destination'] in targets and targets[item['destination']] != item['sha256']:
            raise ValueError('destination collision')
        targets[item['destination']] = item['sha256']
    for dest in manifest['generated']:
        path = local(root, dest)
        if not any(path.is_relative_to(client_dir(s, root)) for s in clients):
            raise ValueError('generated destination mismatch')
        if path.exists() or dest in targets:
            raise ValueError('generated destination collision: ' + dest)


def verify(manifest, root=ROOT):
    errors = []
    registry = json.loads(local(root, MAP_PATH.as_posix()).read_text())
    for item in manifest['moves']:
        dest = local(root, item['destination'])
        if not dest.is_file() or sha(dest) != item['sha256']:
            errors.append('missing/changed destination: ' + item['destination'])
        if registry.get('paths', {}).get(item['source']) != {k: item[k] for k in ('destination', 'sha256', 'client')}:
            errors.append('missing/changed alias: ' + item['source'])
        if local(root, item['source']).exists():
            errors.append('source still present: ' + item['source'])
    for dest, content in manifest['generated'].items():
        path = local(root, dest)
        if not path.is_file() or path.read_text(encoding='utf-8') != content:
            errors.append('missing/changed profile: ' + dest)
    return dict(status='failed' if errors else 'passed', original_files=len(manifest['moves']),
                canonical_files=len({i['destination'] for i in manifest['moves']}),
                profiles=len(manifest['generated']), errors=errors)


def apply(manifest, root=ROOT):
    root = Path(root).resolve()
    preflight(manifest, root)
    token = hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest()[:16]
    backup = local(root, '.local/migrations/' + token)
    if backup.exists():
        raise ValueError('transaction exists; inspect/rollback before retry')
    backup.mkdir(parents=True)
    registry_path = local(root, MAP_PATH.as_posix())
    previous = registry_path.read_text() if registry_path.exists() else None
    registry = json.loads(previous) if previous is not None else dict(schema_version=1, paths={})
    if any(i['source'] in registry['paths'] for i in manifest['moves']):
        raise ValueError('source alias already registered')
    (backup / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    (backup / 'previous-registry.json').write_text(json.dumps(previous))
    for item in manifest['moves']:
        source = local(root, item['source'])
        saved = backup / 'files' / item['source']
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, saved)
        if sha(saved) != item['sha256']:
            raise ValueError('backup mismatch')
    try:
        for item in manifest['moves']:
            source, dest = local(root, item['source']), local(root, item['destination'])
            if sha(source) != item['sha256']:
                raise ValueError('source changed during migration')
            if not dest.exists():
                dest.parent.mkdir(parents=True, exist_ok=True)
                with dest.open('xb') as output:
                    output.write(source.read_bytes())
            if sha(dest) != item['sha256']:
                raise ValueError('copy mismatch')
            registry['paths'][item['source']] = {k: item[k] for k in ('destination', 'sha256', 'client')}
        for dest, content in manifest['generated'].items():
            path = local(root, dest)
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('x', encoding='utf-8') as output:
                output.write(content)
        pending = registry_path.with_suffix('.pending.json')
        pending.write_text(json.dumps(registry, ensure_ascii=False, indent=2))
        pending.replace(registry_path)
        for item in manifest['moves']:
            source = local(root, item['source'])
            if sha(source) != item['sha256']:
                raise ValueError('source changed before removal')
            source.unlink()
        result = verify(manifest, root)
        if result['errors']:
            raise ValueError('; '.join(result['errors']))
        (backup / 'status.txt').write_text('applied\n')
        return dict(result, transaction=str(backup.relative_to(root)))
    except Exception:
        rollback(backup, root)
        raise


def rollback(backup, root=ROOT):
    root = Path(root).resolve()
    backup = Path(backup).resolve()
    if not backup.is_relative_to(root / '.local/migrations'):
        raise ValueError('unknown transaction directory')
    manifest = json.loads((backup / 'manifest.json').read_text())
    previous = json.loads((backup / 'previous-registry.json').read_text())
    registry = local(root, MAP_PATH.as_posix())
    before = json.loads(previous) if previous is not None else dict(schema_version=1, paths={})
    after = json.loads(json.dumps(before))
    for item in manifest['moves']:
        after['paths'][item['source']] = {k: item[k] for k in ('destination', 'sha256', 'client')}
    actual = json.loads(registry.read_text()) if registry.exists() else dict(schema_version=1, paths={})
    if actual not in (before, after):
        raise ValueError('rollback registry changed after this transaction')
    # Refuse to overwrite edits made after migration; preserve those for manual recovery.
    for item in manifest['moves']:
        for path in (local(root, item['source']), local(root, item['destination'])):
            if path.exists() and sha(path) != item['sha256']:
                raise ValueError('rollback would overwrite changed file: ' + str(path))
        saved = backup / 'files' / item['source']
        if not saved.is_file() or sha(saved) != item['sha256']:
            raise ValueError('rollback backup missing/changed')
    for dest, content in manifest['generated'].items():
        path = local(root, dest)
        if path.exists() and path.read_text(encoding='utf-8') != content:
            raise ValueError('rollback profile changed: ' + dest)
    for item in manifest['moves']:
        source = local(root, item['source'])
        source.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(backup / 'files' / item['source'], source)
    for dest in {i['destination'] for i in manifest['moves']} | set(manifest['generated']):
        local(root, dest).unlink(missing_ok=True)
    if previous is None:
        registry.unlink(missing_ok=True)
    else:
        registry.write_text(previous)
    for slug in manifest['clients']:
        base = client_dir(slug, root)
        for path in sorted(base.rglob('*'), key=lambda p: len(p.parts), reverse=True):
            if path.is_dir() and not any(path.iterdir()):
                path.rmdir()
        if base.exists() and not any(base.iterdir()):
            base.rmdir()
    (backup / 'status.txt').write_text('rolled_back\n')
    return dict(status='rolled_back', restored_files=len(manifest['moves']))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('plan')
    p.add_argument('--client', action='append')
    p.add_argument('--output', required=True)
    p.add_argument('--materials', help='project-relative JSON object: client -> [{path, area}]')
    p.add_argument('--materials-only', action='store_true', help='supplement already migrated clients')
    for command in ('apply', 'verify', 'rollback'):
        sub.add_parser(command).add_argument('manifest' if command != 'rollback' else 'transaction')
    args = parser.parse_args()
    try:
        if args.command == 'plan':
            materials = json.loads(local(ROOT, args.materials).read_text()) if args.materials else {}
            if args.materials_only:
                if args.client or not materials:
                    raise ValueError('materials-only requires --materials and no --client')
                manifest = material_plan(materials)
            else:
                manifest = plan(args.client or PILOT, materials=materials)
            preflight(manifest)
            output = local(ROOT, args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            with output.open('x', encoding='utf-8') as stream:
                json.dump(manifest, stream, ensure_ascii=False, indent=2)
            result = dict(status='planned', files=len(manifest['moves']), profiles=len(manifest['generated']), manifest=str(output))
        elif args.command == 'rollback':
            result = rollback(local(ROOT, args.transaction))
        else:
            manifest = json.loads(local(ROOT, args.manifest).read_text())
            result = (apply if args.command == 'apply' else verify)(manifest)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2 if result.get('errors') else 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps(dict(status='blocked', errors=[str(error)]), ensure_ascii=False))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
