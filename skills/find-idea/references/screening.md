# Screening — how a cluster becomes a candidate

Read this at step 5 of `find-idea`, before scoring anything.

The job here is **subtraction**. A shortlist of three is the residue of forty clusters that
died, and the deaths are the value. An idea that survives because nothing was applied to it
has not survived anything.

---

## 1 · The willingness-to-pay ladder

Every evidence record carries a `pays` tier. This is the field that decides survival.

| Tier | What it looks like | Worth |
|---|---|---|
| **T1** | *"We pay $89/mo for <tool> and it still can't do X"* — a named price they already pay | strongest: budget exists, buyer identified, price anchored |
| **T2** | Paying a human: a job posting, an Upwork gig with a budget, a VA task, a productised agency offer | nearly as strong: the budget is approved and the ceiling is public |
| **T3** | Paying with time: *"this takes me four hours every Monday"* from a role whose hourly cost you can estimate | usable, but hours only convert to money when the sufferer controls a budget |
| **T4** | *"I'd pay for this"* / *"is there a tool that…"* | intent, not behaviour. People say this and buy nothing |
| **T5** | Complaint with no payment behaviour of any kind | a vitamin |

**The bar: a cluster reaches the shortlist only with at least one T1 or T2 record, from a
buyer, that you fetched and quoted.** T3 supports; T4 and T5 never carry a cluster on their
own no matter how many of them there are. Fifty people annoyed about something they will not
pay for is fifty people annoyed.

Watch **who** is speaking, not just what they say. The same sentence is T1 evidence from an
operations manager and worthless from a student. If you cannot tell the role from the
artifact, the record does not count.

---

## 2 · Reading the competition

Find the shape first; the shape dictates the verdict.

**A · No competitors — default suspicion, not celebration.** The overwhelmingly common reason
a market is empty is that it is not a market. An empty space survives screening only with an
explicit, evidenced explanation, and there are exactly four that hold up:

1. **The enabler is new** — a capability or cost curve crossed a threshold recently. Date it,
   and say what specifically changed. *"AI exists now"* is not this (see the fake why-now).
2. **A rule changed** — name the regulation and its effective date.
3. **Too small for funded teams, fine for one person** — the segment tops out somewhere in the
   low hundreds of thousands of ARR. Show the arithmetic: buyers × plausible price.
4. **The buyers are genuinely hard to reach**, so nobody bothered — and you must then name the
   channel that reaches them anyway, or this reason kills the idea instead of saving it.

No explanation from that list → graveyard. Write down which one you invoked; `product-critic`
will attack it at phase 1.

**B · Crowded and well reviewed** → skip. You will not out-execute five funded teams with
happy customers.

**C · Crowded and consistently badly reviewed on ONE axis** → the best shape there is. The
market is proven, the buyers are identified, and the reviewers have already written your
wedge for you. Record the axis and the count: *"14 of 31 sub-4-star G2 reviews name the CSV
export."*

**D · One giant plus a long tail of unhappy segments** → niche down. The giant serves the
median customer and cannot afford to serve a segment of two thousand. You can.

**E · An incumbent just died, got gutted, or tripled its price** → a migration window. Real,
but **time-boxed**: name the date it opened and estimate when it closes. If it opened
eighteen months ago, someone already took it.

Verify every competitor claim against the **actual pricing page and changelog**, with the
price quoted and the page dated. Never state a competitor's price from memory.

---

## 3 · "Nobody is doing this" — the three shapes that actually work

Untouched ground is usually untouched for a reason. What you are really hunting is one of:

1. **An unserved niche of a served market.** The tool exists but not for this segment's
   workflow, vocabulary, or compliance regime. Safest, most boring, most reliable.
2. **Newly possible.** Something infeasible 18 months ago on cost, capability, or legality.
   Highest ceiling, shortest window, and you must date the enabler.
3. **Unbundling.** One feature of a bloated incumbent that a segment would buy standalone —
   evidenced by reviews saying *"we only use it for X and pay for all the rest."*

If a candidate is none of these three, it is almost certainly either already served or not
wanted. Say which shape it is, in the write-up, in one sentence.

---

## 4 · Solo + AI kill flags

Any one of these is fatal for one person with little capital, regardless of how good the pain
is. Check every candidate against the whole list and record which ones you cleared.

- **Two-sided liquidity** — a marketplace that is worthless until both sides show up.
- **Enterprise procurement before the first dollar** — SOC 2, security review, legal, a
  six-month sales cycle. The pain may be real and still unreachable.
- **A cold-start corpus you cannot obtain** — the product needs data you have no path to.
- **Licensed or regulated practice** — medical, legal, or financial *advice*; money
  transmission. Tooling for licensed professionals is fine; being one is not.
- **Platform dependency where the platform can ship it** — check the platform's public
  roadmap and changelog. If your product is a line item on their roadmap, you are building
  their feature for free.
- **Broken unit economics** — model cost at realistic usage. Inference/API above ~25% of price
  leaves nothing, and any user-driven unbounded call path without a hard cap is an
  open invoice addressed to you.
- **Support that scales linearly** — per-customer integration, onboarding calls, hand-holding.
  One person is the ceiling.
- **Hardware, field operations, or logistics.**
- **Ad-supported anything** — it only works at a scale a solo founder will not reach.

---

## 5 · Default-reject patterns

Reject on sight unless the evidence in the *override* column is actually in hand. These are
not banned because they always fail; they are banned because they are what a language model
produces when it has no evidence, and they crowd out the real findings.

| Pattern | Override |
|---|---|
| A thin wrapper over a general model capability | a specific workflow + integration + proprietary or hard-won data, with T1/T2 evidence |
| *"<Famous product> for <vertical>"* | vertical-specific evidence that the general product actually fails there, quoted |
| A general-purpose chatbot or assistant for <domain> | never — this is a feature, not a product |
| A marketplace connecting A and B | none, for a solo founder (see kill flags) |
| A dashboard aggregating other people's APIs | T1 evidence of paying for exactly this, plus a retention story |
| Anything *"for SMBs"*, *"for teams"*, *"for everyone"* | name one occupation and one place they gather, with a member count |
| A free-time productivity tool for developers | a team or CI budget line, not an individual's wallet — developers build rather than buy |
| A product competing with a giant's free tier | a segment the free tier structurally cannot serve |

---

## 6 · The scorecard

Score each axis 0–3 with a one-line justification pointing at a specific evidence record.

| Axis | 0 | 3 |
|---|---|---|
| **Pain intensity** | mild annoyance | blocks revenue, compliance, or sleep |
| **Frequency** | once a year | daily or weekly |
| **Payment evidence** | T5 only | multiple T1/T2 from unrelated buyers |
| **Reachable buyer** | *"SMBs"* | a named community/list/board with a member count |
| **Gap quality** | crowded and well reviewed | shape C or D with the axis quantified |
| **Why now** | none, or *"AI exists"* | a dated enabler or a regulatory deadline |
| **Solo + AI build** | months of work before the first user | a thin wedge shippable in ≤6 weeks |
| **Still here in 12 months** | a weekend clone erases you | a niche, a data asset, or a relationship you accumulate |

**Hard gates beat the total.** A candidate is out if *any* of these is true, however high it
scores elsewhere:

- any axis at **0**
- payment evidence below **2** (no T1/T2 in hand)
- any **kill flag** unresolved
- fewer than **3 evidence records from ≥2 lanes**

Surviving that, rank by total (max 24). **A total below 14 is not a shortlist candidate.**

---

## 7 · Do not pad

The output count is a consequence, not a target. If two clusters clear the gates, present
two. If none do, present **none** — report the graveyard, say what the evidence actually said,
and propose the next hunting grounds. Manufacturing a third candidate to fill a slot is the
single most expensive thing this skill can do, because it costs weeks of building, not tokens.

Never soften a dead cluster into a live one by lowering the bar. Move the bar, and the whole
exercise becomes a plausible-sounding random idea generator with citations bolted on.

---

## 8 · Where this stops

`find-idea` screens **broad and shallow**: does the pain exist, does anyone pay, is the space
open, could one person build it. That is all.

TAM/SAM/SOM, full unit economics, the risk register, incident response, the distribution plan
and the GO/NO-GO verdict belong to **`product-critic` at phase 1**, on the single idea the
human picks. Do not do that work here — it is a different depth on a different scope, and
duplicating it wastes the one budget that matters while producing a second opinion nobody
asked for.
