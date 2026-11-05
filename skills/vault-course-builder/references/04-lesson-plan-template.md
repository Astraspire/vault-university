# Lesson Plan Template (Vault Course Builder)

Write `module-{N}/lessons/lesson_plan.md` FIRST. It is the skeleton that maps each source
section to its lesson and problem numbers. Everything else hangs from it.

```markdown
---
topics: [module-N-overview]
tags: [course-code, module-N, lesson-plan]
course: coursecode
module: module-N
type: lesson-plan
created: "YYYY-MM-DD"
---

# Module N — Lesson Plan

**Course:** <FULL COURSE NAME> <Term>
**Source:** <source material — chapter / section>

## Overview

<Brief paragraph: what the module covers and how the lessons break down.>

## Lesson Map

| Lesson | Topic | Source Section | Problems | Status |
|---|---|---|---|---|
| Lesson 1 | <topic> | <section> | problem_1 | done |
| Lesson 2 | <topic> | <section> | problem_2 | done |
| Lesson 3 | <topic> | <section> | problem_3 | planned |

## Problems

| Problem | Topic | Maps To Lesson |
|---|---|---|
| problem_1 | <topic> | [[course/module-N/lessons/lesson-1-*.md|Lesson 1]] |
| problem_2 | <topic> | [[course/module-N/lessons/lesson-2-*.md|Lesson 2]] |

## Assignments

| Assignment | Topic | Maps To Lessons |
|---|---|---|
| (none yet) | | |

## Notes / Other

- <topic> → [[course/module-N/notes/<file>.md|notes file]]
```

## Rules

- Write the plan **before** lessons so you know how many lesson/problem files to create.
- Map every source section to a lesson; every lesson to ≥1 problem.
- Update statuses as lessons/problems are completed.
- Cross-link lessons and problems with wikilinks.
