# SETUP.md — Vault University

Follow these steps once to scaffold the vault skeleton. After this, the vault is ready for
`vault-course-builder` (to build courses) and `vault-professor` (to teach them).

> **Goal:** produce a working `VAULT_ROOT` with the correct folder structure, templates, config,
> and a git repo — so your agent can start teaching and logging immediately.

## Step 0 — Decide VAULT_ROOT

Pick the folder that will be `VAULT_ROOT`:

- It should be the folder you open in Obsidian.
- It should be writable and, ideally, already a git repo (or one you will `git init`).

Replace every occurrence of `VAULT_ROOT` in the skills and this file with that path. Write it into
`VAULT_ROOT/_templates/VAULT-CONFIG.md` (Step 1) so the skills can read it back.

## Step 1 — Create the folder skeleton

Run this from inside `VAULT_ROOT`:

```bash
mkdir -p xlog
mkdir -p courses
mkdir -p profiles/user/comfort-levels
mkdir -p profiles/related-people
mkdir -p concepts
mkdir -p _templates
```

## Step 2 — Create the config file

Create `VAULT_ROOT/_templates/VAULT-CONFIG.md`:

```markdown
---
title: "Vault Config"
---

# Vault Config

- VAULT_ROOT: <the absolute path to your vault>
- VAULT_TZ: <IANA timezone, e.g. America/New_York — detected at setup>
```

Detect the timezone with:

```bash
date +%Z
```

and record the IANA name (e.g. `America/New_York`) in the config. If none is set, the
`vault-xlog` skill detects the system zone and records it here.

## Step 3 — Create the templates

Create `VAULT_ROOT/_templates/` files so new notes follow the same style:

- **Daily note** — mirrors the xLog front-matter:
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

## Step 4 — Create the Comfort Index

Create `VAULT_ROOT/profiles/user/comfort-levels/00-Comfort-Index.md`:

```markdown
---
title: "Comfort Index"
tags: [comfort, index]
---

# Comfort Index

Real-time map of everything the learner knows and how comfortably — across the whole vault.

## Tiers

`planned` → `low` → `medium` → `high` → `expert`

## Topics

| Topic | Tier | Lessons |
| ----- | ---- | ------- |
|       |      |         |
```

## Step 5 — Initialize git (if needed)

```bash
cd VAULT_ROOT
git init
git add -A
git commit -m "Initial vault skeleton (Vault University)"
```

Optional — push to a remote:

```bash
git remote add origin <your-repo-url>
git push -u origin main
```

## Step 6 — Verify the skeleton

```bash
cd VAULT_ROOT
find . -type d -not -path '*/.git*' | sort
```

Expected top-level folders: `xlog`, `courses`, `profiles`, `concepts`, `_templates`.

## Done

The vault is now scaffolded. Your agent can:

- **Build courses** with `vault-course-builder` (from source material into `courses/`).
- **Teach** with `vault-professor` (driven off the Comfort Index).
- **Log** each session with `vault-xlog` (daily files in `xlog/`).
