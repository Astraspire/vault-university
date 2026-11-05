# Vault Integration (Vault Professor)

Where everything lives and how the professor maps onto the vault structure. This is generic —
it works for any subject, level, school, or time frame.

## The vault

```
VAULT_ROOT/
├── courses/
│   └── <CODE>/
│       ├── COURSE-INDEX.md          # course-level entry point
│       └── module-<N>/
│           ├── lessons/
│           │   ├── lesson_plan.md   # maps source -> lessons + problems
│           │   └── lesson-<n>-<topic>.md
│           ├── problems/
│           │   └── problem_<n>.md
│           └── assignments/
│               └── assignment-<n>.md (or project-<N>.md)
├── concepts/   # on-the-fly concept files for uncovered material
├── profiles/
│   └── user/
│       └── comfort-levels/
│           └── 00-Comfort-Index.md  # source of truth for every topic's comfort
└── xlog/               # conversational timeline — where the learner is right now
    └── YYYY/
        └── MM/
            └── YYYY-MM-DD.md
```

## The Comfort Index

`VAULT_ROOT/profiles/user/comfort-levels/00-Comfort-Index.md` is the single source of truth for
every topic's learning status. It holds each topic's **comfort tier** + which **lessons**
teach it. Read it BEFORE every session to know exactly where the learner is.

### Tiers

`planned` → `low` → `medium` → `high` → `expert`

- **planned** — the topic exists but hasn't been studied yet. Default for every new topic.
- **low** — introduced but still shaky.
- **medium** — usable with some effort.
- **high** — usable confidently.
- **expert** — can teach it and connect it to other topics.

### Rules

- One file. Read it and reference it in place.
- New topics always start at `planned`.
- Promote on evidence: the learner studies a topic, then the index is updated.
- Confirm tier changes with the learner; base them on the learner.s understanding.
- Keep it broad — it tracks everything the learner encounters, not just course content.

## The xLog

The **xLog** (`VAULT_ROOT/xlog/YYYY/MM/YYYY-MM-DD.md`) is the source of the current section — which
module, which lesson, what's DONE vs. what's next. The course routing pointer says *which vault
folders to open*; the xLog says *where in that course the learner is right now*.

To find the current section:

1. Open the `vault-xlog` skill and read the current day's file (search backwards if the most
   recent entry is further back — use the most recent session bullet to anchor the topic).
2. Then open the matching lesson file under
   `VAULT_ROOT/courses/<CODE>/module-<N>/lessons/` and teach to that point.

> Read the vault xLog only through the `vault-xlog` skill — not by running retired toolkit
> scripts or a direct shell `cat` against the file.

## Concept files

`VAULT_ROOT/concepts/` holds material not already in a lesson. Create one on the fly for any
concept uncovered while teaching. Log content only, and link it to the related lesson if one
exists.

## Grounding flow (every session)

1. `skills-index` → route.
2. `vault-xlog` skill → read today's xLog (+ prior days if needed).
3. Open `references/COURSE-ROUTING.md`-equivalent: find the current course folder, then the
   current lesson/concept the xLog names.
4. Comfort Index → the current topic's tier.
5. Every task-specific skill this turn matches.

Grounding outranks momentum. A response produced without grounding is wrong.

## If the active course changes

The xLog is the live tracker. When a new course starts, the xLog records it and the current
section updates to match. Keep it in sync.
