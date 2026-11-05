# Vault University

A portable, skill package that lets any AI agent or assistant build out a
**learning + logging vault** for any learner, teach them courses through it, and track exactly
what they know over time.

It is designed to be handed to anyone with an Obsidian vault (or any harness, API key, or local
model). There are no hard-coded paths — you set it up once, and your
agent runs it.

---

## What is Obsidian?

Obsidian is a free, local note-taking app that stores everything as plain Markdown files in a
folder — called a **vault** — that you fully own. No cloud lock-in, no format gymnastics, and it
works offline. That last point matters here: the vault is just a folder of text files, which is
exactly why these skills can read it, write to it, and keep a clean history of it (via git).

**Why we use it:** the skills build course content, track what a learner knows, and log every
session into the vault. Obsidian is the home for all of that — and its Graph View lets you explore
how concepts, courses, and sessions link together.

**Get it (free):**

- Desktop (Windows, macOS, Linux): <https://obsidian.md/download>
- Mobile (iOS, Android): available on the App Store and Google Play — search "Obsidian"
- Web: <https://obsidian.md>

Set up is quick: install Obsidian, click **Create a new vault**, and you have a folder on your
computer. That folder becomes `VAULT_ROOT` — the root everything else hangs off of. See
[**Prerequisites**](#prerequisites) for the full checklist.

---

## What's in the box

Four skills, in `skills/`:

| Skill | What it does |
| --- | --- |
| **vault-course-builder** | Builds lessons, problems, assignments, and module indexes from source material into the vault's course structure. |
| **vault-professor** | Teaches any course to any learner, driving instruction off the vault Comfort Index and tracking understanding in real time. |
| **vault-linking** | Tags and links **every** file in the vault — courses, concepts, xlog logs, related people, and profiles — so nothing is orphaned. Resolves dangling links and tags files that have none. |
| **vault-xlog** | Logs each day's session to a daily file (`VAULT_ROOT/xlog/YYYY/MM/YYYY-MM-DD.md`). |

Supporting references (pedagogy + templates) ship alongside each skill.

---

## The vault layout

Once set up, the vault looks like this (the internal structure stays the same; only the root
folder is yours to name):

```
VAULT_ROOT/
├── xlog/YYYY/MM/YYYY-MM-DD.md        # daily session log
├── courses/{CODE}/module-{N}/
│   ├── lessons/
│   ├── problems/
│   └── assignments/
├── profiles/user/comfort-levels/00-Comfort-Index.md
├── profiles/related-people/
├── concepts/                          # on-the-fly concept files
└── _templates/
```

- **xLog** — the conversational timeline. Each day is one file, organized by year/month.
- **Courses** — indexed + tagged course content, cross-linked and comfort-tagged.
- **Comfort Index** — a real-time map of everything the learner knows and how comfortably,
  across every conversation and every topic. New topics start at `planned`; tiers move up as
  the learner studies them.
- **Concepts** — material uncovered while teaching, logged on the fly.
- **Profiles** — user profiles and related people.
- **00-Index.md** — a landing note that ties the whole vault together (optional but recommended).

> **This is a "second brain."** Beyond courses, the vault also tracks the learner's life — the
> people they work with, their preferences, and the timeline of their sessions — so the agent can
> explain new concepts by bridging from what they already know. The Comfort Index is the spine that
> ties learning to understanding; the graph is a map of how they think.

---

## Prerequisites

To install and use this package you need:

1. **An Obsidian vault** — any folder you open in Obsidian. This is where `VAULT_ROOT` lives. Get
   Obsidian from <https://obsidian.md/download> and create a new vault to start.
2. **A git repository** — the vault should be a git repo so sessions are versioned and backed up.
   (If it isn't yet, `git init` it.)
3. **An AI agent / harness** — the agent that will run these skills. Any harness works: API key,
   local model, or cloud model.

---

## Install

All four skills install with the standard agent-skills installer (Vercel Labs `skills` CLI, run
via `npx`):

```bash
npx skills add Astraspire/vault-university -y
```

That fetches the repo, discovers every `SKILL.md` under `skills/`, and installs all four skills
(`vault-course-builder`, `vault-professor`, `vault-linking`, `vault-xlog`) into your agent's
skills directory. It installs as a symlink by default, so updates flow through automatically.

**Scope & agent options**

| Command | What it does |
| --- | --- |
| `npx skills add Astraspire/vault-university -g` | Install globally (across all projects). |
| `npx skills add Astraspire/vault-university -a claude-code` | Target one agent (`claude-code`, `cursor`, `codeex`, …). Omit `-a` to install to all detected agents. |
| `npx skills add Astraspire/vault-university --copy` | Copy files instead of symlinking. |
| `npx skills add Astraspire/vault-university --skill vault-xlog` | Install only selected skills. |
| `npx skills add Astraspire/vault-university --all` | Install every skill to every agent (`--skill '*' --agent '*' -y`). |

After installing, open your vault in Obsidian and make sure it's a git repo (`git init` if needed).
Then have your agent read `SETUP.md` and follow it to scaffold the vault skeleton.

> **Tip — preview first.** See what a repo contains before installing with:
> `npx skills add Astraspire/vault-university -l`

---

## User workflow — import, teach, and traverse

Here's the everyday loop once everything is installed and your vault is set up:

**1. Import course material.**
Point **vault-course-builder** at your source (a textbook, slides, PDF, syllabus, or notes). It
builds structured lessons, problems, assignments, and module indexes into `courses/{CODE}/module-N/`
and seeds the Comfort Index.

**2. Teach / study.**
Have **vault-professor** teach you the course. It reads the Comfort Index first — it already knows
what you hold comfortably and bridges new ideas from there — and updates your comfort tiers as you
grow. Ask questions, ask it to go deeper, ask it to re-check your understanding.

**3. Keep it wired.**
**vault-linking** tags and cross-links everything as notes are created or edited, so no lesson,
concept, person, or session is orphaned. If you ever feel like notes are disconnected, run it to
re-wire the graph. It also resolves bare `[[wikilinks]]` so nothing dangles.

**4. Log the session.**
**vault-xlog** records every session to `xlog/YYYY/MM/YYYY-MM-DD.md`, so the trail of what was
taught and where you stand persists across sessions and restarts.

**Traverse your vault.**
- **In Obsidian:** open `VAULT_ROOT` as a vault and use **Graph View** to explore how courses,
  concepts, people, and sessions link. Click any node to open it. The Comfort Index is your
  dashboard — open it to see your current understanding at a glance.
- **Concept bridges:** because everything is linked, asking "how does this relate to what I already
  know?" surfaces the actual connections in the graph — that's the second-brain payoff.

---

## Where the paths go

This package uses `VAULT_ROOT/` as a placeholder for wherever your vault lives. Before your agent
builds anything, set the real path — either in the skills or in a config file the skills read.

The skills expect `VAULT_ROOT` to be:

- The folder you open in Obsidian, and
- The root of the git repo that holds your xLog and courses.

Set it once during setup, and the skills take it from there.

---

## How the pieces fit together

The four skills form one pipeline — each calls the next, and they all call `vault-xlog` to log:

1. **vault-course-builder** builds course content from source material into `courses/`.
2. **vault-linking** wires the new course into the ENTIRE vault — tags it, links the course index to
   the Comfort Index, resolves dangling links, and connects related concepts/people. Run this after
   **every** build (and after every teaching session), so nothing is orphaned and the professor can
   bridge to the course cleanly.
3. **vault-professor** teaches that content, reading the Comfort Index to know what the learner
   already holds and bridging new concepts from it. After each lesson it updates the Comfort Index
   and runs vault-linking to wire up any new concept files.
4. **vault-xlog** records every session so the trail of what was taught — and where the learner
   is right now — persists across sessions. Every other skill logs into it, so run it whenever any
   of the other three skills runs.

The Comfort Index is the spine: the course builder seeds it, the professor updates it, the xLog
records the journey, and vault-linking keeps the whole graph connected so it all stays reachable.
