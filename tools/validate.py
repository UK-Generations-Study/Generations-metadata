"""Check the data dictionary. Runs locally and on every push (GitHub Actions).

Checks:
  1. Every .json file in the repository parses.
  2. Every file under variable-level-metadata/schemas/ is a valid JSON Schema (draft 2020-12)
     and every $ref in it resolves to a file in that folder.
  3. ro-crate-metadata.json: IDs are unique, every "#..." link points to an entity in the graph,
     and every local file the graph names exists.
  4. The generated pages and VERSIONS.json are up to date (python tools/build_docs.py --check).

Usage:  python tools/validate.py      (exit code 1 if anything fails)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_docs as bd  # noqa: E402

ROOT = bd.ROOT


def check_json(errors: list):
    for p in sorted(ROOT.rglob("*.json")):
        if ".git" in p.parts:
            continue
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except ValueError as e:
            errors.append(f"invalid JSON: {p.relative_to(ROOT).as_posix()}: {e}")


def check_schemas(errors: list) -> int:
    ss = bd.SchemaSet(bd.SCHEMAS)
    for p, doc in ss.docs.items():
        name = p.relative_to(ROOT).as_posix()
        if not isinstance(doc, dict):
            errors.append(f"not a JSON Schema (data or other JSON?): {name}")
            continue
        try:
            Draft202012Validator.check_schema(doc)
        except SchemaError as e:
            errors.append(f"not a valid JSON Schema: {name}: {e.message[:200]}")
        for ref, src in ss.refs_in(doc, p, []):
            try:
                ss.resolve(ref, src)
            except (KeyError, IndexError, ValueError) as e:
                errors.append(f"unresolved $ref in {name}: {ref} ({e})")
    return len(ss.tables())


def links(node, found: list):
    """Every {"@id": ...} reference nested inside an entity's properties."""
    if isinstance(node, dict):
        if set(node) == {"@id"}:
            found.append(node["@id"])
        for k, v in node.items():
            if k != "@id":
                links(v, found)
    elif isinstance(node, list):
        for v in node:
            links(v, found)
    return found


def check_crate(errors: list) -> int:
    graph = json.loads(bd.CRATE.read_text(encoding="utf-8"))["@graph"]
    ids = [e.get("@id") for e in graph]
    for i in {i for i in ids if ids.count(i) > 1}:
        errors.append(f"ro-crate: duplicate @id {i}")
    known = set(ids)
    for e in graph:
        for target in links(e, []):
            if target.startswith("#") and target not in known:
                errors.append(f"ro-crate: {e['@id']} links to {target}, which is not in the graph")
        local = e["@id"]
        if not local.startswith(("#", "./")) and "://" not in local and local != "ro-crate-metadata.json":
            if not (ROOT / local).exists():
                errors.append(f"ro-crate: {local} is named in the graph but does not exist")
    return len(graph)


def main() -> int:
    errors: list[str] = []
    check_json(errors)
    n_tables = check_schemas(errors)
    n_entities = check_crate(errors)
    errors += bd.stale(bd.generate())
    print(f"Released tables: {n_tables}. Resource graph entities: {n_entities}.")
    if errors:
        print(f"{len(errors)} problem(s):")
        for e in errors:
            print("  -", e)
        if any(e.startswith("out of date") for e in errors):
            print("Generated files: run python tools/build_docs.py")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
