# Incident runbook

For the person on call at 2am, who is you. Written to be followed while tired and alone.

Created at the first release from the *Risks + response* section of `docs/business/<idea>-validation.md`,
then updated by what deploying actually taught you. A risk that has happened once and is not in here
is a lesson thrown away.

## Fast facts

| | |
|---|---|
| Production URL | <…> |
| Hosting / dashboard | <…> |
| Database dashboard | <…> |
| Error tracking | <…> |
| Status pages of dependencies | <…> |
| Last known good tag | <…> |

## Kill switches

- **Roll back the deploy:** <the exact command or dashboard action>
- **Disable the expensive path:** <flag / env var that stops LLM or paid API calls>
- **Maintenance mode:** <how>

## Incidents

### <Symptom as you would actually see it, e.g. "site returns 500 on every page">

- **Check first:** <command / dashboard, and what a healthy answer looks like>
- **Most likely cause:** <…>
- **Fix:** <steps>
- **If that fails:** <fallback — usually revert to the last known good tag>
- **Tell whom:** <affected users? payment provider? nobody?>

### <Symptom: cost spike>

- **Check first:** <which dashboard, which metric, what the normal number is>
- **Fix:** <flip the kill switch above, then find the caller>
- **After:** <rate limit / quota to add so it cannot recur>

### <Symptom: data looks wrong after a migration>

- **Check first:** <…>
- **Fix:** <a code revert does NOT undo a migration — state the real data path>

## After any incident

1. Note it below.
2. Add or fix the entry above so the second occurrence is boring.
3. If a test could have caught it, that test is a backlog item before anything else.

| Date | What happened | Root cause | Runbook updated | Test added |
|---|---|---|---|---|
| <…> | <…> | <…> | <…> | <…> |
