# Front-Matter (Vault Course Builder)

Every course file starts with YAML front-matter. Keep it consistent across a course.

```yaml
---
topics: [topic-one, topic-two, topic-three]
tags: [course-code, module-N, lesson]
course: coursecode
module: module-N
type: lesson
created: "YYYY-MM-DD"
---
```

## Fields

- **topics** — the subjects this file covers (the concepts, not the tags).
- **tags** — machine-readable labels: the course code, `module-N`, and the type.
  Include `learned` only after the topic has actually been studied.
- **course** — the course code placeholder (e.g. `coursecode`).
- **module** — `module-N` for the module this belongs to.
- **type** — `lesson`, `problem`, `assignment`, `lesson-plan`, or `index`.
- **created** — the build date, `YYYY-MM-DD`.

## Rules

- Tags always include the course code, the module, and the type.
- `learned` is added only after the topic has been studied.
- Keep `topics` specific enough to find the file later; keep `tags` structural.
