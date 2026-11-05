# Full Worked Example — Lesson (Generic)

This is a **condensed, annotated** example showing the conventions in action. It is a
generic worked example — replace every placeholder with the real course content you are
building. The style is clean and current: `topics`, `tags`, `course`, `module`, `type`,
`created`, with wikilinks and LaTeX.

## Annotated Lesson (excerpt)

```markdown
---
topics: [linear-equation, slope, y-intercept, standard-form]
tags: [coursecode, module-1, lesson, planned]
course: coursecode
module: module-1
type: lesson
created: "2026-11-03"
---

# Lesson 1 — Linear Equations

**Source:** <chapter / section>
**Module:** Module 1 — <FULL COURSE NAME> <Term>
**Objective:** Students will be able to write and interpret a linear equation in slope-intercept form.

---

## How This Fits Into Module 1

Explain where this lesson sits in the module and how it connects to prior/next lessons.

- Builds on [[course/module-M/lessons/lesson-X.md|previous lesson]]
- Prepares for [[course/module-M/lessons/lesson-Y.md|next lesson]]

> [!note] Hook (optional)
> A short hook tying the topic to something familiar.

---

## What "Linear" Actually Means

The word **linear** is a technical term. An equation is **linear** when every variable
appears only to the first power and no variables are multiplied together.

A linear equation in $n$ variables has the shape:

$$a_1 x_1 + a_2 x_2 + \cdots + a_n x_n = b$$

where $a_i$ are **coefficients**, $x_i$ are **variables**, $b$ is the **constant**.

### The Rules That Make It Linear

An equation is **not** linear if it contains:

- A variable squared or higher: $x^2$, $y^3$.
- Two variables multiplied together: $xy$, $x_1 x_2$.
- A variable inside a root, log, trig, or exponential: $\sqrt{x}$, $\ln x$, $\sin x$, $2^x$.

> [!tip] Key insight
> A linear relationship has a constant rate of change — that's what makes its graph a
> straight line.

---

## Slope-Intercept Form

A linear equation written as

$$y = m x + b$$

has slope $m$ and $y$-intercept $b$.

- **Slope** $m$ — the rate of change: how much $y$ changes per unit of $x$.
- **$y$-intercept** $b$ — where the line crosses the $y$-axis (where $x = 0$).

### Bridge to What You Know

If you already understand "rate of change" from another topic, connect it here: the slope
$m$ *is* the rate of change. A steeper line means a larger $|m|$; a flat line means $m = 0$.

---

## Worked Example

Find the slope and $y$-intercept of $2x + 3y = 6$.

```
2x + 3y = 6
3y = -2x + 6
y = (-2/3)x + 2
```

**Slope:** $m = -\tfrac{2}{3}$ · **$y$-intercept:** $b = 2$.

**Why this works:** isolating $y$ puts the equation in $y = mx + b$ form, where $m$ and $b$
read off directly.

---

## Common Pitfalls

1. Forgetting to flip the sign of the slope when moving a term — keep the sign with the coefficient.
2. Confusing slope with intercept — slope is the rate, the intercept is the starting value.
3. Leaving a variable squared — that's not linear.

---

## Check Your Understanding

1. Write $4x - y = 8$ in slope-intercept form.
2. What is the slope of a horizontal line?
3. Is $y = 2^x$ linear? Why or why not?

---

**Next:** [[course/module-M/lessons/lesson-Y.md|next lesson title]]

**Prev:** [[course/module-M/lessons/lesson-X.md|previous lesson title]]
```

## Why This Is A Good Example

- **Front-matter** has `topics`, `tags` (course, module, type, `planned`), `course`, `module`, `type`, `created`.
- **LaTeX math** throughout ($...$, $$...$$) — use no images or ASCII for formulas.
- **Bridge to What You Know** — explicitly connects to a topic the learner already understands.
- **Cross-links** via wikilinks to related lessons (`[[...]]`).
- **Teach-First structure** — teach the concept fully, then point to the practice phase.
- **`planned` tag** because the topic hasn't been studied yet.

## Companion Problem (excerpt)

```markdown
---
topics: [solving-linear-equation]
tags: [coursecode, module-1, problem, planned]
course: coursecode
module: module-1
type: problem
created: "2026-11-03"
---

# Problem 1 — Solving a Linear Equation

**Maps to:** [[course/module-1/lessons/lesson-1-linear-equations.md|Lesson 1]]

## Problem
Solve for $x$:  $2x + 6 = 3x - 4$.  Verify by substituting back.

## Solution
```
2x + 6 = 3x - 4
6 + 4 = 3x - 2x
10 = x
```
**Check:** $2(10) + 6 = 26$ and $3(10) - 4 = 26$. ✓

## Why This Works
Isolate $x$ on one side, then verify by plugging the value back into the original equation.
```

## Companion Course Index

The course index (`references/08-course-index-template.md`) shows the modern course-index
style: a course structure table, per-module sections with a sequential lesson path and
Next links, and a Template for New Lessons section.
