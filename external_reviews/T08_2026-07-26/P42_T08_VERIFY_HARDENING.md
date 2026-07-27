# Proposed `verify.py` Hardening

This is a **design patch**, not an executed replacement.

## 1. Add a post-run frozen-snapshot check

```python
def snapshot_artifacts(manifest: dict) -> dict[str, tuple[int, str]]:
    out = {}
    for row in manifest["artifacts"]:
        target = safe_manifest_target(row["path"])
        out[row["path"]] = (target.stat().st_size, sha256(target))
    return out
```

In `main()`:

```python
manifest_before, checks = check_manifest()
checks.extend(check_semantics())
manifest_sha_before = sha256(MANIFEST)
snapshot_before = snapshot_artifacts(manifest_before)

commands = run_commands(manifest_before["profiles"][args.profile], args.profile)

manifest_after, post_checks = check_manifest()
post_semantics = check_semantics()
snapshot_after = snapshot_artifacts(manifest_after)

require(sha256(MANIFEST) == manifest_sha_before, "manifest changed during replay")
require(snapshot_after == snapshot_before, "frozen artifact changed during replay")
checks.extend(f"post:{name}" for name in post_checks)
checks.extend(f"post:{name}" for name in post_semantics)
```

## 2. Add realpath containment

```python
PROJECT_REAL = PROJECT.resolve(strict=True)

def safe_manifest_target(raw: str) -> Path:
    posix = PurePosixPath(raw)
    require(not posix.is_absolute(), f"absolute path: {raw}")
    require(".." not in posix.parts, f"escaping path: {raw}")
    target = PROJECT.joinpath(*posix.parts)
    require(target.is_file(), f"missing artifact: {raw}")
    require(not target.is_symlink(), f"symlinked artifact: {raw}")
    resolved = target.resolve(strict=True)
    require(
        resolved == PROJECT_REAL or PROJECT_REAL in resolved.parents,
        f"realpath escape: {raw}",
    )
    return target
```

Apply an equivalent rule to every parent directory, or use a manifest-only
temporary tree.

## 3. Lock dependencies

Before replay:

```python
def dependency_versions() -> dict[str, str]:
    import importlib.metadata as metadata
    names = ["sympy", "python-flint"]
    versions = {}
    for name in names:
        try:
            versions[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            raise RuntimeError(f"missing reviewer dependency: {name}")
    return versions
```

Compare against versions frozen in the manifest/environment lock.

## 4. Make the environment deterministic

```python
environment = {
    **os.environ,
    "PYTHONHASHSEED": "0",
    "TZ": "UTC",
    "LC_ALL": "C.UTF-8",
}
environment.pop("PYTHONPATH", None)
```

## 5. Capture command evidence

```python
completed = subprocess.run(
    command,
    cwd=PROJECT,
    env=environment,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    timeout=TIMEOUTS[command_id],
)
```

Store:

- exact `argv`;
- return code;
- duration;
- stdout/stderr SHA-256;
- dependency versions;
- Python version.

If byte-stable receipts are required, put volatile fields in a separate run
log and keep only their digests in the stable receipt.
