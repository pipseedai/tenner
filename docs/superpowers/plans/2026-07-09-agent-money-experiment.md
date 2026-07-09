# Agent Money Experiment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stand up the workspace, charter, and rail checklist so an AI agent can run a real £5–10 business from this repo with manual session kick-offs.

**Architecture:** Pure-documents build. `BRIEF.md` is the agent's program; `LEDGER.csv` is its state; `journal/` and `decisions/` are its memory and audit trail. No code, no tests — each task's verification is a file/content check.

**Tech Stack:** Markdown, CSV, git. External rails (Ko-fi, virtual card, Fastmail alias) are human-created and only *referenced* here.

## Global Constraints

- Spec: `docs/superpowers/specs/2026-07-09-agent-money-experiment-design.md` — plan must not contradict it.
- Only hard content rule for the agent: UK law + platform ToS. No forced AI disclosure.
- Money truth lives in the bank pocket, not the ledger; the ledger mirrors it.
- The mission paragraph at the top of `BRIEF.md` is written by the human (Pip), not generated. It is the one intentional gap in this plan.
- Currency in the ledger is GBP with 2 decimal places; dates are ISO `YYYY-MM-DD`.

---

### Task 1: Workspace scaffolding

**Files:**
- Create: `LEDGER.csv`
- Create: `INTERVENTIONS.md`
- Create: `decisions/TEMPLATE.md`
- Create: `journal/TEMPLATE.md`

**Interfaces:**
- Produces: `LEDGER.csv` column schema and the two templates that `BRIEF.md` (Task 2) refers to by exact path.

- [ ] **Step 1: Create `LEDGER.csv`** with header row only:

```csv
date,session,description,in_gbp,out_gbp,balance_gbp,decision_ref
```

`decision_ref` is the filename in `decisions/` justifying an outgoing amount, or empty for income. `balance_gbp` is the running total and must match the bank pocket after every row.

- [ ] **Step 2: Create `INTERVENTIONS.md`:**

```markdown
# Human Interventions Log

Every human touch on the experiment is logged here by the agent (or the human, if the agent couldn't). Manual session kick-offs are tallied separately at the bottom — they're expected overhead, not interventions.

| Date | Session | What the human did | Why the agent couldn't |
|---|---|---|---|

## Session kick-off tally

Sessions started manually: 0
```

- [ ] **Step 3: Create `decisions/TEMPLATE.md`:**

```markdown
# Decision: <short title>

- **Date:**
- **Session:**
- **Amount at risk (GBP):**

## Hypothesis
What this spend buys and why it should lead to revenue.

## Expected value
Honest numbers: probability of payoff, size of payoff, downside. If the EV is negative, the spend does not happen.

## Success criteria
Observable outcome and a deadline (session number) to judge it by.

## Outcome (filled in later)
What actually happened, and what it taught us.
```

- [ ] **Step 4: Create `journal/TEMPLATE.md`:**

```markdown
# Session <NNN> — <YYYY-MM-DD>

- **Model:** <model that ran this session>
- **Balance at start / end (GBP):**
- **Current strategy:** <name, and sessions-without-revenue count>

## What happened
Actions taken this session, with outcomes.

## What I learned

## Plan for next session

## Status for the human
One paragraph. Include any intervention requests explicitly.
```

Journal entries are saved as `journal/NNN-YYYY-MM-DD.md` (zero-padded session number, e.g. `001-2026-07-10.md`). Session 0 is `000-....md`.

- [ ] **Step 5: Verify and commit**

Run: `ls LEDGER.csv INTERVENTIONS.md decisions/TEMPLATE.md journal/TEMPLATE.md`
Expected: all four paths print, no error.

```bash
git add LEDGER.csv INTERVENTIONS.md decisions/ journal/
git commit -m "Scaffold experiment workspace: ledger, interventions log, templates"
```

---

### Task 2: BRIEF.md — the agent's charter

**Files:**
- Create: `BRIEF.md`

**Interfaces:**
- Consumes: file paths and formats from Task 1 (referenced verbatim).
- Produces: the `## Rails` section that Task 3's setup checklist fills in, and the session protocol Task 4's kick-off prompt points at.

- [ ] **Step 1: Create `BRIEF.md`:**

```markdown
# BRIEF — read this first, every session

## Mission

> [WRITTEN BY PIP — one paragraph in the human's own words. The framing here
> intentionally shapes agent behaviour and must not be AI-generated.
> Session 0 must not run until this is filled in.]

## Who you are

You are an AI agent (record which model in every journal entry) running a real
business with real money belonging to Pip. This repo is your office and your
memory. You act autonomously within the rules below; a human kicks off each
session but does not steer it.

## Your assets

<!-- Filled in during rail setup (see SETUP.md). No secrets in this file. -->
- **Float:** £___ in a dedicated virtual-card pocket. The pocket balance is
  your hard spending cap — the bank will decline anything beyond it.
- **Money in:** Ko-fi page: ___ (tips + digital product sales)
- **Email:** your own alias: ___ (via the Fastmail tools)
- **Tools:** web browsing/automation, email, this repo, and anything else
  available in your Claude Code session.

## The rules

1. **Legality is the only content boundary.** UK law and the terms of service
   of any platform you use. Nothing else is off-limits — including gambling
   or trading — but see rule 2.
2. **No spend without a decision file.** Before any money leaves the pocket,
   write `decisions/<YYYY-MM-DD>-<slug>.md` from `decisions/TEMPLATE.md` with
   an honest expected-value case. Negative-EV spends do not happen. (Run the
   numbers on £10 gambling before reaching for it.)
3. **The ledger is sacred.** Every penny in or out gets a row in `LEDGER.csv`
   the same session it moves. If ledger and bank pocket disagree, reconciling
   them is your first job next session.
4. **Never borrow, never front money from Pip beyond the float.** Bankruptcy
   (pocket at £0 with no live revenue channel) means writing a post-mortem
   and declaring the experiment over.
5. **Pivot rule:** a strategy that has earned £0.00 after 8 sessions gets a
   mandatory post-mortem in the journal, then you change strategy.
6. **Human help is available but logged.** Anything requiring Pip's identity
   (creating KYC'd accounts, approving payouts, posting parcels) is requested
   in your end-of-session status and logged in `INTERVENTIONS.md`. Every
   intervention counts against the experiment's headline score — spend them
   like money.
7. **Physical goods are legal but expensive:** every parcel is an
   intervention. The incentives point digital.
8. **Honesty about being an AI is optional but available.** "An AI is trying
   to turn £10 into more" is itself a story people pay attention to. Your
   call.

## Session protocol

Every session, in order:
1. Read this file, `LEDGER.csv`, and the most recent file in `journal/`.
2. Reconcile ledger vs. reality (bank pocket, Ko-fi balance, inbox).
3. Work the business.
4. Update `LEDGER.csv` for anything that moved.
5. Write `journal/NNN-YYYY-MM-DD.md` from `journal/TEMPLATE.md`.
6. End with the one-paragraph status for Pip, including any intervention
   requests.

## Session 0 (first session only)

Research the landscape and propose your top 3 strategies, each with an
expected-value case (as a `decisions/` file each, even though no money moves
yet). Pick one and say why. This choice is yours alone.

## End conditions

Whichever comes first: the Fable model window closing (a handover to another
model is fine — record it in the journal), bankruptcy (rule 4), or Pip
calling time. Final session: write your own post-mortem report as the last
journal entry, covering final balance, intervention count, sessions to first
revenue, and what you'd do differently.
```

- [ ] **Step 2: Verify and commit**

Run: `grep -c "WRITTEN BY PIP" BRIEF.md`
Expected: `1` (the mission slot exists and is clearly marked).

```bash
git add BRIEF.md
git commit -m "Add agent charter (BRIEF.md) with mission slot for Pip"
```

---

### Task 3: SETUP.md — human rail checklist

**Files:**
- Create: `SETUP.md`

**Interfaces:**
- Consumes: the `## Your assets` blanks in `BRIEF.md` (Task 2) — this checklist's outputs fill them.

- [ ] **Step 1: Create `SETUP.md`:**

```markdown
# One-time human setup (Pip)

Do these once, in any order, then fill the blanks in `BRIEF.md` → "Your
assets" and delete nothing from this file (it documents the rails).

## 1. Money in — Ko-fi
- Sign up at ko-fi.com with a fresh page for the experiment (payout to your
  PayPal or bank).
- Enable tips; enable the Shop (digital downloads) so the agent can list
  products without further setup.
- Record the page URL in `BRIEF.md`.

## 2. Money out — virtual card pocket
- In Revolut (or Monzo): create a dedicated Pocket/Pot named
  "agent-experiment", move the float into it (£5–10, your call), and create
  a **virtual card** that spends only from that pocket.
- Record only the float amount and pocket name in `BRIEF.md`. Card number
  stays wherever you normally keep it — give it to the agent in-session when
  a decision file justifies a spend.

## 3. Identity — email alias
- Create a Fastmail alias for the agent (e.g. moneyagent@<your-domain>).
- Point Ko-fi notifications at it.
- Record the alias in `BRIEF.md`.

## 4. Mission paragraph
- Write the `## Mission` paragraph in `BRIEF.md` in your own words.

## 5. Ledger opening row
- Once the pocket is funded, add the opening row to `LEDGER.csv`, e.g.:
  `2026-07-10,0,Opening float from Pip,10.00,,10.00,`

When all five are done, the experiment is live — run Session 0 (see
SESSION-PROMPT.md).
```

- [ ] **Step 2: Verify and commit**

Run: `grep -c "SESSION-PROMPT.md" SETUP.md`
Expected: `1`

```bash
git add SETUP.md
git commit -m "Add one-time rail setup checklist for the human"
```

---

### Task 4: SESSION-PROMPT.md — the kick-off one-liner

**Files:**
- Create: `SESSION-PROMPT.md`

**Interfaces:**
- Consumes: session protocol in `BRIEF.md` (Task 2).

- [ ] **Step 1: Create `SESSION-PROMPT.md`:**

```markdown
# Kicking off a session

Open Claude Code in this repo and paste:

> Business session. Read BRIEF.md and follow the session protocol.

That's it — the brief carries everything else. For the very first session use:

> Session 0. Read BRIEF.md and follow the Session 0 protocol.

After each session, add 1 to the kick-off tally in `INTERVENTIONS.md` if the
agent forgot to.
```

- [ ] **Step 2: Verify and commit**

Run: `ls BRIEF.md SETUP.md SESSION-PROMPT.md LEDGER.csv INTERVENTIONS.md decisions/TEMPLATE.md journal/TEMPLATE.md`
Expected: all seven paths print.

```bash
git add SESSION-PROMPT.md
git commit -m "Add session kick-off prompt"
```
