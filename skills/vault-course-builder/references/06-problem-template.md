# Problem Template (Vault Course Builder)

Copy for every problem. One file per problem: `module-{N}/problems/problem_<N>.md`.

```markdown
---
topics: [topic-tested, related-topic]
tags: [course-code, module-N, problem]
course: coursecode
module: module-N
type: problem
created: "YYYY-MM-DD"
---

# Problem N — <Title>

**Maps to:** [[course/module-N/lessons/lesson-N-topic.md|Lesson N]]
**Concept tested:** <one or two phrases>

---

## Problem

<Full statement of the problem.>

---

## Hints

1. <Hint 1>
2. <Hint 2>

---

## Solution

<Step-by-step worked solution. Math as LaTeX.>

---

## Why This Works

<Explain the reasoning / concept that makes the solution correct.>

---

## Common Mistakes

1. <Mistake> — <how to avoid it>
```

## Rules

- `topics` = what the problem tests; `tags` include `problem` type, no `learned` yet.
- Always link back to the lesson it tests (wikilink).
- Include **Problem**, **Hints**, **Solution**, **Why This Works**, **Common Mistakes**.
- Write problems AFTER lessons (problems test what lessons teach).
- Math as LaTeX only.
