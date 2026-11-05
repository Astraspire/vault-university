# Course Index Template (Vault Course Builder)

Create (or update) `courses/{COURSE-CODE}/COURSE-INDEX.md` for each course. This is the
course-level entry point that lists every module and its status.

```markdown
---
title: <COURSE CODE> Course Index
tags: [course-code, course-index]
course: coursecode
type: index
created: "YYYY-MM-DD"
---

# <COURSE CODE> — Course Index

<Full course name> · <Term/Section>

## Overview

<Brief paragraph: what the course covers, prerequisites, structure.>

## Modules

| Module | Topic | Lessons | Status |
|---|---|---|---|
| Module 1 | <topic> | [[course/module-1/lessons/lesson-1-*.md|Lesson 1]] … | complete |
| Module 2 | <topic> | [[course/module-2/lessons/lesson-1-*.md|Lesson 1]] … | in-progress |
| Module 3 | <topic> | (planned) | planned |

## Comfort Levels (per module)

> Synced with profiles/user/comfort-levels/00-Comfort-Index.md.

- **Module 1:** <topic> — <tier>
- **Module 2:** <topic> — <tier>

## Template For New Lessons

Copy this for each new lesson. Use full Obsidian syntax.

```yaml
---
topics: [topic-one, topic-two]
tags: [course-code, module-N, lesson, learned]
course: coursecode
module: module-N
type: lesson
created: "YYYY-MM-DD"
---
```

## Notes

- New topics start at `planned` in the comfort index.
- Every lesson cross-links to prior/next lessons.
```

## Rules

- One `COURSE-INDEX.md` per course, at the course root.
- List every module with a link to its first lesson and a status (`planned` / `in-progress` / `complete`).
- Keep a "Template For New Lessons" section so future builds stay consistent.
- Link modules to their lessons with wikilinks.
