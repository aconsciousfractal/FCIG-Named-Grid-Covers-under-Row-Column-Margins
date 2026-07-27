#!/usr/bin/env python3
"""Fail-closed static closure audit for project-local reviewer imports."""
from __future__ import annotations

import argparse
import ast
import json
import re
from collections import deque
from pathlib import Path, PurePosixPath


def _inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _resolve_module(project: Path, source: Path, module: str) -> list[Path]:
    parts = module.split(".") if module else []
    candidates: list[Path] = []
    for base in (source.parent, project):
        stem = base.joinpath(*parts)
        candidates.extend((stem.with_suffix(".py"), stem / "__init__.py"))
    return [path.resolve() for path in candidates if path.is_file() and _inside(path.resolve(), project)]


def _relative_base(source: Path, level: int) -> Path:
    base = source.parent
    for _ in range(max(0, level - 1)):
        base = base.parent
    return base


def _python_dependencies(project: Path, source: Path) -> tuple[set[Path], list[str]]:
    tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
    dependencies: set[Path] = set()
    dynamic: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                dependencies.update(_resolve_module(project, source, alias.name))
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if node.level:
                base = _relative_base(source, node.level)
                stem = base.joinpath(*module.split(".")) if module else base
                candidates = (stem.with_suffix(".py"), stem / "__init__.py")
                dependencies.update(
                    path.resolve()
                    for path in candidates
                    if path.is_file() and _inside(path.resolve(), project)
                )
                for alias in node.names:
                    child = stem / f"{alias.name}.py"
                    if child.is_file() and _inside(child.resolve(), project):
                        dependencies.add(child.resolve())
            else:
                dependencies.update(_resolve_module(project, source, module))
                for parent in _resolve_module(project, source, module):
                    package = parent.parent if parent.name == "__init__.py" else None
                    if package is not None:
                        for alias in node.names:
                            child = package / f"{alias.name}.py"
                            if child.is_file():
                                dependencies.add(child.resolve())
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            value = node.value.replace("\\", "/")
            if value.endswith(".py") and not re.match(r"^[A-Za-z]+://", value):
                for candidate in (source.parent / value, project / value):
                    if candidate.is_file() and _inside(candidate.resolve(), project):
                        dependencies.add(candidate.resolve())
        elif isinstance(node, ast.Call):
            name = ""
            if isinstance(node.func, ast.Name):
                name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                name = node.func.attr
            if name in {"__import__", "import_module", "run_module", "run_path"}:
                dynamic.append(f"{source.relative_to(project).as_posix()}:{node.lineno}:{name}")

    return dependencies, dynamic


def audit(project: Path, manifest: dict) -> dict:
    project = project.resolve(strict=True)
    declared = {row["path"] for row in manifest["artifacts"]}
    roots = deque()
    for raw in sorted(declared):
        posix = PurePosixPath(raw)
        path = project.joinpath(*posix.parts)
        if path.suffix == ".py":
            roots.append(path.resolve())

    visited: set[Path] = set()
    edges: set[tuple[str, str]] = set()
    missing: set[str] = set()
    dynamic: list[str] = []
    while roots:
        source = roots.popleft()
        if source in visited:
            continue
        visited.add(source)
        dependencies, source_dynamic = _python_dependencies(project, source)
        dynamic.extend(source_dynamic)
        source_rel = source.relative_to(project).as_posix()
        for dependency in sorted(dependencies):
            dependency_rel = dependency.relative_to(project).as_posix()
            edges.add((source_rel, dependency_rel))
            if dependency_rel not in declared:
                missing.add(dependency_rel)
            roots.append(dependency)

    return {
        "declared_python_files": sum(path.endswith(".py") for path in declared),
        "dynamic_import_sites": sorted(set(dynamic)),
        "edges": len(edges),
        "missing_project_local_files": sorted(missing),
        "schema": "p42.output-t.import-closure.v1",
        "status": "PASS" if not missing and not dynamic else "FAIL",
        "visited_project_local_files": len(visited),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    result = audit(args.project, manifest)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())