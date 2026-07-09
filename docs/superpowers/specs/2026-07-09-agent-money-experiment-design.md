# Agent Money Experiment — Design

**Date:** 2026-07-09
**Status:** Draft for review

## Purpose

Give an AI agent (Claude Fable, running in Claude Code) a small amount of real money (£5–10; exact float chosen at setup — the spec says "£10" below for concreteness) and the rails to act on it, and observe whether it can grow it — with as little human intervention as possible. It's fun-first, but set up for the agent's best realistic chance of profit.

Success is loosely defined; the three headline measurements are:

1. **Final balance** vs starting balance
2. **Human intervention count** (every touch logged)
3. **Sessions to first revenue**

The qualitative record (the agent's journal) is the writeup material regardless of P&L.

## Approach

**Open strategy, structured process.** The agent chooses *what* business to run freely (anything within UK law and platform ToS — gambling and trading are permitted but must survive a written expected-value case). *How* it operates is scaffolded: a ledger, decision records before any spend, pivot rules, and hard bank-enforced spending caps.

## Rails (one-time human setup)

| Rail | Choice | Why |
|---|---|---|
| Money in | Ko-fi page | Free, takes tips and sells digital downloads, pays out to owner's PayPal/bank. Completes the earn-loop. Stripe is the upgrade path if needed later. |
| Money out | Revolut/Monzo **virtual card** in a dedicated pocket holding the £10 | The pocket balance is the hard spending cap, enforced by the bank — not by trusting the agent's arithmetic. |
| Identity | Fastmail email alias for the agent | Agent genuinely owns its inbox via the existing Fastmail MCP: signups, Ko-fi notifications, customer contact. |
| Everything else | Created on request | If the agent's strategy needs an account (Gumroad, eBay, domain registrar…), it requests it; the human creates it. Each request = one logged intervention. |

## Workspace (this repo)

```
i-like-money/
├── BRIEF.md          # the agent's charter — rules, rails, discipline, boundaries
├── LEDGER.csv        # every penny in/out, one row per transaction
├── decisions/        # one file per spend: the EV case written BEFORE spending
├── journal/          # one file per session: what it did, learned, plans next; model recorded
├── INTERVENTIONS.md  # log of every human touch, and why
└── docs/superpowers/specs/  # this design
```

Ledger + journal are the agent's business memory: session N+1 starts by reading them.

## Operating loop

- **Kick-off:** manual. The human starts each session (a one-line command); the session then runs autonomously. Frequent sessions — daily or twice daily — since kick-off is cheap and the timeline is short.
- **Session 0:** research the landscape, propose top 3 strategies each with an expected-value case, pick one, log the reasoning. Fully open choice.
- **Recurring sessions:** read ledger + latest journal → work the business (browser, email, files) → update ledger + journal → end with a one-paragraph status for the human.
- **Discipline rules (in BRIEF.md):**
  - No spend without a written EV case in `decisions/`.
  - Pivot rule: zero revenue after ~8 sessions → mandatory post-mortem, then change strategy.
  - Never borrow; never spend beyond the pocket; physical goods allowed but every parcel = an intervention.

## Boundaries and stop conditions

- UK law and platform ToS are the only hard content rules. No forced AI disclosure — though the brief notes "an AI running a £10 business" is itself a marketable story the agent may use.
- **Timeline:** compressed by the Fable plan deadline. The experiment runs while Fable is available; if a different model must take over mid-run, the handover is recorded in the journal and treated as an observation, not a spoiled experiment.
- **Hard end:** Fable deadline, agent-declared bankruptcy, or human call — whichever first. Final session = agent writes its own post-mortem report.
- **Maximum loss:** the £10 float plus payout fees. The virtual-card pocket makes overspend physically impossible.

## Human intervention policy

Help is *available but logged*, never banned. The experiment doesn't test whether the agent can fake independence; it measures exactly how much dependence it needs. Interventions include: creating KYC'd accounts, approving payouts, posting parcels, and each manual session kick-off is noted but counted separately from substantive interventions.

## Out of scope

- Automated/scheduled sessions (manual kick-off for now; can revisit).
- Multi-agent setups, trading bots, or anything requiring the human to execute strategy on the agent's behalf.

## Implementation plan (small)

1. Write `BRIEF.md` (the agent's charter — the single most important artifact).
2. Create `LEDGER.csv`, `INTERVENTIONS.md`, empty `decisions/` and `journal/`.
3. Human sets up: Ko-fi page, virtual card pocket with the float, Fastmail alias.
4. Record rail details (Ko-fi URL, alias address, card pocket name — no secrets) in `BRIEF.md`.
5. Run Session 0.
