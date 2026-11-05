---
name: vault-xlog
description: Log daily sessions to the vault xLog format (one file per day, organized by year/month).

metadata:
  author: Danny Fetter
  version: "1.0.0"
---

# Vault XLog Skill

## Purpose

Log daily sessions to the vault xLog format. This is the vault-specific logging system. 

## The shared logging sink

`vault-xlog` is the one logging skill. Every other vault skill calls it, and it calls none of them:

- **vault-course-builder** logs after it builds a course (its Step 12).
- **vault-professor** logs after every lesson/segment ends (its Logging section).
- **vault-linking** logs after it wires the vault (its Step 8).

If any of those skills runs, run `vault-xlog` too — the trail is what makes the vault persist across
sessions. Log last, after the work is done and (for builder/professor) the course is linked.

## THE LOGGING STANDARD — MUST link, not "should"

Logging without linking leaves the vault disconnected — orphaned notes, dangling links, a Comfort
Index that no longer reflects what's actually wired together. So when you log, you **must** also run
the `vault-linking` skill to tag and wire up every note or change your session produced. Every xLog entry is accompanied by vault-linking. The professor and
course-builder skills are written this way — they run vault-linking before/around their logging; you
follow the same pattern. Log and link together, every time.

## THE LOGGING STANDARD — read every time, no exceptions

These rules are the ONLY correct way to timestamp, order, and insert session entries. There is
no ambiguity. If you are not following each line exactly, you are logging wrong.

### 1. TIMESTAMP ZONE — always the vault's configured zone

The server clock is the wrong source of truth. The vault's configured zone is set during setup
(detected once, then recorded in `VAULT_ROOT/_templates/VAULT-CONFIG.md`). Compute the correct
time with:

```bash
TZ="<VAULT_TZ>" date "+%Y-%m-%d %H:%M %Z"
```

- If no vault zone is recorded yet, detect the system's local zone with `date +%Z` and record
  it in `VAULT_ROOT/_templates/VAULT-CONFIG.md`, then use it.
- The `date` field in the filename and the `HH:MM` in the session bullet BOTH come from this
  command — NOT from `date` alone, NOT from the system prompt's stated time (the system clock
  can be wrong; the `TZ=... date` command is the source of truth).
- If the vault-zone date from the command differs from what you assumed, USE THE COMMAND'S DATE.
  This is the #1 cause of wrong-file logging.

### 2. FILE PATH — derived from the vault-zone date, not the server date

- Path: `VAULT_ROOT/xlog/YYYY/MM/YYYY-MM-DD.md`
- The `YYYY-MM-DD` is the vault-zone date from Step 1.
- If the file does not exist, create it with the exact front-matter + structure below.

### 3. FILE STRUCTURE (create only if the file does not exist)

```markdown
---
title: "Month DD, YYYY"
date: YYYY-MM-DD
tags: [xlog, daily]
---

# Month DD, YYYY

## Sessions

## Notes

## Pending Items
1.
```

### 4. SESSION BULLET FORMAT — exact

```
- [HH:MM TZ] Session N — <brief description>
```

- `HH:MM` = 24-hour time from the vault-zone date command. No seconds. No AM/PM.
- `Session N` = the next integer after the highest session number already in the file. Count
  existing `Session N` bullets. If none exist yet, N = 1.
- `<brief description>` = what actually happened, in factual terms. No narration, no emotional
  filler.

### 5. INSERTION — append under `## Sessions`, keep chronological order

- Find the `## Sessions` header in the file.
- Insert the new bullet as the LAST bullet under `## Sessions` (append).
- If the file already has entries out of chronological order, insert the new entry in its
  correct time position (after the last entry whose timestamp is earlier, before any entry whose
  timestamp is later). Place it correctly.
- Only add the new bullet; leave existing entries untouched.

### 6. SESSION NUMBERING — global per-day counter

- Session numbers increment across the entire day file. If the last entry is `Session 20`, the
  next is `Session 21`.
- Increment session numbers across the entire day file, keeping each number unique.

## APPENDING A SESSION (step-by-step)

1. Run `TZ="<VAULT_TZ>" date "+%Y-%m-%d %H:%M %Z"` — record the vault-zone date and time.
2. Build the path `VAULT_ROOT/xlog/YYYY/MM/YYYY-MM-DD.md` from that date.
3. Check if the file exists. If not, create it with the structure in Step 3.
4. Count existing `Session N` bullets. The new number = highest + 1.
5. Append the bullet under `## Sessions` in correct chronological position (usually last).

## NOTES

- Keep entries concise and factual.
- Always use the vault xLog path pattern: `VAULT_ROOT/xlog/YYYY/MM/YYYY-MM-DD.md`.
