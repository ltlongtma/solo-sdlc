# Artifact format contract — parsed by scripts/check-spec.py, check-plan.py, check-gate.py

All parsing is line-based markdown. Section = `## <Heading>` up to next `## `. Heading match is
case-insensitive prefix (e.g. `## Acceptance checklist — REQUIRED…` matches "Acceptance").

## Spec (`docs/specs/<slug>.md`)

Header bullets (top of file, before first `##`):
- `- **Design source:** <path or url | none>`   → "set" means present and value not `none`/empty/`<…>`
- `- **UI:** yes | no`                            → UI spec if `yes`, or Design source set

`## Requirements` — markdown table. Every data row (not header/separator) must have first cell `R<n>`.

`## Acceptance` section — every checkbox line (`- [ ]` / `- [x]`) must look like:
    - [ ] **A1** (R1) — <exact check> — Verify by: e2e
  - must contain `**A<n>**`
  - must contain `Verify by: e2e|integration|unit|human-B` (exactly one of these words)
  - A-ids unique.
  - any other line in the section containing `**A<n>**` (e.g. `* [ ]`, plain text) is an error, so
    an id can never silently drop out of the gate. Scripts find the id with `**A<n>**` anywhere on
    the checkbox line.

`## UI states` — table `| Screen | State | Viewport | Mockup ref |`. If UI spec: ≥1 data row
containing no `<` … `>` placeholder.

Placeholder = any `<…>` text, e.g. `<feature name>`.

## Plan (`docs/plans/<date-slug>.md`)

Header bullet: `- **Spec:** \`docs/specs/<slug>.md\`` (scripts also accept `--spec PATH`, which wins).

Tasks: each `### Task <N> — <name>` heading (N integer, Task 0 allowed). UI spec → must have
`### Task 0 — Verification harness`. Each task block (until next `###`/`##`) must contain bullets:
- `- **Covers:** A1, A3`           (A-ids; Task 0 may say `harness`)
- `- **Files:** \`a\`, \`b\``       (1–3 comma-separated entries)
- `- **Test (red → green):** …`    (field name starts with `Test`)
- `- **Verify:** <exact command>`
- `- **Tier:** strong | standard | fast`
- `- **Risk flags:** none | money, auth, …`   (anything other than `none`/empty ⇒ Tier must be strong)

`## Task status` lines:
    - [x] Task 1 — <name> — `abc1234`
    - [ ] Task 2 — <name> — `<commit>`
Ticked (`[x]`) line must carry a backticked hex hash (7–40 chars) that `git cat-file -e <hash>^{commit}` resolves.

## Test titles

A test proves acceptance `A<n>` when its title contains literal `[A<n>]`, e.g. `test('[A3] rejects empty title', …)`.
Acceptance tests are written first as `test.fixme('[A3] …')`.
`Verify by: e2e` must be proven by a test in a Playwright JSON report; `unit`/`integration` by a
test in a Vitest JSON report. A Vitest report fails the gate when `success` is not `true` or any
`testResults[]` file `status` is not `passed`.

## Gates (`docs/gates.md`)

    ## G1 — <question>
    - **Options:** a | b
    - **Default:** a
    - **Blocks:** A4, Task 3
    - **Answer:** <empty until human answers>
A gate block runs from one `##`/`###`(or deeper) heading to the next; `Blocks`/`Answer` reset per block.
A `human-B` acceptance A<n> is answered when some gate block lists A<n> in `Blocks:` and its
`Answer:` is not empty, `TBD` (any case), `-`, `?`, or a `<…>` placeholder.

## Reviews (`docs/reviews/*.md`)

Bucket headings `## Act on`, `## Consider`, `## Noted`, `## Dismissed`. Only lines inside these four
sections are scanned (preamble and `## Return summary` are prose). A scanned line containing the word
`blocking` in any case (not `non-blocking`) is unresolved unless it contains the literal token
`[resolved]`; `RESOLVED` or `resolved` alone does not count. `check-gate --reviews` is required.
A review file with none of the four bucket headings fails the gate ("not in review format") — fail
closed, since findings outside the buckets are never scanned. Every reviewer agent writes its report
in this format: agent-specific summary (verdict, options, matrix) in the preamble, every finding in
exactly one bucket, a must-fix finding in `## Act on` with `BLOCKING` on its line, every Dismissed
item with a reason.

## Ledger (`docs/qa/ledger.tsv`)

Header: `acceptance_id\tsha\tverdict\tevidence\tverifier\tdate`. verdict `live-ui-verified` (or `fail`).
A row at SHA S counts for `check-gate --sha H` when S and H prefix-match (≥7 hex chars), or S
resolves in git and `git diff --quiet S H -- . ':!docs/'` reports no change (only docs/ changed since
QA). The last counting row per A-id wins. CI passes the PR head SHA and checks out full history.

## Output convention for all check-*.py

Python 3 stdlib only. One `path:line: problem` per failure on stdout, exit 1 if any failure, 0 otherwise.
Warnings print `path:line: warning: …` and do not change exit code. `--help` works.
