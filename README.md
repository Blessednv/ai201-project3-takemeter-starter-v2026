# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

My community is cybersecurity Reddit, which is public and not tied to one show
or release. I have 426 clean posts and 98 comments, all text only, saved in
three CSV files that I'm keeping. I leave out any post that contains a link.
Most of them are link-only news posts with almost no text to judge, and links
also make the labeling less consistent. The classifier reads a post and
sorts it into one of four labels based on what the writer included:
`specific_problem` (asking for help with a detailed problem), `vague_worry`
(worried but gives no details), `reasoned_opinion` (sharing an opinion with a
reason) or `broad_question` (asking a general question).

**Four distinctions I saw in the text:**

1. Specific names vs. general description. Some posts name an exact tool, error
   or setup, like "M-PESA Daraja callbacks" or "Trojan:JS/EtherHiding". Others
   only say "I clicked something and ads keep popping up".

2. Says what they already tried. Some posts list steps taken, like
   disconnecting the PC and changing passwords. Others go straight to "should I
   be worried?".

3. Gives a reason or a position. Some posts explain why they think something.
   Others only ask "has your company changed anything?".
   
4. One narrow question vs. a broad one. "Which request attributes must the PDP
   source independently?" has one answer to look for. "Which certs should I
   get?" is open-ended.



---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

Each post gets exactly one of four labels. The labels describe what is in the
text (what the writer included), not whether the post is "good" or "bad". A
"technical specific" below means a concrete detail an expert could look up or
check: an error message, a detection name, a program or process name, a file, a
setting, or a named API. Naming a phone or an app alone (like "iPhone" or
"TikTok") does not count.

### `specific_problem`

**Definition:** The writer asks for help with a situation and names at least
one technical specific.

**Example 1:**
> "I started getting a captcha when I opened google chrome incognito tab ...
> windows defender picked up on this: Trojan:JS/EtherHiding,CX!ams ... the
> threat was removed and I've wiped my chrome's cookies and data from all time,
> and also changed all passwords from another device."
>
> *(r/cybersecurity_help. It names the exact detection and says what was
> already done.)*

**Example 2:**
> "I build systems that receive payment confirmations from Safaricom's M-PESA
> Daraja API (STK Push and C2B callbacks). As far as I can tell, Daraja doesn't
> send an HMAC signature or similar with its callbacks ..."
>
> *(r/AskNetsec. It names the API and lists the protections already in use.)*

### `vague_worry`

**Definition:** The writer describes a scare or symptom with no technical
specifics, only what they saw or felt, and asks whether something is wrong.
What the person did, like "I hung up", does not count as a technical detail.

**Example 1:**
> "recently ive clicked a suspicious link, i have clicked something and all of
> the ads keep popping up and it even redirected me to my apps like, shein
> tiktok, etc. do yall think i have a virus?"
>
> *(r/cybersecurity_help. No error, file or program is named.)*

**Example 2:**
> "Okay so I just got a message that my tiktok was trying to be accessed and
> panicked but then realized that it said the username was [a username] and im
> super confused, should I be worried?"
>
> *(r/cybersecurity_help. A scare with no detail to check. I removed the
> username.)*

### `reasoned_opinion`

**Definition:** The writer states, or clearly hints at, a position and gives at
least one reason or checkable fact for it, even if the post ends with a
question.

**Example 1:**
> "Sat through enough demos this year that I've started using a short checklist
> to filter vendors ... If the honest answer involves an SDK, a proxy, or code
> changes, that's not 'runtime,' that's integration work with extra marketing.
> ... Input filtering alone misses anything novel ..."
>
> *(r/AskNetsec. Every point on the checklist comes with a reason.)*

**Example 2:**
> "Is it just me, or are we being gaslit into thinking its practical and
> productive to provide Hermes agents API keys to an OPNSense router so it can
> fully manage it? Even if its doesn't do anything nefarious, if using a cloud
> LLM to back Hermes, your networking info is being sent to the cloud."
>
> *(r/cybersecurity. It takes a side and gives a reason for it.)*

### `broad_question`

**Definition:** The writer asks for general advice or opinions that anyone could
answer without examining the writer's own system, even if they add some
background.

**Example 1:**
> "I see lots of articles and discussions on AI-enabled traditional
> cybersecurity pentesting, but what a people doing or using for AI-security
> pentesting?"
>
> *(r/AskNetsec. One open question with no setup described.)*

**Example 2:**
> "about five months ago, I started my journey in IT ... So far, I've learned
> Python, SQL, and a little bit of C ... I want to know which certifications I
> should pursue, what skills I need to develop ..."
>
> *(r/cybersecurity. Some background, but the question is open to anyone.)*

### The hardest boundary

**Which two labels:** `reasoned_opinion` and `broad_question`.

**The post that sits between them (r/AskNetsec):**
> "Why do so many recent breaches start with a leaked API token or service
> account? Going through breach reports from the last year and it's the same
> story over and over. Leaked API tokens and OAuth apps nobody remembered
> approving. Nobody phished a person, just found a key under the mat... Are non
> human identities the easiest way in now and what are you doing about the ones
> nobody owns?"

It could be a `reasoned_opinion`, because the writer points to a pattern from
breach reports. It could also be a `broad_question`, because it ends by asking
everyone for general advice.

**The decision rule I used every time:**
<!-- e.g. "If the post names a specific checkable fact, it's `analysis`, even
     if the tone is heated." -->
Remove the final question. If a claim with a reason or a checkable fact is
still left, the post is `reasoned_opinion`. If nothing is left but the question,
it is `broad_question`. The post above keeps its claim (breach reports show the
same pattern: leaked tokens and forgotten apps, not phishing), so I label it
`reasoned_opinion`.



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:**

**How I labelled them:** <!-- Cold first? Pre-labelled with AI and corrected?
Say so plainly — the disclosure is required, not penalised. -->

**Counts per label:**

| Label | Count | Share |
|---|---|---|
|  |  |  |
|  |  |  |
|  |  |  |
| **Total** |  | 100% |

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:*
>
> *Could have been:*
>
> *I chose, because:*

**2.**
> *The post:*
>
> *Could have been:*
>
> *I chose, because:*

**3.**
> *The post:*
>
> *Could have been:*
>
> *I chose, because:*

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:**

**Settings:** <!-- epochs, learning rate, batch size, seed -->

**Anything I changed from the defaults, and why:**

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Pre-labelling disclosure:**

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
