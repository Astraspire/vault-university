# Vault Course Directory Design

The vault stores course content in an indexed + tagged structure so it can be cross-linked
and comfort-tagged. This layout is generic — it works for any subject, level, or school.

## Top-Level Layout

```
VAULT_ROOT/
├── courses/
│   └── {COURSE-CODE}/
│       ├── COURSE-INDEX.md          # course-level entry point
│       └── module-{N}/
│           ├── lessons/
│           │   ├── lesson_plan.md   # maps source -> lessons + problems
│           │   └── lesson-<n>-<topic>.md
│           ├── problems/
│           │   └── problem_<n>.md
│           └── assignments/
│               └── assignment-<n>.md (or project-<N>.md)
├── profiles/
│   └── user/
│       └── comfort-levels/
│           └── 00-Comfort-Index.md  # real-time map of what the learner knows
└── xlog/
    └── YYYY/
        └── MM/
            └── YYYY-MM-DD.md        # daily session log
```

## The Comfort Index

`VAULT_ROOT/profiles/user/comfort-levels/00-Comfort-Index.md` is a real-time map of everything
the learner knows and how comfortably — across the whole vault, not just one course.

- New topics start at `planned`.
- Tiers: `planned` → `low` → `medium` → `high` → `expert`.
- It is updated as the learner studies; the course builder promotes a tier only after the learner studies it.

## Cross-Linking

- Lessons link to prior / next lessons.
- Problems link to the lesson they test.
- The course index links to each module's first lesson.
- Topics in lessons are tagged so the comfort index can find them.

## Tags

Every file's front-matter `tags` include:

- the course code
- `module-N`
- the type (`lesson`, `problem`, `assignment`, `lesson-plan`, `index`)

Add `learned` only after the topic has actually been studied.
