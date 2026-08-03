# Source and normalization lock

## Source authority

Lee Sallows is the source authority for the underlying C32, C46, P49, P26, and P21
geomagic specimens and displayed arrangements. The primary article is:

- Lee Sallows, “Geometric Magic Squares”, *The Mathematical Intelligencer* 33
  (2011), 25–31, DOI `10.1007/s00283-011-9229-0`.

The official Sallows gallery and Peter Cameron's 21 January 2011 finite
group-action discussion provide adjacent source context. Exact source records,
retrieval metadata, and local normalization checks are preserved in:

- `registry/c32_source_lock.json`;
- `registry/c46_source_lock.json`;
- `packages/package_c_comparative_hypergraphs/specimens/p49_locked.json`;
- `packages/package_c_comparative_hypergraphs/specimens/p26_locked.json`;
- `packages/package_c_comparative_hypergraphs/specimens/p21_locked.json`;
- `reports/C32_SOURCE_AUDIT.md`;
- `reports/C46_SOURCE_AUDIT.md`.

No source raster bytes are redistributed. A repository replay is an
independent downstream enumeration from a frozen normalized transcription: it
begins after the source images have been transcribed into explicit finite cell
masks. It checks those masks, their normalization contracts, exhaustive finite
computations, and the paper's deductions; it does not independently reacquire,
segment, or retranscribe the source images.

The P26 lock has SHA-256
`2732d9400d3a02eb889799306f51985fa765c3106214e01e36ddfadc8c06a35e`.
That digest is also the P26 input anchor in
the residual-area verification certificate; the executable producer and the
specimen validator are mandatory replay steps.

## Normalization lock

- The target and pieces are finite subsets of `Z^2`.
- Allowed orientations are explicit lattice automorphisms; duplicate masks are
  identified.
- C32 and C46 selected rows use unique area labels; P49 and P21 use zero-based
  locked piece indices because areas repeat.
- The canonical repair graph changes exactly two named placements.
- Largest-piece ties use the paper's canonical eligibility rule.
- The public parameter name is **largest-piece residual area**. Legacy
  `coarea_*` filenames are stable artifact identifiers only.

## Imported theorem boundary

Discrete tomography, polyatomic/tile reconstruction, domino tomography,
infeasible-state reconfiguration, locked pair recombination, toric tiling
connectivity, Markov bases, indispensable fibers, and invariant/equivariant
Markov methods are prior art. The paper imports only cited context and standard
tools at their stated hypotheses. `THEOREM_LEVEL_PRIOR_ART_AUDIT.md` records
the theorem-by-theorem relation.

## Not source-authorized

- priority or firstness;
- a complete P21 Markov basis or exact degree;
- reconstruction of Sallows' raster art;
- continuous/polygonal C34 geometry;
- a theorem for arbitrary tile-tomography models.
