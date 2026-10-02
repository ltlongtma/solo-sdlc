# Review: <what was reviewed> — <date>

Reviewer: <agent or person> · Scope: <commit range / files>

Every finding goes in exactly one bucket. Mark a must-fix-before-merge finding by starting it with
`BLOCKING:` (any case); when fixed, append `[resolved]` on the same line. The gate scans only the
four bucket sections below: a marked line there without `[resolved]` fails it. Keep instructions
and the return summary outside those sections.

## Act on
<≤5 items, highest value first. Must-fix items start with the marker described above.>

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
