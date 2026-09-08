#!/usr/bin/env python3
"""Local lexical retrieval; explicit metadata, no client crossover or eval leakage."""
import argparse
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def words(text):
    text = "".join(c for c in unicodedata.normalize("NFD", text.casefold()) if not unicodedata.combining(c))
    return set(re.findall(r"\w{3,}", text))


def retrieve(query, entries, route, client, use=None, limit=4, root=ROOT):
    tokens, results = words(query), []
    for item in entries:
        if item.get("status") != "active" or route not in item.get("routes", []):
            continue
        if item.get("client") not in (client, "*"):
            continue
        if use and item.get("use") != use:
            continue
        path = (root / item["path"]).resolve()
        try:
            relative = path.relative_to(root.resolve())
        except ValueError:
            continue
        if any(part in ("evals", ".local", "history") for part in relative.parts) or not path.is_file():
            continue
        summary = item.get("summary", "")
        tags = " ".join(item.get("tags", []))
        overlap = tokens & words(summary + " " + tags)
        if not overlap:
            continue
        # Rank metadata first; read only a bounded excerpt after filtering.
        score = len(overlap) * 2 + (1 if item.get("client") == client else 0)
        results.append(dict(id=item["id"], path=str(relative), use=item["use"],
                            score=score, summary=summary, matched=sorted(overlap)))
    results.sort(key=lambda x: (-x["score"], x["id"]))
    selected = results[:limit]
    for item in selected:
        item["excerpt"] = (root / item["path"]).read_text(encoding="utf-8")[:1200]
    return selected


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--query", required=True)
    p.add_argument("--route", choices=("lp", "social", "ads", "direct"), required=True)
    p.add_argument("--client", required=True)
    p.add_argument("--use", choices=("guidance", "positive", "negative", "structure"))
    p.add_argument("--index", action="append", default=[])
    p.add_argument("--limit", type=int, default=4)
    a = p.parse_args()
    if a.limit < 1 or a.limit > 20:
        p.error("limit must be 1..20")
    entries = []
    for path in a.index or [str(ROOT / "knowledge/retrieval-index.json")]:
        entries.extend(json.loads(Path(path).read_text()))
    result = retrieve(a.query, entries, a.route, a.client, a.use, a.limit)
    print(json.dumps(dict(results=result, note="Open selected sources. Ranking is not factual validation."), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
