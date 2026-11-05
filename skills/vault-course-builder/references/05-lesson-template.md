# Lesson Template (Vault Course Builder)

Copy this for every lesson. Use full Obsidian syntax (callouts, LaTeX, wikilinks). Math
must be rendered as LaTeX (use no images or ASCII for formulas).

```markdown
---
topics: [topic-one, topic-two, topic-three]
tags: [course-code, module-N, lesson]
course: coursecode
module: module-N
type: lesson
created: "YYYY-MM-DD"
---

# Lesson N — <Descriptive Title>

**Source:** <source section — chapter / section>
**Module:** Module N — <FULL COURSE NAME> <Term/Section>
**Objective:** <One sentence: "Students will be able to …">

---

## How This Fits Into Module N

Explain where this lesson sits in the module and how it connects to prior/next lessons and
earlier modules. Use wikilinks to related lessons:

- Build on [[course/module-M/lessons/lesson-X.md|previous lesson]]
- Prepares for [[course/module-M/lessons/lesson-Y.md|next lesson]]

> [!note] Hook (optional)
> A short hook tying the topic to something familiar.

---

## <Concept 1: The Core Idea>

Teach the concept directly and completely. Use headings, tables, and worked examples.

### <Sub-concept>

- Explanation.
- Key formula (LaTeX): $e^{i\pi} + 1 = 0$

> [!tip] Key insight
> A highlighted insight.

---

## Worked Example 1 — <Scenario>

```
<worked solution, code, or math>
```

**Why this works:** <explanation>

---

## Common Pitfalls

1. <Pitfall 1> — <fix>
2. <Pitfall 2> — <fix>
3. <Pitfall 3> — <fix>

---

## Video / Resources

- [Title](url) — brief description

---

## Check Your Understanding

1. <Question>
2. <Question>
3. <Question>

---

## Bridge to What You Know

Connect this concept to something the learner already understands at high comfort. Explain
it in a way that makes it intuitive for this specific learner.

---

**Next:** [[course/module-M/lessons/lesson-Y.md|next lesson title]]

**Prev:** [[course/module-M/lessons/lesson-X.md|previous lesson title]]
```

---

## Section Notes

- **Front-matter:** `topics` (subjects), `tags` (course, module-N, lesson — no `learned`
  yet), `course`, `module`, `type: lesson`, `created`.
- **Source header** — ties the lesson to the source material.
- **Objective** — one sentence, student-centered.
- **"How This Fits"** — mandatory cross-link section.
- **Teach-First** — teach the concept fully first, then layer "why it matters."
- **Worked Examples** — at least one, with a "Why this works" explanation.
- **Common Pitfalls** — 3 concrete mistakes + fixes.
- **Check Your Understanding** — 3–7 questions.
- **Bridge to What You Know** — connect to a topic the learner already has at high comfort.
- **Next / Prev** wikilinks at the very bottom.
- **Math = LaTeX only.** Inline `$...$`, block `$$...$$`.
