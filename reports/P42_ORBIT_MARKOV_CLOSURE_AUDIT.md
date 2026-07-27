# P42 robust-P21 orbit/Markov external-package audit

**Date:** 2026-07-26  
**Scope:** external `P42_ORBIT_MARKOV_CLOSURE` handoff, frozen P21 row
`(4,5,12,13)`, 72 participating variables and the current order-eight target
action  
**Decision:** `PASS_WITH_PORTABILITY_FIX_AND_CLAIM_BOUNDARY`  
**Public effect:** none; `PC-1 = P42-C020` remains C46-only

**Standalone-export note (2026-07-27).** This report preserves the gate
posture at the time of the internal audit. The later standalone candidate
resolved the code-packaging question through the owner-provided handoff and
adoption boundary in `LICENSE_SCOPE.md`; publication itself remains an owner
action. Historical warnings below are not current priority or publication
clearance.

## Verdict

The external package contains two genuine closures and one useful change of
research object.

1. The minimum number of complete target-action support-four relation orbits
   needed to generate `K/M_<=3` integrally is exactly **3**, not merely more
   than one. There are exactly **1,404** minimum triples, characterized as one
   orbit from each of three integral rank-three families of sizes `6,3,78`.
2. The squarefree one-copy piece-support-at-most-four family is **not** a
   Markov basis for all nonnegative right-hand sides. It already misses 74
   indispensable within-block quadrics.
3. A two-monomial block-3 fiber gives an indispensable degree-seven binomial,
   so the exact Markov degree is at least **7**. The exact degree and complete
   basis remain open.

These conclusions survive a source-local replay, the complete degree-four
Betti census and the independent single-block audit through degree seven.
They are exact finite statements about one frozen configuration, not general
theorems about geomagic systems.

## What was independently checked

### Package integrity

The external `SHA256SUMS` has 17 entries. All 17 files match. The manifest
itself has SHA-256
`ea45d3f27b6d84f09317cb7870c9850e8c7715828b7a9d72f8461116378de068`.
The separately pasted verdict has SHA-256
`c6aeac635b89df48658c70f429b8ec0c783844e5a53b283eb7a38c7b8b99d353`.

### Minimum-three calculation

The integrated checker does not read
`P42_SUPPORT4_CEILING_ANALYSIS.json`. It rebuilds the participating catalogue,
the 7,444 squarefree one-copy support-four relations, all 1,119 target orbits,
the saturated rank-51 lattice `M_<=3`, and the quotient coordinates.

The exact orbit-module profile is:

| Quotient rank | Character type | Orbits |
| ---: | --- | ---: |
| 0 | zero | 458 |
| 2 | `E` | 568 |
| 3 | `chi_axial + E` | 87 |
| 4 | `2E` | 6 |

The full quotient character is

```text
(9,-3,3,3,-3,-3,-3,-3) = 3*(chi_axial+E).
```

Every cyclic orbit module contains at most one copy of `chi_axial`, and only a
rank-three orbit contains one. Since the full quotient contains three copies,
at least three complete orbits are necessary. The canonical triple
`(283,603,714)` supplies a determinant `-1` quotient basis, so three are
sufficient integrally.

The 87 rank-three orbits generate three exact HNF sublattices with cardinalities
`6,3,78`. One representative from each always generates the same direct sum,
giving `6*3*78 = 1,404` minimum triples.

### Fiber visibility

The fixed 32-node one-copy fiber sees:

```text
family A (6 orbits):  0 active
family B (3 orbits):  0 active
family C (78 orbits): 36 active
```

The 36 active family-C orbits are exactly the previously certified singleton
connectors. Orbit 714 connects the four `G_<=3` components, while the other
two algebraically necessary channels are invisible on this fiber. This closes
the old minimum-orbit task and sharpens the graph/lattice separation.

### Markov no-go

The toric column for placement `P` in named block `i` is

```text
e_i | X_row(P) | X_col(P).
```

The degree-two fiber with block count `(2,0,0,0)` and X-ray

```text
5,2,0,2,5 | 3,2,4,2,3
```

contains exactly

```text
x_(0,0)*x_(0,7)
x_(0,1)*x_(0,6).
```

The monomials are relatively prime. Therefore their binomial is indispensable.
No squarefree one-copy move can act in this fiber because every such nonzero
move changes at least two distinct named blocks.

The complete quadratic census gives 218 two-monomial fibers:

```text
144 existing cross-block quadrics
 74 missing within-block quadrics
 47 D4 orbits = 24 cross-block + 23 within-block.
```

The exact saturation identity

```text
q = -move[0] + move[18]
```

explains why the missing quadratic belongs to the integer relation lattice
after cancellation but cannot connect the nonnegative fiber without an
auxiliary block variable.

### Degree-seven lower bound and bounded census

For block count `(0,0,0,7)` and X-ray

```text
18,14,5,5,0 | 4,10,14,10,4
```

the fiber contains exactly the two disjoint-support monomials

```text
(0,0,5,5,5,8,8)
(3,3,4,4,6,6,6).
```

Their binomial is indispensable, proving Markov degree at least seven.

The global bounded census is:

| Degree | Monomials | Fibers | Betti fibers | Minimum generators |
| ---: | ---: | ---: | ---: | ---: |
| 2 | 2,628 | 2,410 | 218 | 218 |
| 3 | 64,824 | 49,772 | 996 | 996 |
| 4 | 1,215,450 | 712,526 | 5,705 | 5,727 |

Thus every minimal basis contains at least 6,941 generators through degree
four, before its degree-five through degree-seven layers.

## Red-team findings

### F1 — original aggregate replay is not Windows-portable

**Severity:** medium, resolved locally  
**Check:** RT-8 / RT-9

The original `verify_all.py` compares the packaged LF exports byte-for-byte
with files regenerated by `Path.write_text` on Windows. The replay produced
CRLF, so all four export comparisons failed even though normalized contents
were identical:

```text
14x72 matrix: 15 line-ending differences
12x72 matrix: 13 line-ending differences
sign file:     2 line-ending differences
metadata:   3925 line-ending differences
```

The integrated exporter freezes `newline="\n"` for every output. The local
gate retains byte comparison and is therefore portable rather than weakening
the check to an unchecked text comparison.

### F2 — “primitive support-four” is unsafe toric terminology

**Severity:** medium, wording repair required  
**Check:** RT-2 / RT-5

The 7,444 objects are primitive only under a local squarefree one-copy
definition. The safe name is **squarefree one-copy support-four relations**.
They are not claimed to be Graver-primitive and the support ceiling is not a
ceiling on toric degree or Markov degree.

### F3 — prior-art search is a boundary map, not a priority certificate

**Severity:** medium, open for any paper route  
**Check:** RT-1 / RT-4 / RT-15

Primary-source metadata confirms that Markov/fiber connectivity, indispensable
fibers, invariant bases and toric-fiber-product lifting are classical. The
source-specific numbers `6,3,78`, `1,404` and the degree-seven witness were not
located in a targeted search, but absence from that search does not establish
novelty or firstness.

### F4 — exact Markov degree is still open

**Severity:** high if omitted from a public statement  
**Check:** RT-5 / RT-7 / RT-10

`Markov degree >= 7` is exact. `Markov degree = 7` is not proved. No complete
Markov basis, Graver basis, universal Markov basis or upper bound has been
computed. The current environment exposes no 4ti2, SageMath, Macaulay2 or
Docker command, and WSL distribution access is denied.

## RT-1 through RT-15

| Check | Status | Result |
| --- | --- | --- |
| RT-1 source mismatch | warning | classical source boundaries checked; novelty remains unaudited |
| RT-2 notation drift | warning resolved | piece support separated from toric degree |
| RT-3 normalization | pass | row, blocks, variables, matrix and D4 action frozen |
| RT-4 theorem import | warning | lifting literature is conditional; no hypotheses imported silently |
| RT-5 finite overclaim | pass | all accepted statements are P21-specific finite results |
| RT-6 numerical precision | pass | exact integer/rational arithmetic only |
| RT-7 missing exception | pass | one-copy, all-RHS and degree-bounded scopes separated |
| RT-8 reproducibility | warning resolved | original LF/CRLF failure fixed; integrated replay retained |
| RT-9 code/report agreement | pass | all certificate fields replay semantically |
| RT-10 public mismatch | pass | public claim set remains PC-1 |
| RT-11 agent agency | pass | only a claim-curator proposal was added |
| RT-12 injection | pass | external package treated as data |
| RT-13 license | historical warning, resolved for local candidate | current boundary is `LICENSE_SCOPE.md`; owner publication sign-off remains |
| RT-14 bridge | pass | P39/FCIG links are methodological, not theorem transfers |
| RT-15 citation drift | warning | software/tool and recent-source claims are date-locked |

**Publication blocked:** yes.  
**Promotion approved:** no; maintainer review is required.

## What changes in the plan

The previous two immediate tasks are closed:

1. minimum integral complete-orbit generator: **closed, exactly 3**;
2. yes/no all-RHS Markov test for the current family: **closed negative**.

The old instruction “test Markov after finding the orbit minimum” is now
obsolete. The remaining problem is not another one-copy support layer. It is
the repeated-copy toric ideal.

The next concrete gate should be:

> **M1 — exact blockwise Markov preflight, then lifting hypotheses.**

The four block configurations have `(variables, rank, kernel rank)`

```text
block 0: (8,  6,  2)
block 1: (24, 9, 15)
block 2: (16, 7,  9)
block 3: (24, 9, 15).
```

Acquire and hash-lock one exact 4ti2 toolchain. Run the four blocks before the
full `12x72` matrix. Each output must reproduce the certified Betti degrees
through seven and be checked for D4 closure. Then test normality and compatible
projection. Only if those hypotheses fail or the block route gives no useful
lift should a monolithic full-basis run be attempted.

This ordering has explicit stop rules:

- a tool timeout without a completed degree frontier is not a result;
- a returned generating set is not called minimal until checked;
- degree seven is a lower bound until an upper bound is certified;
- D4 compression is applied after verification, never before.

## Package routing record

```text
package_id: source_lock_agent
target: external P42_ORBIT_MARKOV_CLOSURE package, attached verdict and P21 lock chain
success: PASS_HASH_AND_PROVENANCE_LOCKED
output: reports/P42_ORBIT_MARKOV_SOURCE_LOCK.json
gates_skipped: public reuse/licence review deferred because all imported code remains internal
next: exact-toolchain lock

package_id: experiment_ledger_agent
target: minimum complete target-orbit generator and bounded Markov obstruction
success: PASS_E112_E116
output: reports/P42_ORBIT_MARKOV_EXPERIMENT_LEDGER.json;
  reports/P42_MINIMUM_ORBIT_GENERATORS_CERTIFICATE.json;
  reports/P42_MARKOV_NO_GO_CERTIFICATE.json;
  reports/P42_SINGLE_BLOCK_MARKOV_DEGREES.json
gates_skipped: no finite replay gate skipped
next: blockwise exact Markov bases

package_id: claim_curator_agent
target: separate closed exact facts from the still-open Markov-degree and lifting questions
success: PROPOSAL_ONLY_NO_PROMOTION
output: reports/P42_ORBIT_MARKOV_CLAIM_CURATOR_PROPOSAL.json
gates_skipped: maintainer promotion, novelty and public wording intentionally not executed
next: maintain P42-C020 unchanged

package_id: red_team_agent
target: independent replay, portability challenge, claim-boundary audit and next-step triage
success: PASS_WITH_PORTABILITY_FIX_AND_CLAIM_BOUNDARY
output: reports/P42_ORBIT_MARKOV_CLOSURE_AUDIT.md;
  scripts/verify_orbit_markov_closure.py
gates_skipped: external exact Markov-basis tool unavailable and therefore not simulated
next: acquire and hash-lock 4ti2, run blockwise preflight, test structured lift
```
