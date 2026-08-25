# Idea scan — <hunting grounds / original idea>

- **Date:** YYYY-MM-DD
- **Mode:** cold start (no idea) | fog (sharpening an existing idea)
- **Hunting grounds searched:** <list>
- **Lanes run:** 1 complaint · 2 review · 3 paid labour · 4 market shift
- **Clusters found:** N → **cleared the gates:** M

> Screened broad and shallow. Nothing here is validated — the shortlist is what survived
> long enough to be worth `product-critic` at phase 1. Pick one; it can still come back NO-GO.

<!-- Mode "fog" only. Delete this block on a cold start. REQUIRED when sharpening an idea. -->
## What you thought vs. what the evidence says

| | Your framing | What the search found |
|---|---|---|
| Problem | | |
| Who has it | | |
| What they use today | | |
| Why now | | |

**Verdict on the original idea:** survives as-is | survives but narrowed to <segment> | splits
into <N> sharper variants | dies — the real pain next door is <X>

<one paragraph, blunt, on what the evidence contradicted>

---

## Shortlist

<!-- One block per candidate. Default 2-3. One is fine. ZERO is fine — see "Nothing cleared". -->

### C1 · <name it in the customer's language, not yours>

**Pitch (one sentence):** <who> can't <do X> without <pain>, so they <current workaround>.

- **Buyer:** <one occupation, one segment — not "SMBs">
- **Shape:** unserved niche | newly possible | unbundling
- **Score:** NN/24 — pain N · frequency N · payment N · reachable N · gap N · why-now N · build N · durable N
- **Kill flags cleared:** <list the ones you checked>

**Evidence** (≥3 records, ≥2 lanes, ≥1 at T1/T2)

| # | Lane | Date | Who | Quote | Pays | Source |
|---|---|---|---|---|---|---|
| 1 | | | | "…" | T? | <url> |
| 2 | | | | "…" | T? | <url> |
| 3 | | | | "…" | T? | <url> |

**What they do today, and what it costs them:** <the workaround + the number>

**Competition** — shape A/B/C/D/E

| Name | Price (from the pricing page, dated) | Why this buyer is unhappy | Source |
|---|---|---|---|

<If shape A (empty market): which of the four legitimate explanations applies, with evidence.
If shape C/D: the wedge axis, quantified — "14 of 31 sub-4-star reviews name the CSV export".
If shape E: when the window opened and when you think it closes.>

**Why now:** <dated enabler or regulatory deadline — never "AI exists now">

**The thin wedge:** <the smallest thing shippable in ≤6 weeks that a buyer would pay for>

**First customers:** <a named community/board/list, with a member count and a URL>

**The one thing that kills it:** <single biggest risk — hand this to `product-critic` first>

**Cheapest next test (≤48h, before any code):** <landing page · 10 DMs in the named community ·
a manual concierge run for one buyer> — **pass criterion:** <a number>

---

### C2 · …

---

## Nothing cleared the gates

<!-- Delete if the shortlist is non-empty. Otherwise this section IS the deliverable. -->

No cluster reached the bar. Padding the list would cost weeks of building, not tokens.

- **What the evidence actually said:** <the honest summary>
- **Closest miss:** <cluster> — failed on <gate>, would need <what evidence to change the verdict>
- **Next hunting grounds worth a run:** <3-5, with why>

---

## Graveyard

Everything looked at and rejected, so the next run doesn't re-walk it.

| Cluster | Best evidence found | Died on | Note |
|---|---|---|---|
| | | payment below T2 / kill flag / crowded+happy / no why-now / default-reject pattern | |

---

## WHAT I CHECKED

- **Searches run:** <the queries, per lane>
- **Sources that returned nothing:** <an empty lane is a finding>
- **FETCH FAILED:** <pages that could not be read — do not silently drop these>
- **Limits of this scan:** <recency, language, paywalled sources, communities not searchable>

---

## Handoff

1. Human picks **one** candidate. (Or none — no candidate is a valid outcome.)
2. `/solo-sdlc:validate <the pitch paragraph>` → `product-critic` attacks it for real:
   TAM, unit economics, distribution, risk, GO/NO-GO.
3. On GO → phase 0 backlog entry, then the pipeline.

This file lives in scratch until phase 1 returns GO. On GO it moves into `docs/business/`
next to the validation, so the repo records what the idea beat.
