# Third-party notices

## Source geomagic specimens

The C32, C46, P49, and P21 source geometries are attributed to Lee Sallows and
the source records identified in `docs/SOURCE_LOCK.md`. No original raster or
page image is included. The replay begins from explicit, source-locked discrete
cell masks and checks the P42 normalization and downstream computations.

## Imported literature

The paper cites prior work in discrete tomography, tile reconstruction,
reconfiguration, exact covers, algebraic statistics, and Markov bases. These
works are not bundled, copied, or relicensed. Bibliographic identifiers and
the exact import/contribution boundary appear in the manuscript and
`docs/THEOREM_LEVEL_PRIOR_ART_AUDIT.md`.

## Dependencies

This package uses CPython and the separately distributed `pypdf`, `sympy`, and
`python-flint` packages. Their own licenses apply. No dependency source is
vendored here.

## External review material

The T-08 packet is preserved to document findings and remediation. It is an
advisory review artifact, not a source, proof, priority certificate, or
publication approval.

Computational-agent handoffs supplied by the owner and adopted into the P42
codebase are governed by `LICENSE_SCOPE.md`; they are not bundled as an
unreviewed third-party dependency. The preserved review packet remains outside
any broader relicensing claim.
