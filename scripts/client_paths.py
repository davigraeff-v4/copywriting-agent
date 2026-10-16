#!/usr/bin/env python3
"""Resolve preserved references after client migration, without following escapes."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = Path('.local/client-path-map.json')


def client_dir(slug, root=ROOT):
    if not isinstance(slug, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
        raise ValueError('client must be a lowercase slug')
    root = Path(root).resolve()
    path = (root / 'clients' / slug).resolve()
    if not path.is_relative_to(root / 'clients'):
        raise ValueError('client directory outside clients/')
    return path


def resolve_reference(reference, root=ROOT):
    """Existing local file or exact migration alias; no URL guessing or prefix rewrite."""
    root = Path(root).resolve()
    if not isinstance(reference, str) or not reference.strip():
        raise ValueError('local reference must be a non-empty path')
    path = Path(reference)
    candidate = (root / path).resolve()
    if not candidate.is_relative_to(root):
        raise ValueError('local reference outside project')
    if candidate.is_file():
        return candidate
    relative = candidate.relative_to(root).as_posix()
    registry_path = root / MAP_PATH
    if registry_path.exists():
        if not registry_path.resolve().is_relative_to(root):
            raise ValueError('migration registry outside project')
        registry = json.loads(registry_path.read_text(encoding='utf-8'))
        if not isinstance(registry, dict) or not isinstance(registry.get('paths'), dict):
            raise ValueError('invalid migration registry')
        entry = registry.get('paths', {}).get(relative)
        if entry:
            if not isinstance(entry, dict) or not isinstance(entry.get('destination'), str) or not entry['destination'].strip():
                raise ValueError('invalid migration destination')
            candidate = (root / entry['destination']).resolve()
            if not candidate.is_relative_to(root):
                raise ValueError('migration destination outside project')
            if entry.get('client') and not candidate.is_relative_to(client_dir(entry['client'], root)):
                raise ValueError('migration destination belongs to another client')
            if candidate.is_file():
                return candidate
    raise FileNotFoundError('local reference not found: ' + reference)
