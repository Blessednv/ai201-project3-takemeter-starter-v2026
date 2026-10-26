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
`specific_problem` (asking for help or advice about a named thing), `vague_worry`
(worried but names nothing specific), `reasoned_opinion` (sharing an opinion
with a reason) or `broad_question` (asking a general question).

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
A "named thing" below means something concrete an expert could look up or
check: a product, vendor, vulnerability (like a CVE), API, error message,
detection name, process, file, setting or role. Naming a phone or an app alone
(like "iPhone" or "TikTok") does not count.

**Why four labels, and why I chose them early.** I started with four labels from
the beginning, not three, and I wrote all four into this README (my first README
commit, before I collected or labelled any data). While reading 36 posts I could
point at four different things in the text: whether the writer names something
specific, whether they say what they already tried, whether they give a reason,
and whether the question is narrow or open-ended. Four labels was the smallest
set that kept those differences apart. I settled on four because of what I saw in
the posts, not because of the grading criteria, and I had not looked at the
stretch section when I decided.

The fourth label, the one three labels would have missed, is `broad_question`.
My first three kinds of post were people asking for help about a named thing
(`specific_problem`), people describing a scare with no details (`vague_worry`),
and people arguing a position with a reason (`reasoned_opinion`). Those left out a
large group: open-ended questions for general advice or experiences that name
nothing, and are neither a scare nor an argument. That group became
`broad_question`, and it turned out to be my largest label (141 of 428 posts,
32.9%). Without it, about a third of my posts would have had no label that fit.

### `specific_problem`

**Definition:** The writer asks for help or advice about a named thing: a
product, vendor, vulnerability, API, error message, detection name, process,
file, setting or role.

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

**Definition:** The writer describes a scare or symptom with no named thing,
only what they saw or felt, and asks whether something is wrong. What the
person did, like "I hung up", does not count as a technical detail.

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

**Definition:** The writer asks an open-ended question for general advice,
opinions or experiences, where no particular named thing is the subject, so it
could be asked of any security person about the field in general.

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

**A second rule, for `specific_problem` vs. `broad_question`:** If a named thing
(a product, vendor, vulnerability, API, error, file, setting or role) is the
subject of the question, the post is `specific_problem`. If nothing is named, it
is `vague_worry` (a personal scare) or `broad_question` (a general question). I
added this after testing my definitions on my first 50 cold-labeled posts, where
my first wording left many narrow questions about a named product or
vulnerability ending up in the wrong label.



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:**
Public Reddit posts from three cybersecurity communities (r/cybersecurity,
r/AskNetsec and r/cybersecurity_help), collected in October 2026 from Reddit's
public RSS feeds. No login was needed. I kept only text-only posts: I dropped
posts with empty bodies, links, images, video or emoji, duplicates, and posts in
other languages. That left 428 posts. I also collected comments from
r/SecurityCareerAdvice but did not use them.

**How I labelled them:** <!-- Cold first? Pre-labelled with AI and corrected?
Say so plainly — the disclosure is required, not penalised. -->
I labelled the first 50 posts cold: by hand, using only my own definitions, with
no AI help. I made every label decision on those 50 myself. For a few hard cases
I asked Claude to review my reasoning or suggest wording for the note. I marked
these rows `cold`.

The other 378 posts were pre-labelled by AI. Fresh Claude instances, given only
my label definitions and decision rules, suggested a label for each post. I then
read the rows and checked the labels, correcting 2. Rows are marked
`pre-labeled, checked` or `pre-labeled, corrected`.

Before pre-labelling, I tested my definitions by having an AI label my 50 cold
posts without seeing my labels. Its agreement with me was 64% at first, which led
me to tighten the `specific_problem` definition. The tightened wording raised
agreement to 72%.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `specific_problem` | 134 | 31.3% |
| `vague_worry` | 87 | 20.3% |
| `reasoned_opinion` | 66 | 15.4% |
| `broad_question` | 141 | 32.9% |
| **Total** | 428 | 100% |

**Six hard cases**

These are six of the 14 hard cases I recorded. All 14 are in `hard_cases.csv`.

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* "If an AI agent was authorized correctly, but the evidence it used
> changes before execution, where should the security control live?" It gives a
> worked example (a balance of $10,000 becomes $2,000 before an $8,000 transfer
> runs) and then asks where teams enforce the boundary.
>
> *Could have been:* `reasoned_opinion` or `broad_question`.
>
> *I chose* `reasoned_opinion`, because with the questions removed, the post
> still argues that the failure is state changing between observation and
> execution, backed by a worked example. This is the case my decision rule was
> written for.

**2.**
> *The post:* "What are the most common messaging platforms used as command and
> control networks (excluding discord, signal, and telegram)."
>
> *Could have been:* `broad_question` or `specific_problem`.
>
> *I chose* `broad_question`, because it is a general factual question with no
> situation of the writer's own, even though it is narrow and technical.

**3.**
> *The post:* "My wife just noticed in her past orders, a canceled order for PS5
> with a comment ... It shows as canceled and total is "0$" ... What could have
> possible happened?"
>
> *Could have been:* `vague_worry` or `specific_problem`.
>
> *I chose* `vague_worry`, because it is a personal scare with no named technical
> thing. Target is a store account, which does not count, and the order details
> are what the writer saw, not technical specifics.

**4.**
> *The post:* "For people who have integrated monitoring or threat-intel feeds,
> which production detail caused the most trouble: auth, event delivery,
> coverage gaps, or remediation state handling?" Before that question, it argues
> that "Webhooks are especially easy to underestimate. A monitoring product can
> look fine in staging and still lose alerts during a deploy, timeout, or
> signature-validation mistake months later." It also reads partly like a
> promotional article.
>
> *Could have been:* `specific_problem` or `reasoned_opinion`.
>
> *I chose* `specific_problem`, because the post is about integrating monitoring
> and threat-intel APIs and names concrete details like webhooks, signature
> validation and a DPA. It could be `reasoned_opinion` because it argues, with
> reasons, that webhooks are easy to underestimate.

**5.**
> *The post:* "What identity verification API are you using in production across
> a lot of countries?" The writer describes poor pass rates on documents outside
> the US and Western Europe and slow support, and ends: "If you are running one of
> these in prod across a lot of countries, what are you on and would you pick it
> again?"
>
> *Could have been:* `specific_problem` or `broad_question`.
>
> *I chose* `specific_problem`, because the writer describes a concrete situation
> (low pass rates on non-US documents, slow support, tests with a worn national ID)
> and asks about webhooks and AML screening. It could be `broad_question` because
> the final ask is open to any reader.

**6.**
> *The post:* "Possible opportunity? I’m given a weird opportunity and I’m
> unsure how to go about it to make the most of it." A friend sent the writer
> equipment, and they ask how to use it to reach their cybersecurity career goals.
>
> *Could have been:* `vague_worry` or `broad_question`.
>
> *I chose* `vague_worry`, because the writer sounds unsure how to make the most
> of the opportunity and apologizes for asking. It is a weak fit, since there is
> no scare or symptom. It could be `broad_question` because the main ask is
> general career advice that anyone could answer.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`, fine-tuned for 4-way classification.

**Settings:** <!-- epochs, learning rate, batch size, seed -->
First run: 3 epochs, learning rate 2e-5, batch size 16, 128 tokens per post,
seed 42. Trained on an Apple Silicon GPU (`mps`), PyTorch 2.2.2, taking 3
minutes 41 seconds.

**Anything I changed from the defaults, and why:**
**First run:** nothing. I used every notebook default.

**Second run (the stretch, declared before running it):** I will change exactly
one setting: **epochs, from 3 to 5.** In the first run, the loss was still
falling at epoch 3 (training loss 1.36, 1.15, then 1.04), and validation
accuracy and F1 were still rising, so I want to see whether more training
helps. Everything else stays the same: seed 42, so the split and the 65 test
posts are identical, plus learning rate 2e-5, batch size 16 and 128 tokens. The
first run's results are saved as `results_run1.json`. After the run, I will
report which numbers changed against the first run and by how much. I will not
change my criteria in `criteria.md` because of either run.

**What moved (second run, 5 epochs, vs. 3 epochs).** The second run's results are
saved as `results_run2.json`. On the same 65 test posts, accuracy went from 0.585
to 0.569 (-0.015, one post fewer correct, 38 to 37) and macro F1 from 0.481 to
0.463 (-0.018). By label: `specific_problem` F1 fell from 0.500 to 0.444,
`vague_worry` from 0.769 to 0.741, `broad_question` rose from 0.655 to 0.667, and
`reasoned_opinion` stayed at 0.000: the model never predicted that label in
either run. The confidence result was identical. Validation accuracy rose from
0.569 to 0.600, so more epochs helped on the validation posts but not on the
test posts. With 65 test posts, one post is worth about 1.5 points, so I read
these changes as small, and the one clear finding is that more training did not
fix `reasoned_opinion`.

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->
298 train, 65 validation and 65 test. Test posts per label: `specific_problem` 20,
`vague_worry` 13, `reasoned_opinion` 10, `broad_question` 22. No label has fewer
than 8 test posts, but `reasoned_opinion` has only 10, so its score will move a
lot between runs.



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1: testing my label definitions**

- *What I asked for:* a fresh Claude, which had not seen my labels, to label my 50
  cold posts using only my four definitions, so I could see where my definitions
  were unclear.
- *What came back:* it agreed with me on 64% (32 of 50). Most of the disagreement
  was on `specific_problem`, which it often called `broad_question` or
  `reasoned_opinion`.
- *What I changed:* I tried a broader `specific_problem` definition, which made
  agreement worse (52%), so I rejected it. A narrower version, requiring a named
  thing as the subject of the question, raised it to 72%. I kept that one and
  updated the README and `label_definitions.txt`.

**Moment 2: AI pre-labelling 378 posts**

- *What I asked for:* fresh Claudes, in batches, to suggest a label, an unsure
  flag and a one-sentence reason for each of my remaining 378 posts, using only
  my definitions.
- *What came back:* a label for every post. One batch looked wrong, with 62%
  `specific_problem` when the others had about 30%, so I had it relabelled and
  used the second version.
- *What I changed:* I read the rows and checked every label, and corrected 2. I
  marked each row in the note column as `pre-labeled, checked` or
  `pre-labeled, corrected`.

**Moment 3: help with hard cases**

- *What I asked for:* Claude's view on some hard posts, and suggested wording for
  the reasons in my hard-case notes.
- *What came back:* arguments for the other label, and draft reason sentences.
- *What I changed:* I chose the labels myself. For several notes, I used or
  adapted Claude's wording.

**Pre-labelling disclosure:**
I labelled the first 50 posts cold, by hand, with no AI help on the labels. The
other 378 posts were pre-labelled by AI from my written definitions. I read and
checked every one and corrected 2, and the note column records which rows were
pre-labelled. Claude also wrote the scripts I used to collect the posts and to
label them, and helped draft my README text.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Stretch Goals (Unit 6)

I am adding one stretch feature in this unit:

- **Per-label error write-up:** for whichever label my confusion matrix
  shows is worst, I will write which label it gets confused with and what
  the wrong examples have in common.

### Per-label error write-up: `reasoned_opinion`

My worst label was `reasoned_opinion`, with an F1 of 0.000 in all three seeds.

**Which label it was confused with:** across the three seeds, 7, 9 and 9 of its 10 test posts were called `broad_question`, and the rest `specific_problem`. The model never predicted `reasoned_opinion` once.

**What the wrong examples have in common:** I read the 10 `reasoned_opinion` posts in the seed 42 test set. Each makes an argument or describes a real experience in the body, but 7 of the 10 end by asking the community something. Five end with a question mark, for example:

> "...What's your retention, and did you have to fight for it?"
>
> "...What part of the account lifecycle has caused the most trouble in your experience?"

Two more end with a request for input and no question mark, for example "am interested to hear what you'd leave out of phase one". The other three end on a statement, so the pattern is not universal.

My own rule is to remove the final question and judge the argument underneath. The model has no such rule, so my best explanation is that the closing question looks like `broad_question`. I can't prove that. Only 50% of `reasoned_opinion` test posts end with a question mark, against 55% of `broad_question` posts, so the question alone cannot be the whole reason, and `reasoned_opinion` was also my smallest label (66 posts).

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.185 | 0.585 | +0.400 |
| Macro F1 | 0.110 | 0.481 | +0.371 |
| F1 — `broad_question` | 0.167 | 0.655 | +0.489 |
| F1 — `reasoned_opinion` | 0.274 | 0.000 | -0.274 |
| F1 — `specific_problem` | 0.000 | 0.500 | +0.500 |
| F1 — `vague_worry` | 0.000 | 0.769 | +0.769 |

Both models were scored on the same 65 posts in `test_split.csv`. The baseline
used my definitions from `label_definitions.txt`.

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->
I predict that my trained model will beat the untrained model by the biggest margin on the labels `specific_problem` and `vague_worry`, because the untrained model scored zero on both of those, meaning it never once got one right. My model has actually studied hundreds of real posts that I labeled myself, so it should have picked up the habits that make a post a "specific problem" (a person describing one concrete thing that went wrong) or a "vague worry" (a person feeling anxious without saying exactly what about), while the untrained model only had my short written definitions to go on and had never seen a single example.

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->
**What my definitions were worth.** To find out whether the written definitions I made for my four labels actually helped, I ran the untrained model twice on the same 65 test posts, changing only one thing. In the first run I gave it my full definitions from `label_definitions.txt`, and it got 18.5% of the posts right (0.185). In the second run I took the definitions away and gave it only the bare label names, such as `vague_worry`, and it got 40.0% right (0.400). The gap between the two is 0.185 minus 0.400, which is −0.215, so my definitions were worth about negative 21 points: they made the untrained model worse, not better. I think this happened because this model does not read a definition the way a person does. It works by checking how well a post "fits" a short phrase, so a short name like "vague worry" gave it a clear target, while my longer descriptions gave it more words to match against and pulled it toward the wrong labels. I know this is a property of the untrained model and not a flaw in my labeling, because my trained model never read the definitions at all. It learned from my labeled examples and scored 0.585, which is higher than both runs. I am keeping the run with definitions (0.185) as my main baseline, since that is the setup the assignment describes, and I am also reporting the stronger names-only run (0.400) so the comparison is honest. My trained model beats both.



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

**Spread table from the notebook (section 6).** Device: `mps` (Apple Silicon
GPU), torch 2.2.2. Seeds 42, 7 and 2024, on the held-out posts of each seed's
own split.

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.585 | 0.569 | 0.662 | 0.092 |
| Macro F1 | 0.481 | 0.454 | 0.549 | 0.094 |
| F1 — `specific_problem` | 0.500 | 0.345 | 0.606 | 0.261 |
| F1 — `vague_worry` | 0.769 | 0.828 | 0.889 | 0.120 |
| F1 — `reasoned_opinion` | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 — `broad_question` | 0.655 | 0.645 | 0.700 | 0.055 |

Accuracy moved 0.092 across seeds. Enough that a criterion landing within that
band can't really be called either way.

**Run log:**

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.60 in all three seeds, and ≥ 0.15 above always guessing the biggest label | 0.585 | 0.569 | 0.662 | MISSED |
| 2. Every label's F1 | ≥ 0.50 for every label | 0.000 (lowest: `reasoned_opinion`) | 0.000 (lowest: `reasoned_opinion`) | 0.000 (lowest: `reasoned_opinion`) | MISSED |
| 3. Label balance | every label between 15% and 50% of my posts | 15.4% to 32.9% | 15.4% to 32.9% | 15.4% to 32.9% | MET |
| 4. Self-agreement | ≥ 32 of 40 relabeled posts match my first labels (80%) | 30 of 40 (75%), one check, not tied to a seed | same check | same check | MISSED |
| 5. Confidence | ≥ 75% correct among predictions at ≥ 80% confidence, at least 10 of them | 0.714 (most-confident third, stand-in) | 0.619 (most-confident third, stand-in) | 0.667 (most-confident third, stand-in) | MISSED |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

Seed 42, 65 held-out posts, device `mps`. Rows are true labels, columns are
the model's guesses.

| true \ predicted | specific_problem | vague_worry | reasoned_opinion | broad_question |
|---|---|---|---|---|
| **specific_problem** | 9 | 2 | 0 | 9 |
| **vague_worry** | 2 | 10 | 0 | 1 |
| **reasoned_opinion** | 3 | 0 | 0 | 7 |
| **broad_question** | 2 | 1 | 0 | 19 |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->
The biggest number off the diagonal is 9: nine real `specific_problem` posts were called `broad_question` by the model, while only 2 real `broad_question` posts went the other way. That is a direction, not just an error rate. It means the model did not learn where the line between those two labels sits, and when it is unsure it falls back on `broad_question`. Of my 20 `specific_problem` test posts, only 9 were right, so nearly half of them were read as a broad question instead. The model is very good at the opposite case, getting 19 of 22 `broad_question` posts right, which fits a model that has learned to say `broad_question` often.

A second, bigger problem shows in the `reasoned_opinion` row and column. The model never guessed `reasoned_opinion` even once, so that whole column is zeros and all 10 of my real `reasoned_opinion` posts were wrong: 7 were called `broad_question` and 3 were called `specific_problem`. This matches the F1 of 0.000 for `reasoned_opinion` in all three seeds, so it is not bad luck on one split. The model treats `reasoned_opinion` as a kind of `broad_question`, which is the boundary I already expected to be my hardest one when I wrote my criteria.

`vague_worry` is the cleanest label: 10 of its 13 posts were right. This matrix is from seed 42 only, so I will check it against the other two seeds, and against my agreement report, before I decide whether the cause is the model, my labels, or too few examples. I am not claiming a cause yet.



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥ 0.60 in all three seeds, and ≥ 0.15 above always guessing the biggest label | MISSED | 0.585, 0.569 and 0.662: only seed 2024 reaches 0.60, and the target has to hold in all three |
| 2 | Every label's F1 | ≥ 0.50 for every label in all three seeds | MISSED | `reasoned_opinion` is 0.000 in all three seeds, and `specific_problem` is 0.345 in seed 7 |
| 3 | Label balance | Every label between 15% and 50% of my posts | MET | The biggest label is 33% and the smallest is 15.4%, so all four are in range |
| 4 | Self-agreement | Agree with my own first labels on at least 32 of 40 relabeled posts (80%) | MISSED | 30 of 40 relabeled posts kept the same label (75%), 2 short of the target |
| 5 | Confidence | ≥ 75% correct among predictions at ≥ 80% confidence, with at least 10 such predictions | MISSED | Stand-in measure: the most-confident third was 0.714, 0.619 and 0.667 correct, below 0.75 in every seed |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->

**Criterion 1: MISSED.** Accuracy was 0.585, 0.569 and 0.662, so only seed 2024 reached 0.60. The main cause is one label the model never learned. `reasoned_opinion` scored 0.000 on precision, recall and F1 in all three seeds, so all 10 of its test posts were wrong every time. If those 10 had been right, seed 42 would have scored about 0.74 (48 of 65) instead of 0.585. My confusion matrix for seed 42 shows where they went: 7 into `broad_question` and 3 into `specific_problem`. The model also over-uses `broad_question` as a default. Across the three seeds its recall is high (0.86 to 0.95) but its precision is low (0.50 to 0.55), and in seed 42 it also swallowed 9 real `specific_problem` posts. The counts fit this: `reasoned_opinion` is my smallest label (66 of 428 posts, 15%, less than half of the 141 `broad_question` posts), and `broad_question` is my largest (33%). So I think the cause is too few examples of `reasoned_opinion`, together with a hard boundary between it and `broad_question`, which I already expected to be my fuzziest. I can't say my own labeling was inconsistent. My agreement check used the staff's posts and labels, and my two pile (a) slips were on other labels. It does show I can apply a written rule loosely, so I treat inconsistency as a possible extra cause, not a proven one.

**Criterion 2: MISSED.** The target was an F1 of at least 0.50 for every label in all three seeds. Two labels fell short. `reasoned_opinion` scored 0.000 in all three seeds. The model never predicted it once, and 7, 9 and 9 of its 10 test posts were called `broad_question`, with the rest called `specific_problem`. `specific_problem` scored 0.500, 0.345 and 0.606, so it missed in seed 7 alone. The two misses have different causes. For `reasoned_opinion`, I think the cause is too few examples combined with a hard label pair. It is my smallest label (66 of 428 posts), and the model never learned to separate it from `broad_question`, even though `vague_worry` learned well from only 87 posts. For `specific_problem`, too few examples doesn't fit, since it has 134 posts. Its recall is low and unstable (0.45, 0.25, 0.50), and it loses 9, 11 and 8 test posts to `broad_question`, so the issue is that boundary. A caveat: with only 20 test posts, one split can swing its F1 a lot, which fits the 0.26 spread across seeds.

**Criterion 3: MET.** My rule was that no label should have more than half of my posts, and none should have fewer than 15%, so that no label would be too big to dominate or too small to learn. I have 428 labeled posts. `broad_question` has 141 (32.9%), `specific_problem` has 134 (31.3%), `vague_worry` has 87 (20.3%) and `reasoned_opinion` has 66 (15.4%). All four are inside the range, so the criterion is met. The count describes my whole dataset, so it is the same in all three seeds. It was a close pass. Fifteen percent of 428 posts is about 64, and `reasoned_opinion` has 66, so it clears the minimum by only about two posts. That matters because `reasoned_opinion` is the label the model failed to learn in criteria 1 and 2. My rule technically held, but the 15% floor was too low to guarantee enough examples for the model to learn a label. I would not change this criterion, since it was measurable and I met it, but it is a clue for my diagnosis.

**Criterion 4: MISSED.** The target was to agree with my own first labels on at least 32 of 40 relabeled posts (80%). I relabeled 40 of my 50 hand-labeled posts without looking at my first labels, and 30 kept the same label (75%), so I missed by 2 posts. I did not save the relabels as a file, so this rests on my own count. For 5 of the changed posts I kept the details, and all 5 involved `specific_problem`: three were swaps with `broad_question` in both directions, one went to `vague_worry` and one to `reasoned_opinion`. `vague_worry` was my most stable label. The cause is a boundary I applied inconsistently. My second rule says a named thing must be the real subject of the question for a post to be `specific_problem`, and I did not apply it the same way twice. This likely contributes to the model's errors in criteria 1 and 2: across the three seeds it lost 9, 11 and 8 `specific_problem` test posts to `broad_question`, with F1 scores of 0.500, 0.345 and 0.606. I cannot say how much, because the pair may also be hard on its own, and 20 test posts is a small sample.

**Criterion 5: MISSED.** The target was that, among predictions where the model is at least 80% confident, at least 75% are correct, with at least 10 such predictions. The notebook saves a summary of the model's confidence for each seed, not a confidence for every prediction, so I could not count the predictions at 80% or more. As a stand-in, I used the model's most-confident third of predictions (21 per seed). Those were 0.714, 0.619 and 0.667 correct, so even the most confident group misses 0.75 in all three seeds. The evidence points to a model that is rarely sure about anything: its average confidence was only 0.40 to 0.44, so very few predictions can have reached 80%. Its confidence also says little about whether it is right: the average confidence on correct predictions (0.440, 0.433, 0.399) was almost the same as on wrong ones (0.415, 0.419, 0.393). I think the cause is that this is a hard four-label task for a small model trained on under 300 posts, which is the "task the model can't reach from this much data" cause. It was not clearly inconsistent labeling, since my agreement check was on the staff's labels and not my own. There is some signal, because the most-confident third beat the least-confident third in every seed (0.714 against 0.476, 0.619 against 0.476, 0.667 against 0.571), but not enough to reach the target.



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** 27 / 30 = 90%

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
> *The post:* "Everyone blames the hill at 18 miles. I split the field into people who ran the first half under 1:45 and over, and the slowdown after 18 was almost identical for both groups. If the hill were the problem the fast starters would fall apart harder."
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* The staff rules say a post is "analysis" only if it backs its argument with a fact you can actually check. Here, the writer tells us how they split the runners into two groups (1:45 for the first half), but then never tells us the numbers that matter: how much each group slowed down. The post only says the slowdown was "almost identical". That is the whole point of the argument, and we're asked to take it on trust. So I read it as a confident claim that sounds like research, which the rules call a "hot_take". I can see why staff chose analysis. The writer did set up a comparison, and the last sentence follows from it. The rules also don't say how much of the result has to be written out. So I think staff's reading is reasonable, but mine is defensible too.
>
> *Which pile:* (c). The rule is open to two readings here, and mine is defensible.

**2.**
> *The post:* "Three of us ran the same session on the same day, different shoes, within 10 seconds of each other over 5 miles. I'm not saying shoes do nothing, but whatever they do was smaller than the noise between three people."
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* I think staff is right. The staff rules say a post is "analysis" when it backs its point with a fact you can check, and the fact is the reason for the conclusion. This writer did exactly that. They gave a specific result: three runners, the same session, different shoes, all within 10 seconds over 5 miles. Their conclusion, that shoes matter less than the normal differences between runners, comes straight from that result. Take the 10-second gap away and the writer would have nothing to say. The writer is also careful. They say "I'm not saying shoes do nothing", which is not how someone sounds when they only want to announce an opinion. I labeled it hot_take mainly because three runners is a very small test. But the staff rules say nothing about how big a test has to be. They only ask whether the fact carries the argument, and here it does. So I judged the post by something the rule doesn't ask for.
>
> *Which pile:* (a). The rule covered it, and I applied it loosely.

**3.**
> *The post:* "The club needs to stop pretending the Tuesday session is for everyone. It isn't and it never has been."
>
> *Staff said / I said:* `hot_take` / `reaction`
>
> *My call, and why:* I think staff is right. The staff rules say a "reaction" is about something that just happened to the writer, and a "hot_take" is a general statement about how things are. This post is about the club, not about the writer. It doesn't describe anything that just happened, and "it never has been" looks back over a long time. I labeled it a reaction because it sounded frustrated, and because it mentions the Tuesday session. But a regular club session isn't a recent event, and the rules say a heated post is still a hot_take if it makes a general claim.
>
> *Which pile:* (a). The rule covered it, and I applied it loosely.

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:** I re-checked the 34 posts that I had labeled by hand with no AI help and that carried either `specific_problem` or `broad_question`, and applied my one rule the same way to each: if a named thing is the subject of the question, it's `specific_problem`, otherwise `broad_question`. 10 rows changed (8 from `specific_problem` to `broad_question`, 2 the other way). Nothing else was changed: not my taxonomy, my criteria, or any training setting.

**Which diagnosis pointed at it:** Criterion 4. When I relabeled 40 of my own posts, I matched my first labels on only 30 (75%), and the changes were mostly swaps between these two labels. That fits criterion 2, where `specific_problem` lost 9, 11 and 8 test posts to `broad_question`.

### Run Log — After

Same device (`mps`, Apple Silicon GPU) and same seeds as the before run. Written to `results_three_seeds_after.json`.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.60 in all three seeds, and ≥ 0.15 above always guessing the biggest label | 0.585 | 0.569 | 0.615 | MISSED |
| 2. Every label's F1 | ≥ 0.50 for every label | 0.000 (lowest: `reasoned_opinion`) | 0.000 (lowest: `reasoned_opinion`) | 0.000 (lowest: `reasoned_opinion`) | MISSED |
| 3. Label balance | every label between 15% and 50% of my posts | 15.4% to 34.3% | 15.4% to 34.3% | 15.4% to 34.3% | MET |
| 4. Self-agreement | ≥ 32 of 40 relabeled posts match my first labels (80%) | not re-measured | not re-measured | not re-measured | MISSED (unchanged from the before run) |
| 5. Confidence | ≥ 75% correct among predictions at ≥ 80% confidence, at least 10 of them | 0.810 (most-confident third, stand-in) | 0.714 (most-confident third, stand-in) | 0.762 (most-confident third, stand-in) | MISSED |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->
It helped a little in one place and not in others, so I would call it a mixed result. After I made the labels for the `specific_problem` / `broad_question` boundary consistent (10 rows changed), the model's overall accuracy did not improve: it stayed at 0.585 and 0.569 on two seeds and fell from 0.662 to 0.615 on the third. No verdict changed. But `specific_problem` became steadier: its F1 went from 0.500, 0.345 and 0.606 to 0.500, 0.550 and 0.500, so the gap between my best and worst seed shrank from 0.261 to 0.050, and it now reaches 0.50 on every seed. The model also leaned less on `broad_question`. Its recall dropped from 0.86, 0.91 and 0.95 to 0.77, 0.77 and 0.95 on the three seeds, and the confusion between the two labels became more even: in seed 42, 8 `specific_problem` posts were called `broad_question` and 5 went the other way, where before it was 9 and 2. I cannot say these small changes are real. Only 10 rows changed, my seeds already swing by several points, and a few of the test posts had their labels changed too, so the before and after test sets are not perfectly identical. `reasoned_opinion` stayed at 0.000 in every seed, which is expected because this change did not target it.



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
