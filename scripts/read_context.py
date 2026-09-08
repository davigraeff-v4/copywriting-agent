#!/usr/bin/env python3
"""Print sources and append phase/hash receipts; does not certify comprehension."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("paths", nargs="+")
    p.add_argument("--phase", choices=("context", "production", "review"), required=True)
    p.add_argument("--receipts", type=Path, required=True)
    a = p.parse_args()
    records = json.loads(a.receipts.read_text()) if a.receipts.exists() else []
    for name in a.paths:
        path = (ROOT / name).resolve()
        relative = path.relative_to(ROOT).as_posix()
        data = path.read_bytes()
        print(f"\nFILE: {relative}\n{data.decode('utf-8')}")
        records.append(dict(path=relative, phase=a.phase, sha256=hashlib.sha256(data).hexdigest(),
                            read_at=datetime.now(timezone.utc).isoformat()))
    a.receipts.parent.mkdir(parents=True, exist_ok=True)
    a.receipts.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
