# Comfort Levels (Vault Course Builder)

The comfort index is a **real-time map of everything the learner knows and how comfortably**
— across all conversations and all topics, not just the content of one course.

## Tiers

`planned` → `low` → `medium` → `high` → `expert`

- **planned** — the topic exists but hasn't been studied yet. This is the default for every
  new topic a course introduces.
- **low** — the learner has been introduced to it but is still shaky.
- **medium** — the learner can use it with some effort.
- **high** — the learner can use it confidently.
- **expert** — the learner can teach it and connect it to other topics.

## How the Course Builder Uses It

1. **Read it first** — before building, open `00-Comfort-Index.md` and see what the learner
   already knows at high comfort. Those are the anchors to bridge new concepts from.
2. **Set new topics to `planned`.** Assume no prior knowledge until the index shows otherwise.
3. **Bridge known → unknown** — when teaching a new concept, explicitly connect it to a
   topic the learner already has at high comfort.
4. **Promote on study.** The learner studies a topic, then the index is updated. The
   course builder bumps a tier only on that evidence.

## Rules

- One file: `VAULT_ROOT/profiles/user/comfort-levels/00-Comfort-Index.md`.
- New topics always start at `planned`.
- Confirm tier changes with the learner; base them on the learner.s understanding.
- Keep it broad — it tracks everything the learner encounters, not just course content.
