"""Check the Generations metadata repository. Runs locally and on every push (GitHub Actions).

Checks:
  1. Every .json file in the repository parses.
  2. Every file under structural-metadata/schemas/ is a valid JSON Schema (draft 2020-12)
     and every $ref in it resolves to a file in that folder.
  3. ro-crate-metadata.json: IDs are unique, every "#..." link points to an entity in the graph,
     and every local file the graph names exists.
  4. Generations-specific terms: every term a JSON-LD file maps to the gs: prefix is defined in that file,
     and no term is defined differently in two files.
  5. The generated pages and VERSIONS.json are up to date (python tools/build_docs.py --check).

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


def check_terms(errors: list) -> int:
    entries = bd.collect_terms()
    meaning: dict[str, tuple[str, str]] = {}
    for t, src in entries:
        label, comment = bd.term_label(t), t.get("rdfs:comment", "")
        if label in meaning and meaning[label][0] != comment:
            errors.append(f"term '{label}' is defined differently in {meaning[label][1]} and {src}")
        meaning.setdefault(label, (comment, src))
    for path in (bd.STUDY_RECORD, bd.CRATE):
        doc = json.loads(path.read_text(encoding="utf-8"))
        defined = {bd.term_label(e) for e in doc.get("@graph", []) if bd.is_term(e)}
        for ctx in bd.as_list(doc.get("@context")):
            if isinstance(ctx, dict):
                for key, value in ctx.items():
                    if isinstance(value, str) and value.startswith("gs:") and value[3:] not in defined:
                        errors.append(f"term '{value[3:]}' is used in {path.name} but not defined there")
    return len({bd.term_label(t) for t, _ in entries})


def main() -> int:
    errors: list[str] = []
    check_json(errors)
    n_tables = check_schemas(errors)
    n_entities = check_crate(errors)
    n_terms = check_terms(errors)
    errors += bd.stale(bd.generate())
    print(f"Released tables: {n_tables}. Resource graph entities: {n_entities}. Generations-specific terms: {n_terms}.")
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
