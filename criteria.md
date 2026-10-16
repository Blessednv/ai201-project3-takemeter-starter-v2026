# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1.

<!-- Your criterion. It must name a number. -->
Overall accuracy on the held-out test set is at least **0.60** in all three
seeds, and at least **0.15** above the accuracy of always guessing my biggest
label.

**Target:** accuracy ≥ **0.60**, and ≥ **0.15** above the biggest-label guess.

**Why this target:**
With four labels, random guessing gets about 25%. I expect about 68 test posts
(426 posts, about 16% held out), so each post moves the score by about 1.5
points and the three seeds will differ. I chose 0.60 and not higher because of
that, and because the `reasoned_opinion` vs. `broad_question` boundary is
fuzzy. The 0.15 margin is there because my balance rule allows one label up to
50%, and a model that always guessed that label would score 0.50.

---

## 2.

<!-- Your criterion. -->
Every label has an F1 of at least **0.50** on the held-out set, in all three
seeds.

**Target:** F1 ≥ **0.50** for every label.

**Why this target:**
The overall number can look fine while one label is ignored, so this sets a
floor for each label. My smallest label could be as low as 15% of the data
(about 64 posts), which gives only about 10 test posts, so its F1 will jump
between seeds. That is why this floor is looser than criterion 1. I expect
`reasoned_opinion` and `broad_question` to be the weakest, since that is my
hardest boundary.

---

## 3.

<!-- Your criterion. -->
No label has more than **50%** of my labeled posts, and none has fewer than
**15%**.

**Target:** every label between **15%** and **50%** of the labeled posts.

**Why this target:**
I am labeling all 426 posts, so the counts follow what people actually post
and I cannot choose them. I expect `specific_problem` and `broad_question` to
be the biggest, so I allow up to 50%, which is below the README's 70% cap. The
15% minimum is about 64 posts, which gives about 10 in the test split, enough
for a usable F1 on the smallest label.

---

## 4.

<!-- Your criterion. -->
When I relabel **40** of my own posts at least a day later, without looking at
my first labels, I agree with myself on at least **32 of 40 (80%)**.

**Target:** agreement ≥ **32 of 40 (80%)**.

**Why this target:**
Random relabeling would agree about 25% of the time. I am not asking for 90%
because I know the `reasoned_opinion` vs. `broad_question` line is subjective,
even with my written decision rule. I use 40 posts so that one disagreement
moves the result by only 2.5 points. If I fall below 80%, my definitions are
too vague for a model to learn them consistently.

---

## 5.

<!-- Your criterion. -->
Among test predictions where the model is at least **80%** confident, at least
**75%** are correct, and at least **10** test predictions reach that
confidence.

**Target:** ≥ **75%** correct at ≥ **80%** confidence, with ≥ **10** such
predictions.

**Why this target:**
A confident prediction should be right more often than the overall 0.60, or the
confidence score tells me nothing. I set the bar at 75%, a little under the
confidence level, because a small, lightly trained model is unlikely to be
perfectly calibrated. The minimum of 10 stops a handful of easy predictions
from passing or failing this by luck. I did not set it higher, because with
about 68 test posts a small model may rarely be 80% sure.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
