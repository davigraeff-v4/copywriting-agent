#!/usr/bin/env python3
"""Copy reference retrieval: public hybrid RAG, explicit metadata compatibility."""
import argparse
import json
import re
import unicodedata
from pathlib import Path
from client_paths import resolve_reference

ROOT = Path(__file__).resolve().parents[1]


def load_entries(indexes=None, root=ROOT):
    """Use core + curated corpus by default; explicit indexes remain authoritative."""
    if indexes:
        paths = [Path(path) for path in indexes]
    else:
        paths = [root / 'knowledge/retrieval-index.json']
        repertoire = root / 'knowledge/repertorio/catalogo.json'
        if repertoire.is_file():
            paths.append(repertoire)
    entries = []
    for path in paths:
        entries.extend(json.loads(path.read_text()))
    return entries


def words(text):
    text = "".join(c for c in unicodedata.normalize("NFD", text.casefold()) if not unicodedata.combining(c))
    return set(re.findall(r"\w{3,}", text))


def retrieve(query, entries, route, client, use=None, limit=4, root=ROOT):
    """Preserved metadata comparator and explicit-index compatibility API."""
    tokens, results = words(query), []
    for item in entries:
        if item.get("status") != "active" or route not in item.get("routes", []):
            continue
        if item.get("client") not in (client, "*"):
            continue
        if use and item.get("use") != use:
            continue
        try:
            path = resolve_reference(item['path'], root)
            relative = path.relative_to(root.resolve())
        except (OSError, ValueError, KeyError, TypeError):
            continue
        if relative.parts[0] == 'clients':
            if item.get('client')=='*':continue
            if len(relative.parts)==2:
                if relative.stem!=client:continue
            elif relative.parts[1]=='current':
                if relative.stem!=client:continue
            elif relative.parts[1]!=client:continue
        if any(part in ("evals", ".local", "history") for part in relative.parts) or not path.is_file():
            continue
        # Legacy metadata indexes contain text references only. Binary originals
        # belong to the audited ingestion registry and the public RAG API.
        if item.get('extraction_path') or path.suffix.lower() not in {'.md','.txt'}:
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
    p.add_argument("--use", choices=("guidance", "positive", "negative", "structure", "original"))
    p.add_argument("--index", action="append", default=[])
    p.add_argument("--limit", type=int, default=4)
    p.add_argument("--source", action="append", default=[])
    p.add_argument("--page",type=int)
    p.add_argument("--section")
    p.add_argument("--engine", choices=("auto","lexical","semantic","hybrid","metadata"), default="auto")
    a = p.parse_args()
    if a.limit < 1 or a.limit > 20:
        p.error("limit must be 1..20")
    if a.index or a.engine=='metadata':
        if a.source or a.page is not None or a.section is not None:
            p.error('--source/--page/--section require the audited public RAG; metadata indexes do not support these filters')
        if a.index and a.engine not in {'auto','metadata'}:
            p.error('Explicit indexes preserve metadata scope; use --engine metadata. Public RAG never embeds client files.')
        entries=load_entries(a.index)
        result=retrieve(a.query,entries,a.route,a.client,a.use,a.limit)
        payload=dict(results=result,engine_used='metadata',note='Explicit indexes preserve their scope. Open full sources; ranking is not factual validation.')
    else:
        from rag_search import Retriever
        try:payload=Retriever().search(a.query,a.route,a.client,a.use,a.limit,a.engine,source_ids=a.source,page=a.page,section=a.section)
        except (OSError,ValueError,KeyError,TypeError) as exc:
            payload=dict(results=[],engine_used='unavailable',error=str(exc),note='Invalid public corpus; no client fallback was attempted.')
            print(json.dumps(payload,ensure_ascii=False,indent=2));raise SystemExit(1)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
