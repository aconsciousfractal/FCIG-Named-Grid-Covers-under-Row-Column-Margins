# Repository experiment ledger

Date: 2026-07-27  
Scope: standalone Output T repository assembly and T-11 closure.

Failed, aborted, or inconclusive runs are retained. Volatile timings and raw
stdout/stderr belong in `results/verification_run.json`; stable receipts carry
normalized commands and hashes.

| ID | Route | Command / operation | Environment | Result | Outputs / note |
| --- | --- | --- | --- | --- | --- |
| T-EXP-00 | package assembly | mechanical export from accepted T-08/T-10 material | local filesystem | PASS | standalone source tree prepared on local `main`; replay is remote-independent and policy permits only the canonical GitHub remote when present |
| T-EXP-01 | clean environment | `python -m pip install -r requirements.txt` | CPython 3.12.13 | PASS | `pypdf==6.14.2`, `python-flint==0.9.0`, `sympy==1.14.0` |
| T-EXP-02 | manuscript build | `tectonic main.tex --outdir . --keep-logs --reruns 2 --only-cached` | Tectonic 0.16.9 Windows MSVC archive SHA-256 `131a24604785a9600989a3d91225f597df52ac06f00aeffe86fd529f99ee5cdd` | PASS | accepted 18-page PDF and stable build log |
| T-EXP-03 | visual PDF QA | Poppler `pdftoppm` render and inspection of every page | 150 dpi PNG | PASS | all 18 pages inspected; zero layout defects found |
| T-EXP-04 | manifest profile | `python -X utf8 -B scripts/verify.py --profile manifest` | locked environment | PASS | manifest bytes, sizes, realpaths, category coverage, import closure, and semantic anchors |
| T-EXP-05 | core replay | `python -X utf8 -B scripts/verify.py --profile core` | locked environment | PASS | 73 s observed; manuscript, C32, C46, residual-area, P21 smoke, repository policy |
| T-EXP-06A | full replay preflight | `python -X utf8 -B scripts/verify.py --profile full` | locked environment | ABORTED / INCONCLUSIVE | stopped after 447 s when T-11 edits intentionally made the starting manifest obsolete; no mathematical failure observed and no PASS claimed |
| T-EXP-06B | full acceptance replay | `python -X utf8 -B scripts/verify.py --profile full` | locked environment | RECEIPT-GATED | must end PASS on the final current manifest; authoritative result is `results/verification.json` |
| T-EXP-07 | repository policy | `python -X utf8 -B scripts/validate_repository.py` | locked environment | PASS | fail-closed structural/public-boundary receipt |
| T-EXP-08 | final red team | `python -X utf8 -B scripts/verify_final_red_team.py` | locked environment | RECEIPT-GATED | must pass twice without source changes; authoritative result is `results/final_red_team_verification.json` |

`RECEIPT-GATED` is not a substituted result: the final verifier rejects a
missing or failed receipt and rejects a full receipt bound to any older
`certificates/MANIFEST.json` digest.
