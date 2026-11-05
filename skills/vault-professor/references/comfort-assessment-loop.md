# Comfort Assessment Loop (Vault Professor)

The Comfort Index is a real-time map of everything the learner knows and how comfortably —
across all conversations and all topics, not just one course. This skill owns the loop that
keeps it current: after each lesson/segment, assess, re-assess, and re-label.

The loop is lightweight and runs quietly at the end of a segment, once the lesson is complete.
lesson in progress — the teaching comes first, the relabelling follows.

## Why this loop

The student's comfort index must be formally re-assessed or re-labelled over time. Without relabelling, the Index goes stale:
Without this loop: 
- topics the learner now holds stay mislabelled,
- bridges that should carry new concepts stay invisible,
- gaps that were filled (or newly opened) go untracked.

This loop closes that gap. It is the difference between an Index that merely records and one
that stays accurate as the learner's understanding changes.

## The loop (5 steps, at the end of a lesson/segment)

### 1. Observe — gather evidence

Collect the signals from this segment. Evidence, not vibes:

- Which microsteps did the learner do unaided?
- Which needed a hint, and how big?
- Where did they stall, self-correct, or push back confusedly?
- Could they explain it back in their own words?
- Did they reach a correct answer on their own, or only after scaffolding?

### 2. Re-assess — assign the tier the evidence supports

Map the evidence to a tier. Promote only on evidence the learner can point to.
actually demonstrated:

| Evidence this segment                                    | Tier            |
| -------------------------------------------------------- | --------------- |
| Did it unaided AND could explain it back                 | `high` / `expert` |
| Did it with one hint                                     | `medium`        |
| Needed several hints, or got it wrong then fixed it      | `low`           |
| New, just introduced, not yet held                       | `planned` / `low` |

### 3. Relabel — update the Index, then confirm

- Update the Comfort Index tier for the topic (and any new concept file created this segment).
- Confirm the new tier with the learner — "You're at `medium` here, does that feel right?" —
Assign a label the learner would accept, and confirm it with them.
Promote on evidence: a tier moves only because the evidence (and the learner.s agreement)
  supports it.

### 4. Re-assess bridges & gaps

- **Bridges** — what concept did the learner now hold that can carry NEW material? Note it as
  an anchor to bridge future concepts from.
- **Gaps** — what remains unfilled? A stall, a wrong answer, a confused pushback, a topic they
  couldn't reach. A gap must be filled before advancing past it.
- **Re-check old bridges & gaps** — a bridge that was shaky may now be solid; a gap that was
  filled can be retired; a topic that looked solid may have reopened.

### 5. Log — record it

- Update the Comfort Index with the new tiers, bridges, and gaps.
- Append a session bullet to the day's xLog (via the `vault-xlog` skill) noting what was
  taught, the tier changes, and any bridges or gaps.

## Rules

Runs at the END of a segment, once the lesson is complete.
One relabelling per topic per segment, to keep the Index stable.
- Confirm with the learner; the Index reflects their reality, not your guess.
New topics start at `planned`; promote only on evidence.
- Keep the Index broad — it tracks everything the learner encounters, not just course content.
Promote or demote a tier only on the evidence the learner can point to.
  supports just to keep things "simple."
