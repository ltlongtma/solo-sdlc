# Where pain is written down — the four lanes

Field manual for the scouts spawned at step 2 of `find-idea`. Each scout owns ONE lane
and returns **evidence records**, never ideas. Read your lane plus *Evidence record
schema* and *Source hygiene* at the bottom; skip the other lanes.

| Lane | What it proves | Willingness-to-pay strength |
|---|---|---|
| 1 · Complaint | the pain exists and is described in the sufferer's own words | weak on its own |
| 2 · Review | someone is *already paying* an incumbent and is unhappy on a specific axis | strong |
| 3 · Paid labour | someone has an *approved budget* and is spending it on a human | strongest |
| 4 · Market shift | there is a dateable **why now** and a window that closes | timing, not demand |

A cluster that only ever shows up in lane 1 is a vitamin. Lanes 2 and 3 are where money is.

---

## Lane 1 · Complaint mining

**Where**

- **Reddit** — the on-site search is poor; drive it from a web search engine with
  `site:reddit.com/r/<sub>`. Profession subs beat topic subs: r/accounting, r/msp,
  r/sysadmin, r/ExperiencedDevs, r/smallbusiness, r/Construction, r/dentistry, r/lawyers,
  r/nonprofit, r/logistics, r/recruiting. Sort by top-of-year to skip the noise.
- **Hacker News** — `hn.algolia.com/api/v1/search?query=<q>&tags=comment` returns JSON with
  timestamps, no scraping needed. Mine `Ask HN: what do you pay for`, `Ask HN: what boring
  problem`, and the monthly *Who is hiring* / *Freelancer? Seeking freelancer?* threads.
- **Stack Overflow / Stack Exchange** — questions with high view counts and **no accepted
  answer** mark a workflow with no good solution, not just a coding question.
- **GitHub issues** — `is:issue is:open sort:reactions-+1-desc` on popular repos. A
  long-open issue with a hundred 👍 is demand the maintainer has decided not to serve.
- **Vendor community boards** — Shopify, WordPress, HubSpot, Atlassian, Salesforce, Xero,
  QuickBooks. People there are paying customers describing exactly what the product won't do.
- **X / Bluesky / LinkedIn** — lower signal, but `"I would pay for"` still surfaces things.

**Query patterns** (substitute the profession/workflow, keep the quotes)

```
site:reddit.com/r/<sub> "every week" spreadsheet
"is there a tool that" <workflow>
"I'd pay for" OR "shut up and take my money" <domain>
"we still do this manually" <industry>
"alternative to <incumbent>"
"<incumbent> is too expensive" OR "<incumbent> pricing" reddit
"how do you all handle" <workflow>
"wasted" hours OR days <workflow>
```

**What counts as a signal** — a named workflow, a stated frequency (daily/weekly/monthly),
a stated cost in hours or money, from someone whose role implies a budget.

**Traps** — students, hobbyists and job-seekers complain loudly and buy nothing. A complaint
aimed at a platform (`Shopify should add X`) is a feature request the platform may ship next
quarter; check its public changelog before treating it as an opening. One loud thread is not
a market — you need the same complaint from unrelated people.

---

## Lane 2 · Review mining

**Where**

- **B2B review sites** — G2, Capterra, GetApp, TrustRadius, Software Advice. Filter to
  **2–3 stars** and read only the *Cons* field. Also read the vendor's own `/alternatives`
  and comparison pages — they name the segments they are losing.
- **App stores** — App Store and Google Play, 1–2 stars sorted by *most recent*. Review
  volume and install count double as a crude market-size proxy.
- **Niche marketplaces are the richest of all** because installs, ratings and sometimes
  revenue are public and the buyers are commercial: Shopify App Store, Chrome Web Store,
  WordPress.org plugin support forums, Atlassian Marketplace, Salesforce AppExchange, Figma
  Community, Notion/Slack/Zapier app directories, VS Code Marketplace.
- **Trustpilot** for consumer and SMB services.
- **Product Hunt comments** — the `wish it also did X` replies under a launch.

**What counts as a signal** — **the same complaint from N unrelated reviewers on one axis.**
One angry review is noise; eleven reviews saying *"great tool, but the export is useless"* is
a wedge with the wedge already named for you. Record N and the axis.

**Before believing it** — open the incumbent's pricing page and changelog. If they shipped
the fix or the reviews predate a major release, the gap is closed. Quote the actual price
from the actual pricing page; never recall a price from memory.

**Traps** — incentivised/gamed reviews (a wall of 5-stars in one week). Complaints about
support or onboarding are not product gaps — though they can be a *service* business.
"Too expensive" alone is not a gap unless a cheaper credible option is genuinely absent.

---

## Lane 3 · Paid-labour mining

The strongest evidence there is: **somebody already got the budget approved and is spending
it on a human.** You are not asking whether they would pay — you are reading the invoice.

**Where**

- **Job boards** — LinkedIn, Indeed, We Work Remotely, remote-first boards. Hunt for titles
  that are literally a manual workflow: *data entry, operations coordinator, billing
  reconciliation, report compilation, claims processing, lead list building, invoice
  matching, compliance documentation.* The same posting appearing at twenty different
  companies is a recurring budgeted pain, and **the salary range is the budget ceiling**.
- **Freelance marketplaces** — Upwork and Fiverr. Search the workflow, count live gigs, read
  repeated near-identical requests and record their posted budgets. On Fiverr, a category
  with hundreds of sellers is proven demand with a public price.
- **BPO / VA service menus** — Belay, Athena, Magic and similar publish a catalogue of tasks
  people pay humans to do monthly. It is a demand list with prices attached.
- **Productised agency offers** — a small agency selling *"done-for-you <X>, $2k/mo"* has
  already validated both the pain and the price; the question is only whether X is automatable.
- **r/forhire** and equivalents — the *hiring* side, not the *for hire* side.

**What counts as a signal** — a budget number, repetition across unrelated buyers, and a task
that is **rule-bound** enough to automate.

**Traps** — work that is really judgement, relationships or physical presence will not
automate. A single one-off gig is not a market. A job title is usually broader than the
manual task inside it — quote the responsibility bullet, not the title.

---

## Lane 4 · Market-shift mining

This lane does not prove demand. It proves **why now** and how long the window stays open.

**Where**

- **Shutdowns and sunsets** — `"is shutting down" OR "sunsetting" OR "end of life" <category>`,
  plus product-graveyard trackers. The migration thread that follows (*"what is everyone
  moving to?"*) is a list of customers with a deadline.
- **Price hikes and repackaging** — `"<product> price increase" 2025..2026`, the backlash
  threads, and any free tier being killed. A 2–3× hike opens a migration window that closes
  within months.
- **Acquisitions that gut a product** — `"acquired by"` followed by a wave of complaints.
- **Abandoned open source with real users** — last commit older than ~18 months, issues
  piling up, but the package still has serious weekly downloads on npm/PyPI or many
  dependents. Users with no maintainer are users looking for somewhere to pay.
- **Regulation with a deadline** — the single strongest willingness-to-pay event that exists,
  because people buy on a date. Look for effective dates 6–24 months out on regulator sites
  (accessibility, e-invoicing mandates, data residency, ESG/sustainability reporting,
  AI disclosure). Record the **exact date and the regulation's name**.
- **Platform policy and API changes** — app-store rule changes, API deprecations, a platform
  closing a free tier. These orphan a known set of users overnight.
- **Newly viable** — a capability or a cost curve that crossed a threshold in the last
  12–18 months. You must be able to **date the enabler and say what specifically changed.**

**Trap — the fake why-now.** *"AI can do this now"* is not a why-now: everyone on earth has
that same enabler, which is precisely why the space fills up within a quarter. A real why-now
is specific and dateable: a price that fell 10×, a rule that takes effect on a date, an
incumbent that left the market. If the why-now cannot be dated, the cluster does not get one.

---

## Secondary sweep · Vietnam / SEA

Run this only after the global sweep, and only if the global evidence points at a workflow
that is obviously local (language, regulation, banking rails, local platform).

- Facebook Groups by profession, Vietnamese dev and founder communities, Zalo OA / local
  SaaS forums, local job boards (TopCV, ITviec) for the manual-workflow titles from lane 3.
- Local regulation is a strong lane-4 source (e-invoicing, tax filing, labour reporting).

Weigh it honestly: less competition, but a **much lower price ceiling** and payment evidence
that is far harder to find. A VN-only cluster needs lane-3 evidence to survive — a complaint
in a Facebook group is not enough. If the same workflow has global demand, prefer global.

---

## Evidence record schema

Every scout returns a flat list of records. No prose, no ideas, no recommendations.

```
- artifact:  <one sentence: what this is>
  url:       <real, fetched URL>
  date:      <YYYY-MM or YYYY-MM-DD from the page; "undated" if truly absent>
  who:       <role/segment of the person, and how you know>
  quote:     "<verbatim, ≤40 words, their words not yours>"
  pays:      <T1 already paying $X/mo for <tool> | T2 paying a human $X | T3 spends N hrs/<period>
              | T4 says they would pay | T5 complaint only>
  lane:      <1-4>
```

`pays` uses the willingness-to-pay ladder in `screening.md`. Get it right — it is the field
that decides whether a cluster survives.

## Source hygiene

- **Never invent a URL.** If a page could not be fetched, say `FETCH FAILED` and move on —
  a fabricated citation is worse than a missing one and poisons every step downstream.
- **Every record carries a date.** Evidence older than ~24 months is stale unless the
  workflow is genuinely static; flag it rather than dropping it silently.
- **Quote verbatim.** The customer's own words become the landing-page copy later, and a
  paraphrase quietly launders your assumptions into their mouth.
- **Prefer the primary artifact** over a listicle about it. `Top 10 tools for X` blog posts
  are SEO affiliate content, not demand evidence.
- Report the search you ran and what it returned, including the searches that found nothing.
  An empty lane is a real finding.
