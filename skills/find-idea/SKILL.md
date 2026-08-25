---
name: find-idea
description: Find or sharpen a startup product idea by mining the internet for evidence that real people are already paying to escape a specific pain. Use when the user has no idea yet and wants somewhere to start, when the user has an idea that is still vague and needs sharpening or narrowing, or when the user says "find me a startup idea" / "what should I build" / "brainstorm product ideas" / "is anyone actually paying for this" / "help me find a niche". Runs upstream of phase 0 of the solo-sdlc pipeline and hands a shortlist to product-critic at phase 1.
---

# find-idea — evidence first, idea second

Most idea brainstorming runs backwards. It invents plausible products, then goes looking for
support. A language model is extremely good at the inventing half, which is exactly the
problem: the output is fluent, confident, and indistinguishable from a real finding.

This skill runs the other direction. **Collect dated, quoted, linked complaints from real
people first. Cluster them. An idea is only ever allowed to exist as the answer to a cluster.**
If a candidate did not come out of something somebody actually wrote, it does not go in the
shortlist — no matter how good it sounds.

The target is a pain that (a) many people have, (b) somebody is **already paying** to escape,
and (c) is either unserved, badly served, or newly serveable. **Not** a pain nobody has
addressed — an untouched market is usually untouched because it is not a market.

## Two modes

Detect from what the user said; ask one question only if genuinely unclear.

- **Cold start** — no idea at all. Start by choosing *hunting grounds*, not ideas.
- **Fog** — an idea exists but is vague. Take it as a search hypothesis, not a conclusion.
  The usual outcome is that the idea survives **narrowed** to a segment it wasn't aimed at,
  splits into sharper variants, or dies while the search surfaces the real pain next door.
  All three are wins. Say which one happened, bluntly.

Run market-first. Do not interview the user about their skills, budget or audience — if they
volunteered constraints, honour them; otherwise let the evidence decide and let
`product-critic` test founder fit at phase 1.

## Workflow

### 1 · Frame the search

**Cold start** — pick **3–5 hunting grounds**. A hunting ground is not an idea; it is a
specific occupation or workflow where all three hold:

1. **Money already moves** — the people there have budgets, invoices, or salaries attached.
2. **They complain in public** — there is a searchable board, sub, or review corpus. A
   profession that only talks in private Slacks cannot be mined and cannot be sold to either.
3. **It is boring** — unglamorous enough that funded teams skip it. Glamour attracts capital,
   capital attracts competition, and one person loses that race.

Bias toward operational back-office work, regulated paperwork, trades and field services,
niche professional practices, and long-tail plugin ecosystems. Pick grounds that don't overlap
so the lanes don't return the same thing four times.

**Fog** — decompose the user's idea into: problem · who has it · mechanism · why now. Turn
each blank or shaky one into a search question. Then hunt the *problem*, never the solution —
searching for the product they imagined only ever finds competitors.

Show the grounds or the search questions in three lines and let the user redirect once. This
is a checkpoint, not a gate — proceed if they say nothing useful. Redirecting is cheap here
and expensive after the fan-out.

### 2 · Fan out — four scouts, one lane each, in parallel

Spawn four subagents concurrently. Each owns one lane and returns **evidence records only** —
no ideas, no recommendations, no synthesis. Give every scout this prompt shape:

```
You are scout for LANE <n> of a market-evidence sweep. Read <skill>/references/sources.md,
YOUR LANE SECTION ONLY, plus "Evidence record schema" and "Source hygiene".

Hunting grounds: <list>          (fog mode: search questions instead)

Return 8-15 evidence records in the exact schema. Rules:
- Every record needs a real URL you actually fetched, a date from the page, and a verbatim
  quote of <=40 words. Never invent a URL. Unfetchable page -> write FETCH FAILED.
- Records only. If you catch yourself proposing a product, stop and go back to searching.
- Report the queries you ran, including the ones that returned nothing.
- Get the `pays` tier right - it decides whether this survives.
```

Web search and fetch are mandatory. Use a browsing or scraping skill (`/browse`, `/scrape`) if
one is installed — review sites and pricing pages often need a real browser. The Hacker News
Algolia API returns dated JSON and is worth scripting rather than scraping.

### 3 · Cluster

Group records by **job to be done**, not by tool or by industry. *"Reconcile payouts against
orders every month"* is a cluster; *"Shopify apps"* is not.

Drop any cluster with fewer than **3 records** or drawn from fewer than **2 lanes**. A cluster
living entirely in lane 1 is people being annoyed, which is not a business.

Name each surviving cluster in the customer's own vocabulary, lifted from the quotes.

### 4 · Verify — one pass per surviving cluster, in parallel

This is where confident nonsense dies. For each cluster, a subagent confirms:

- **Competitors** — who exists, at what price, taken from the **actual pricing page**, quoted
  and dated. Then the shape (see `references/screening.md` §2).
- **The wedge, quantified** — if the shape is "crowded but badly reviewed", count it: how many
  sub-4-star reviews name the same axis, out of how many.
- **The why-now** — a date, or it does not exist.
- **Platform risk** — if the idea rides a platform, read that platform's public roadmap and
  changelog. Building a line item on someone's roadmap is building it for them, free.
- **Every quote from step 2** — re-fetch a sample. A single fabricated citation invalidates
  the run; catching it here costs minutes, catching it at phase 1 costs credibility.

### 5 · Score and cut

Read `references/screening.md` in full, then apply it: the willingness-to-pay ladder, the
competition shapes, the solo+AI kill flags, the default-reject patterns, and the scorecard.

Hard gates beat totals. **A cluster with no T1/T2 payment evidence does not reach the
shortlist**, however loud the complaining. Below 14/24, or any axis at zero, or any unresolved
kill flag → graveyard, with the reason recorded.

### 6 · Write it up

Copy `templates/idea-scan.md` to `<scratch>/idea-scan-YYYY-MM-DD.md` and fill it in.
Scratch means a working directory outside any repo — **do not `git init`, do not create a
project.** A repo is the artifact of deciding to build, and nothing has been decided yet.
When phase 1 later returns GO, the scan moves into `docs/business/` beside the validation.

The graveyard section is not filler. It is what stops the next run re-walking the same forty
dead clusters, and it is the evidence that the shortlist was subtracted rather than invented.

### 7 · Present and hand off

Show 2–3 candidates plus the graveyard summary. Then stop — picking is the human's call, and
nothing downstream should start on its own.

Handoff is `/solo-sdlc:validate <the pitch paragraph>`, which spawns `product-critic` for the
real attack at phase 1. On GO, the pipeline continues at phase 0 triage.

## How many candidates

Default **2–3**. One is a fine answer. **Zero is a fine answer** — fill in *Nothing cleared the
gates*, report what the evidence actually said, and propose the next hunting grounds. More than
three only when a ground was unusually rich, and cap at five.

Padding the list is the single most expensive failure available here, because the cost is not
tokens — it is the weeks the human spends building the filler.

## Hard rules

- **No quote, no idea.** Every candidate traces to ≥3 fetched, dated, quoted records from ≥2
  lanes. Writing an idea you did not read in somebody's complaint means deleting it.
- **Never fabricate a URL, a price, a review count, or a date.** `FETCH FAILED` and "could not
  verify" are acceptable results. An invented citation is not, and it survives into every
  downstream artifact where it is far more expensive to catch.
- **Somebody must already be paying.** Money to a competitor, money to a human, or hours from
  a role that controls a budget. *"I'd pay for this"* is a sentence, not evidence.
- **An empty market is a red flag until explained.** Invoke one of the four legitimate
  explanations in `references/screening.md` §2, with evidence, or send it to the graveyard.
- **A why-now that is "AI can do this now" is not a why-now.** Everyone has that enabler,
  which is why those spaces close within a quarter. Date it or drop it.
- **Report the empty lanes.** A lane that found nothing is a finding about the market, and
  hiding it makes a thin sweep look thorough.
- **Do not do `product-critic`'s job.** No TAM model, no full unit economics, no risk register,
  no verdict. Broad and shallow here; deep and adversarial there, on one idea, at phase 1.
- **Do not write code, scaffold, or create a repo.** This runs upstream of everything.
