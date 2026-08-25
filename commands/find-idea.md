---
description: Mine the internet for evidence of a pain people already pay to escape, then shortlist 2-3 buildable product ideas.
---

Invoke the `find-idea` skill from this plugin and run it end to end for what the user described below.

Pick the mode from their input — **cold start** if they have no idea, **fog** if they have one that is still vague. If it genuinely is not clear, ask exactly one question.

Follow the skill exactly, in particular:

1. Evidence first. Collect fetched, dated, quoted records before any candidate exists. Never invent a URL, a price, or a review count.
2. A candidate needs T1/T2 payment evidence — someone already paying money to a competitor or to a human. Complaints alone go to the graveyard.
3. Write the scan to a scratch directory. Do **not** `git init`, scaffold, or write code — a repo is the artifact of deciding to build.
4. Do not run `product-critic`'s analysis here. No TAM, no unit economics, no verdict.
5. Present 2–3 candidates plus the graveyard, then stop. Zero candidates is a valid, honest outcome — never pad the list.

End by telling the user the scan's path and that the next step is `/solo-sdlc:validate` on whichever candidate they pick.

Idea or starting point (may be empty): $ARGUMENTS
