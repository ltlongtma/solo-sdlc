# Review: <what was reviewed> — <date>

Reviewer: <agent or person> · Scope: <commit range / files>

Every finding goes in exactly one bucket. Mark a must-fix-before-merge finding with `BLOCKING`;
when fixed, append `[resolved]` on the same line. An unresolved `BLOCKING` line fails the gate.

## Act on
<≤5 items, highest value first.>

- BLOCKING — <finding, location, fix> 
- <finding, location, fix>

## Consider
- <worth doing if cheap; say what it would cost>

## Noted
- <true but no action now>

## Dismissed
Each item needs a reason, so the same finding is not re-raised.

- <finding> — dismissed because <reason>

## Return summary
<≤15 lines handed back to the main session: verdict, count per bucket, every BLOCKING line,
the top Act-on items, and nothing else.>

```
verdict: <pass | pass with fixes | fail>
act-on: <n>  consider: <n>  noted: <n>  dismissed: <n>
blocking:
- <…>
top actions:
1. <…>
```
