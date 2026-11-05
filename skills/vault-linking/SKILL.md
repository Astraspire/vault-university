---
name: vault-linking
description: "Use when the user wants to cross-link, tag, or wire up notes inside the vault — connecting lessons to their module overview, problems to the lesson they test, concept notes to real files, people to the courses they touched, and orphaned files to a proper tags line. Use when notes feel disconnected, when a wikilink is dangling or bare-title, when a file has no tags, or when the user asks to link, relink, or connect vault files. Generic: any course, any module, any vault. Tags and links EVERY file — courses, concepts, xlog logs, related people, and profiles — so nothing is left orphaned."
metadata:
  author: Danny Fetter
  version: "1.0.0"
---
# Vault Linking Skill

## Purpose

Turn a vault of plain Markdown notes into one coherent graph. This skill **tags and links every
file** in the vault — courses, concepts, xlog logs, related people, and profiles — so that no note
is orphaned and every `[[wikilink]]` resolves. Obsidian's Graph View reads the `[[wikilinks]]`
inside the notes; nothing links them by default. This skill wires them all together.

The vault is a "second brain": courses track learning, the Comfort Index tracks what the learner
knows, xlog tracks the timeline, people/profiles track the learner's life. Linking them means the
graph is also a map of how the learner understands things — which lets the agent explain new
concepts by bridging from what they already know.

This is **generic**: any course, any module, any vault, any learner. No course code, module
number, topic, or person name is hard-coded here — the scripts learn the vault's current state at
run time.

## WHEN IT RUNS — the wiring step

vault-linking is the vault's wiring step. It runs **after** `vault-course-builder` finishes a course
and **after** `vault-professor` creates/concepts a lesson, so nothing is orphaned. In short:

- **After the builder** — every time a course is built, run vault-linking to connect the course
  index to the Comfort Index, link lessons/problems to their module, and resolve dangling links.
  (The course-builder skill calls this in Step 11.)
- **After the professor** — every time a teaching session produces new or changed notes (concept
  files, updated Comfort Index, lessons), run vault-linking to wire them up. (The professor skill
  calls this in its Linking section.)
- **On demand** — when the user feels notes are disconnected, or before a fresh start, run it to
  re-wire the whole graph.

vault-linking does NOT edit the Comfort Index (that belongs to the teaching skill) and does NOT
build or teach (that belongs to the builder/professor). Its job is purely to make sure every note
is tagged, linked, and resolvable.

## THE LINKING STANDARD — read every time, no exceptions

These rules are the ONLY correct way to link a vault. If you are not following each line exactly,
you are linking wrong.

### 1. VAULT ROOT — find it before touching anything

The vault root is the folder you open in Obsidian and the root of the git repo holding `xlog/` and
`courses/`. It is set during setup and recorded in `VAULT_ROOT/_templates/VAULT-CONFIG.md` as
`VAULT_ROOT: <absolute path>`.

- Read `VAULT_ROOT/_templates/VAULT-CONFIG.md` to get the real path. Do NOT guess it.
- If the config file does not exist, ask the user where their vault lives. Do not proceed without
  it.

### 2. VAULT LAYOUT — what you are linking

```
VAULT_ROOT/
├── courses/
│   └── {COURSE-CODE}/
│       └── module-{N}/
│           ├── lessons/
│           ├── notes/
│           ├── problems/
│           ├── assignments/
│           └── other/
├── concepts/                # cross-cutting concept notes (flat or subfoldered)
├── xlog/YYYY/MM/YYYY-MM-DD.md
├── profiles/related-people/*.md
├── profiles/user/*.md
├── profiles/user/comfort-levels/00-Comfort-Index.md
├── 00-Index.md              # and any other root note
└── _templates/
```

Every markdown file here — including xlog logs, person files, and your user profile, which may have
**no front matter at all** — gets tagged and linked. A file with no front matter was simply ignored
before; that is fixed.

### 3. THE LINKING SCRIPTS — use these, not hand-rolled links

Two scripts live in the **skill folder**, not in the vault. They encode the linking conventions
and are the source of truth for what links exist and where they go. Do NOT hand-write the links
they produce.

Run them from anywhere; they auto-discover the vault root (the nearest folder containing
`courses/`, `xlog/`, `profiles/`, or `concepts/`).

#### `link_notes.py` — tag + wikilink EVERY file in the vault

```bash
python3 <skill>/scripts/link_notes.py
```

That's it. Drop your notes into the vault and run it once. It does four things, in this order:

1. **Tags orphaned files.** If a file has no `tags:` line, it adds one. Course files get the course
   code, module, and type tags. Non-course files get area-appropriate tags:
   `concepts/` → `[concept, <area>]`, `xlog/` → `[xlog]`, `profiles/related-people/` →
   `[person, related-people]`, `profiles/user/` → `[profile, user]` (the Comfort Index keeps its
   existing `comfort, comfort-registry, user-variables`). **Files with no front matter at all
   (xlog logs, person files, user profile) get a minimal front-matter block** with a `type:` and
   `tags:` — they were silently ignored before, not anymore.
2. **Links course lessons to their module overview** (discovered dynamically — no hard-coded paths).
3. **Links sibling lessons to their matching problem** where the teaches-first convention applies.
4. **Resolves dangling bare-title links ANYWHERE in the vault.** A `[[Some Title]]` with no path
   that points to exactly one real file is rewritten to `[[path/to/file|Some Title]]`. This is what
   wires concepts → people → courses into one resolvable graph.

It is idempotent — running it twice changes nothing the second time, so it is safe to run
repeatedly or on a schedule.

#### `extract_meta.py` — index every file in the vault (prints by default)

```bash
python3 <skill>/scripts/extract_meta.py            # print a per-area summary (default)
python3 <skill>/scripts/extract_meta.py --write meta.json   # ALSO write JSON to <path>
```

It scans **all areas** (courses, concepts, xlog, profiles, root notes), extracts front matter plus
the first heading and a short body preview, and prints a compact per-area summary. By default it
only prints — pass `--write <path>` to also emit a JSON index. It never drops an artifact into the
vault on its own. Run this after linking to confirm the vault looks right.

### 4. WIKILINK FORMAT — exact

Obsidian wikilinks use `[[...]]`:

- `[[path/to/file]]` — link by path.
- `[[path/to/file|Label]]` — link with a custom label.
- `[[Some Title]]` — link by title; Obsidian auto-resolves it if one file matches.

Links are written relative to the vault root so Obsidian resolves them.

### 5. TAGS — every file carries tags

- course files: course code, module (`module-N` or `COURSE_CODE/module-N`), and type
  (`lesson`, `problem`, `assignment`, `notes`, `other`, `index`).
- non-course files: the area-appropriate tags above.

Do not invent tags. Use exactly the scheme the scripts produce. No file is left without tags.

### 6. COMFORT INDEX — the spine, not a link target to fabricate

`VAULT_ROOT/profiles/user/comfort-levels/00-Comfort-Index.md` is the real-time map of everything
the learner knows and how comfortably — tiers run
`planned` → `low` → `medium` → `high` → `expert`. The linking skill does NOT edit the Comfort Index;
that belongs to the teaching skill. The Comfort Index is why the graph matters: linked notes are the
things being tracked. Do not confuse "linking notes" with "updating comfort tiers."

## LINKING WORKFLOW (step-by-step)

1. Run `python3 <skill>/scripts/link_notes.py` → tags and links every file in the vault.
2. Run `python3 <skill>/scripts/extract_meta.py` → read the per-area summary to confirm the vault
   looks right.
3. Verify: open a sample of the changed files and confirm the links and tags landed correctly.
4. Log the session to the vault xLog (see the vault-xlog skill).

## VERIFYING THE LINKING (do not skip)

- Re-read the changed files (open them) — confirm tags and `[[wikilinks]]` are present and correct.
- Confirm NO file was left without tags (spot-check an xlog log and a person file).
- If you cannot verify, say "I don't know" — do not claim linking succeeded without evidence.

## NOTES

- Always use the vault xLog path pattern: `VAULT_ROOT/xlog/YYYY/MM/YYYY-MM-DD.md`.
- The vault uses normal file tools for everything — there is no separate retired toolkit.
- Scripts live in the **skill folder** (`skills/vault-linking/scripts/`), never in the vault. The
  vault must not contain scripts, `.json` dumps, or other non-note artifacts.
- Personalization (the exact vault layout, area tag scheme, and the vault's real path) lives in the
  skill's own reference file, not in this generic SKILL.md. Read
  `references/vault-linking-personalization.md` for the concrete, vault-specific details.
