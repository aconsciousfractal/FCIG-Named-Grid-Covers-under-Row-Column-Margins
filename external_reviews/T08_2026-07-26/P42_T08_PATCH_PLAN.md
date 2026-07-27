# P42 Output T — Concrete Patch Plan

## A. Manuscript

### A1. Replace title

Current:

```text
Tomographic Exactness and Co-Area Localization for Named Grid Covers
```

Recommended:

```text
Named Grid Covers under Row–Column Margins:
Three Exactness Levels and Largest-Piece Localization
```

### A2. Add source-credit paragraph

Insert in the introduction before the finite-library overview:

```text
The finite C32, C46, and P49 libraries are normalized from
4-by-4 geomagic-square specimens created and displayed by Lee Sallows.
The piece geometries, targets, and displayed arrangements are Sallows's
source material. Our contribution begins with the source-locked discrete
transcription: complete placement and exact-cover censuses, aggregate-margin
fibers, replacement graphs, and the uniform largest-piece localization
theorem. We do not claim authorship of the underlying geomagic specimens.
```

### A3. Add library-level predicate definition

```text
A declared library is universally support-exact, fiber-pure, or
repair-exact when the corresponding predicate holds for every declared
area-compatible selected row.
```

### A4. Harden orientation definition

```text
The supplied orientation set consists of explicitly represented lattice
automorphisms of Z^2 (or, equivalently, explicitly listed integer-cell masks
for every allowed orientation). Each legal pose is one such oriented mask
followed by an integer translation and contained in T.
```

### A5. Replace informal T-TYPE with a formal problem

```text
Implicit Selected-Library Problem(q,h)
Input: a finite target T, a finite named library, an explicit orientation
action of size at most h, an integer Q, and a requested predicate.
Question: does there exist an area-compatible selected named set E whose
canonically selected largest name L(E) satisfies |T|-|L(E)| <= Q and whose
fiber has the requested predicate?
Output variant: a compressed list of exact participation-type count vectors,
with named multiplicities, not a literal expansion of all named selections.
```

Then state and prove:

```text
Type-Isomorphism Lemma.
Two selected residual multisets with the same exact participation-type count
vector yield canonically isomorphic margin fibers, exact-cover subloci,
G^(2) graphs, and G^(<=2) graphs after renaming equal-type names.
```

### A6. Clarify source replay

Add:

```text
The public/reviewer package reproduces the mathematics from the locked
discrete masks. Re-transcription from the original gallery rasters requires
the owner-supplied source bytes matching the published digests and is a
separate provenance audit.
```

## B. Reviewer documentation

### B1. Correct dependencies

Replace “uses only the Python standard library” with a version-locked dependency contract.

Add:

```text
requirements-review.txt
```

containing the exact successful-run versions of:

```text
sympy
python-flint
```

and any other imported non-stdlib package discovered by an import audit.

### B2. Fix checklist

Replace:

```text
complete 94-piece carrier
```

with:

```text
complete 94-row area-compatible carrier over 16 named pieces
```

## C. Verifier hardening

### C1. Run twice around child processes

Required control flow:

```python
manifest_before, checks_before = check_manifest()
semantics_before = check_semantics()
snapshot_before = snapshot_artifacts(manifest_before)

commands = run_commands(...)

manifest_after, checks_after = check_manifest()
semantics_after = check_semantics()
snapshot_after = snapshot_artifacts(manifest_after)

require(snapshot_after == snapshot_before, "frozen artifact drift")
require(sha256(MANIFEST) == manifest_sha_before, "manifest drift")
```

Only then write `PASS`.

### C2. Resolve paths safely

For every artifact:

```python
project_real = PROJECT.resolve(strict=True)
target_real = target.resolve(strict=True)
require(
    target_real == project_real or project_real in target_real.parents,
    f"realpath escape: {raw}",
)
require(not target.is_symlink(), f"symlinked frozen artifact: {raw}")
```

Also reject symlinked parent directories or run in an isolated copy.

### C3. Deterministic environment

Set at least:

```python
PYTHONHASHSEED=0
TZ=UTC
LC_ALL=C.UTF-8
```

Remove or lock `PYTHONPATH`.

### C4. Richer command receipt

Record:

```json
{
  "id": "...",
  "argv": ["..."],
  "exit_code": 0,
  "duration_ms": 1234,
  "stdout_sha256": "...",
  "stderr_sha256": "...",
  "python_version": "...",
  "dependency_versions": {
    "sympy": "...",
    "python-flint": "..."
  }
}
```

Store full logs separately if needed.

### C5. Import closure

Preferred:

1. construct a temporary project tree containing only manifest-pinned files;
2. run the profiles there;
3. fail on any missing import.

Alternative: static/import-trace audit that adds every project-local imported module to the manifest.

## D. Bibliography

Add or harden:

- Lee Sallows, “Geometric Magic Squares”, *The Mathematical Intelligencer* 33 (2011), 25–31. DOI 10.1007/s00283-011-9229-0.
- Lee Sallows, official *Geomagic Squares* gallery, access date and specimen asset descriptors.
- Peter J. Cameron, “Geomagic squares”, 2011, expository group-action context.
- G. T. Herman and A. Kuba, eds., *Discrete Tomography: Foundations, Algorithms, and Applications*, Birkhäuser, 1999.
- M. Chrobak and C. Dürr, “Reconstructing Polyatomic Structures from Discrete X-Rays: NP-Completeness Proof for Three Atoms”, TCS 259 (2001), 81–98.
- Journal metadata for “Tile-Packing Tomography Is NP-hard”, *Algorithmica* 64 (2012), 267–278.
- Full author list and DOI for “On Solution Discovery via Reconfiguration”.
- Tracy Chin, *A Computational Commutative Algebra Approach to Tilings*, after direct full-text review.

## E. Acceptance run

After all patches:

```text
1. rebuild MANIFEST intentionally;
2. run full profile in isolated tree;
3. run post-replay hash comparison;
4. render all PDF pages;
5. rerun bibliography/attribution grep;
6. update T-08 issue log;
7. maintain PC-1 as the only public claim.
```
