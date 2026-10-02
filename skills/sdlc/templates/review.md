# Review: <what was reviewed> — <date>

Reviewer: <agent or person> · Scope: <HEAD sha> <commit range / files>

Every finding goes in exactly one bucket. Mark a must-fix-before-merge finding by starting it with
`BLOCKING:` (any case); when fixed, the reviewer who raised it appends `[resolved]` on the same line.
The gate scans every `##` section except `## Return summary`, headings included: a line there with
the marker (uppercase `BLOCKING`, or `blocking:` with a colon in any case) and no `[resolved]` fails
it. Prose like "no blocking issues found" is not a marker. Write the marker only on a must-fix line.
The first token after `Scope:` is the commit you reviewed (`git rev-parse HEAD`): `--require-review`
counts this file only when that SHA counts for the gated SHA.

Act on: every `BLOCKING:` line, none dropped or moved for the cap; then up to 5 other items,
highest value first; the rest go to Consider.

## Act on
<must-fix lines first, then the capped items, as described above>

- <finding, location, fix>

## Consider
- <worth doing if cheap; say what it would cost>

## Noted
- <true but no action now>

## Dismissed
Each item needs a reason, so the same finding is not re-raised.

- <finding> — dismissed because <reason>

## Return summary
<≤15 lines handed back to the main session: verdict, count per bucket, every must-fix line,
the top Act-on items, and nothing else. Not scanned by the gate; the Act on lines are the record.>

```
verdict: <pass | pass with fixes | fail>
act-on: <n>  consider: <n>  noted: <n>  dismissed: <n>
must-fix:
- <…>
top actions:
1. <…>
```
