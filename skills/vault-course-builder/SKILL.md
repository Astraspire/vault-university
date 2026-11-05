---
name: vault-course-builder
description: "Build complete course content for the vault from any reference material — lessons, problem sets, assignments, and module indexes — into the indexed, tagged vault course directory structure. Use when the user wants to build, generate, or expand course content (lessons, problem sets, assignments, module indexes) from source materials (textbooks, slides, PDFs, syllabi, notes, course materials). Generic: any subject, any level, any learner, any time frame."

metadata:
  author: Danny Fetter
  version: "1.0.0"
---
# Vault Course Builder

## Purpose

Turn reference material about a set of topics — plus a time frame — into a set of lessons and/or
problems that bridge what the learner already knows to what they need to learn. Output is course
content stored in the vault's indexed + tagged course directory, cross-linked and comfort-tagged,
ready for a later teaching skill to use.

This is generic: **any subject, any level, any learner, any school, any time frame.**

## Step 0 — Clarify Scope & Time Frame

Before building, confirm the scope. Ask only if the user hasn't specified it:

- **Time frame:** How long should this course take? (a week, a term, a month, self-paced)
- **Scope:** Which topics / modules, and in what order?
- **Source material:** What reference material am I working from?
- **Learner level:** Introductory, intermediate, advanced?

## Step 1 — Read & Understand the Source

- Read the reference material thoroughly.
- Identify the distinct topics, in the order they should be taught.
- Note the key concepts, worked examples, and problems already in the material.

## Step 2 — Check the Comfort Index

Read `VAULT_ROOT/profiles/user/comfort-levels/00-Comfort-Index.md` (create it if missing).

- This is a **real-time map of everything the learner knows and how comfortably** — across all
  conversations and all topics, not just this course.
- Find topics the learner already knows at high comfort — these are the anchors to bridge new
  concepts from.
- Set every NEW topic in this course to `planned`.
- Only promote comfort tiers when the learner actually studies the topic.

## Step 3 — Create the Directory Structure

Follow the vault course structure. See `references/01-vault-design.md` for the layout.

## Step 4 — Write the Course Index

Create `VAULT_ROOT/courses/{COURSE-CODE}/COURSE-INDEX.md`. See `references/08-course-index-template.md`.

## Step 5 — Write the Lesson Plan

Write `VAULT_ROOT/courses/{COURSE-CODE}/module-{N}/lessons/lesson_plan.md` FIRST. It maps each
source section to its lesson and problem numbers; everything else hangs from it. See
`references/04-lesson-plan-template.md`.

## Step 6 — Write Lessons

Create one file per lesson in `VAULT_ROOT/courses/{COURSE-CODE}/module-{N}/lessons/`. See
`references/05-lesson-template.md`.

- Teach each concept fully first, then layer in "why it matters."
- Bridge new concepts to topics the learner already knows at high comfort.
- Cross-link lessons with wikilinks (prior / next).
- Match the front-matter style of the course you are working in.

## Step 7 — Write Problems

Create one file per problem in `VAULT_ROOT/courses/{COURSE-CODE}/module-{N}/problems/`. See
`references/06-problem-template.md`.

- Write problems AFTER lessons — problems test what lessons teach.
- Always link back to the lesson it tests.

## Step 8 — Write Assignments (if applicable)

Create assignments / projects / labs in `VAULT_ROOT/courses/{COURSE-CODE}/module-{N}/assignments/`
or `project-<N>.md`. See `references/07-assignment-template.md`.

## Step 9 — Update Comfort Levels

- Add new topics to the comfort index at `planned`.
- Only promote topics as completed after the learner studies them, then update the index.

## Step 10 — Cross-Link Everything

- Every lesson links to prior / next lessons.
- Every problem links to the lesson it tests.
- Every assignment links to the lessons it draws on.
- The course index links to each module's first lesson.
- Use wikilinks for internal vault links.

## Step 11 — Wire the Course into the Whole Vault (vault-linking)

Run the `vault-linking` skill to tag and wire the newly built course into the ENTIRE vault — not
just the course files. It links the course index to the Comfort Index, connects the course to
related concepts and people, and resolves any dangling links the build introduced. This is **not
optional**: a course built without vault-linking is orphaned, and the professor cannot bridge to it
cleanly. See `vault-linking`.

## Step 12 — Log the Build

Append a session bullet to the day's xLog using the `vault-xlog` skill.

## Consuming the content

The lessons built here are what `vault-professor` teaches. Nothing surfaces the course to the
professor cleanly until vault-linking has run (Step 11) and the session is logged (Step 12).

## Output Format Rules

- **Front-matter:** `topics`, `tags`, `course`, `module`, `type`, `created`. Tags include the
  course code, `module-N`, and the type. Only include `learned` after the topic has actually been
  studied.
- **Wikilinks:** use `[[path|label]]` for internal vault links.
- **Callouts:** use `> [!tip]`, `> [!note]`, `> [!warning]` for highlights.
- **Math:** LaTeX only (`$...$` inline, `$$...$$` block) for all formulas.
- **Anchors:** bridge new concepts to what the learner already knows at high comfort.

## Teaching Devices

The goal is to bridge known concepts to new ones. Match the teaching device to the topic and the
learner — vary the device rather than forcing one. Options include analogy, worked example,
Socratic framing, and visual / diagram. Choose what best conveys this specific topic to this
specific learner.

## Constraints

- Stay within the vault's file conventions (Obsidian-flavored markdown).
- Keep front-matter consistent across the whole course.
- Build only from what the user provides.
- Only promote comfort tiers after the learner actually studies the topic.
