# Verification architecture

The release uses a fail-closed manifest plus three replay profiles. The design
separates mathematical recomputation from packaging checks and keeps generated
run diagnostics outside the frozen payload.

## Trust boundary

The replay starts from source-locked normalized cell models. It does not
reproduce raster acquisition, segmentation, or transcription, and it is not an
independent external reproduction. Mathematical certificates are checked by
implementations that do not import their corresponding producers where that
independence is part of the stated contract.

## Profiles

- `manifest` verifies the environment, containment, symlink policy, byte
  hashes, sizes, import closure, subprocess closure, semantic anchors, and
  public-package policy.
- `core` adds manuscript/PDF consistency, C32 and C46 certificate checks,
  specimen validation, residual-area regeneration, an integrated P21 replay,
  and release-checksum validation.
- `full` adds mutation suites, the complete P21 degree-four and single-block
  audits, and a nested replay from a temporary tree containing only the
  manifest allowlist.

Every profile snapshots frozen artifacts before execution and verifies byte
identity afterward. Stable results are written to `results/verification.json`;
timestamps, durations, commands, stdout, and stderr go to the ignored
`results/verification_run.json`.

## Reproducibility identifiers

Some JSON certificates and Python constants retain a historical namespace.
These are stable machine identifiers required by frozen hashes and script interfaces.
Reader-facing documentation, public claim labels, and the paper use descriptive
names instead.
