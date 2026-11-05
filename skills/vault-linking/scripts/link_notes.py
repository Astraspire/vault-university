#!/usr/bin/env python3
"""
link_notes.py — tag + link every markdown file in an Obsidian "second brain" vault.

Two jobs, both fully generic (any course, any vault, any person — nothing about a
specific course is hard-coded):

  1. TAG every file.
     - Structural tags come from the folder path:
           courses/{CODE}/module-N/{type}/...   ->   [code, module-N, type]
       (the code, module and type are READ from the folder names. No course code is
        baked in, so the same script works for any vault.)
     - Content tags come from the note's ACTUAL CONTENT. The script first scans the
       whole vault to build a vocabulary of every tag already in use, then for each
       note matches that vocabulary against the words in the note. A tag is applied
       when its words show up in the note's text. So a note is tagged with exactly the
       concepts that vault already uses for those topics — nothing invented, nothing
       course-specific.
     - Files with no front matter at all (xlog logs, people, profiles) get a minimal
       block with a `type:` and `tags:`.

  2. LINK every file so nothing is orphaned:
     - lessons get a link to their module overview and to their matching problem.
     - every bare-title [[Link]] in the vault is resolved to [[path|Link]] when it
       points to exactly one real file.

Run:
    python3 link_notes.py <VAULT_ROOT> --dry-run   # report only, no writes
    python3 link_notes.py <VAULT_ROOT>             # apply changes
    python3 link_notes.py --dry-run                # auto-discover root from CWD

Idempotent: running it again changes nothing.
"""
import os
import re
import sys
from math import ceil

DRY = False

COURSE_TYPES = ("lessons", "notes", "problems", "assignments", "other", "references")

BARE_LINK = re.compile(r"\[\[([^\|\]\n]+?)\]\]")
FRONT_MATTER = re.compile(r"^\s*---\s*\n(.*?)\n---\s*(\n|$)", re.S)


# --------------------------------------------------------------------------- #
# Vault discovery
# --------------------------------------------------------------------------- #
def find_vault_root(explicit=None, start=None):
    signals = ("courses", "xlog", "profiles", "concepts")
    candidates = [explicit] if explicit else []
    d = os.path.abspath(start or os.getcwd())
    while True:
        if any(os.path.isdir(os.path.join(d, s)) for s in signals):
            candidates.append(d)
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    for c in candidates:
        if any(os.path.isdir(os.path.join(c, s)) for s in signals):
            return c
    return None


def iter_md_files(root, subdir=None, skip=("_templates",)):
    base = os.path.join(root, subdir) if subdir else root
    if not os.path.isdir(base):
        return
    for dirpath, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in skip and not d.startswith(".")]
        for fn in files:
            if fn.lower().endswith(".md"):
                rel = os.path.relpath(os.path.join(dirpath, fn), root).replace(os.sep, "/")
                yield rel


# --------------------------------------------------------------------------- #
# Classification — pure path logic, generic (no course codes baked in)
# --------------------------------------------------------------------------- #
def classify(relpath):
    """Return (kind, course, module, ftype) from the folder path only."""
    parts = relpath.split("/")
    head = parts[0]
    if head == "courses":
        course = parts[1] if len(parts) > 1 else None
        module = ftype = None
        for p in parts[2:]:
            if module is None and re.match(r"module-?\d+", p, re.I):
                module = p
            elif ftype is None and p.lower() in COURSE_TYPES:
                ftype = p.lower()
        return "course", course, module, ftype
    if head == "xlog":
        return "xlog", None, None, None
    if head == "profiles":
        if len(parts) >= 2 and parts[1] == "related-people":
            return "person", None, None, None
        if len(parts) >= 2 and parts[1] == "user":
            if "comfort-levels" in parts:
                return "comfort", None, None, None
            return "user_profile", None, None, None
    if head.lower().endswith("concept") or head.lower() == "concepts":
        return "concept", None, None, None
    return "root_note", None, None, None


def structural_tags(relpath, kind, course, module, ftype):
    """Path-derived tags: [code, module-N, type] for course files, else area tags."""
    if kind == "course":
        code = (course or "").lower()
        mod = re.sub(r"^module-?", "", module) if module else None
        tags = [t for t in (code, module, ftype) if t]
        return tags
    # non-course areas
    parts = relpath.split("/")
    if kind == "concept":
        return ["concept", parts[1]] if len(parts) >= 3 else ["concept"]
    if kind == "xlog":
        return ["xlog"]
    if kind == "person":
        return ["person", "related-people"]
    if kind == "user_profile":
        return ["profile", "user"]
    if kind == "comfort":
        return ["comfort", "comfort-registry", "user-variables"]
    return ["note"]


# --------------------------------------------------------------------------- #
# Content vocabulary — every tag already used anywhere in the vault
# --------------------------------------------------------------------------- #
def parse_tags(value):
    r"""Extract tag names from a YAML tags value.

    Accepts the two forms the vault actually uses:
        tags: ["a", "b", "c"]        (quoted, comma or space separated)
        tags: [a, b, c]               (bare identifiers, comma separated)

    Only well-formed tokens are returned. We deliberately do NOT fall back to a
    catch-all \S+ match: doing so (as it used to) slurps in the surrounding
    brackets, commas and stray quotes as if they were tags, which is exactly the
    corruption that produced mangled tags and empty tokens."""
    quoted = re.findall(r'"([^"]+)"|\'([^\']+)\'', value)
    if quoted:
        return [t[0] or t[1] for t in quoted if any(t)]
    backtick = re.findall(r"`([^`]+)`", value)
    if backtick:
        return backtick
    bare = re.findall(r"\[([^\]]*)\]", value)
    if bare:
        out = []
        for piece in bare[0].split(","):
            piece = piece.strip()
            if piece:
                out.append(piece)
        return out
    return []


def build_vocabulary(root):
    """Scan the vault once and return everything content matching needs:

        vocab          tag -> file count across the whole vault (for reporting)
        course_tags    course-lower -> set of content tags used by that course
        other_tags     set of content tags used only by non-course files
                        (concepts, xlog, profiles, root notes) — these are
                        course-agnostic and safe to attach to any note.

    Structural tags (code/module/type) are excluded so content matching only
    pairs a note with real topic tags.

    The per-course split is what keeps a note from picking up another course's
    topic tags: a lesson is only ever matched against its own course's tag set
    (plus the course-agnostic ones), so it can never end up tagged with another
    course's concepts just because a shared word showed up in the body."""
    vocab = {}
    course_tags = {}
    other_tags = set()
    for rel in iter_md_files(root):
        try:
            text = read(root, rel)
        except OSError:
            continue
        kind, course, module, ftype = classify(rel)
        fm, body, d = parse_frontmatter(text)
        tags = parse_tags(d.get("tags", ""))
        for t in tags:
            low = t.lower()
            if low in STRUCTURAL_TAGS:
                continue
            vocab[low] = vocab.get(low, 0) + 1
            if kind == "course" and course:
                course_tags.setdefault(course.lower(), set()).add(low)
            else:
                other_tags.add(low)
    return vocab, course_tags, other_tags


STRUCTURAL_TAGS = {"course", "module", "type", "lesson", "notes", "note", "problem",
                   "problems", "assignment", "assignments", "other", "reference",
                   "references", "index", "concept", "xlog", "person", "profile",
                   "comfort", "comfort-registry", "user-variables", "root_note"}


# --------------------------------------------------------------------------- #
# Content matching — does a vault tag apply to this note's words?
# --------------------------------------------------------------------------- #
def content_signal(text):
    """The words a note is 'about': the topics line (author-chosen keywords) plus
    the body text, but not the structural front-matter keys."""
    fm, body, d = parse_frontmatter(text)
    words = []
    if "topics" in d:
        words.append(parse_tags(d["topics"]))
    words.append(re.findall(r"[a-zA-Z0-9]+", body.lower()))
    flat = []
    for w in words:
        flat.extend(w)
    return flat


def matches_tag(note_words, tag):
    """A tag matches when its words actually appear in the note.
    Single-word tag: the word must appear. Multi-word (hyphenated) tag: the full
    hyphenated phrase appears, OR a majority of its words appear. This keeps the
    pairing honest — we never attach a topic the note doesn't contain."""
    tag_words = tag.split("-")
    wordset = set(note_words)
    hits = sum(1 for w in tag_words if w in wordset)
    if len(tag_words) == 1:
        return hits >= 1
    # Multi-word tag: require the EXACT phrase, OR every component word present.
    # Requiring all words (not just a majority) stops a shared generic word
    # ("audio", "event", "system") from dragging an unrelated concept tag onto
    # a note that only mentions one of them.
    if tag in " ".join(note_words):
        return True
    return hits >= len(tag_words)


# --------------------------------------------------------------------------- #
# File IO helpers
# --------------------------------------------------------------------------- #
def read(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as f:
        return f.read()


def write(root, rel, content):
    with open(os.path.join(root, rel), "w", encoding="utf-8") as f:
        f.write(content)


def exists(root, rel):
    return os.path.exists(os.path.join(root, rel))


# --------------------------------------------------------------------------- #
# Front matter
# --------------------------------------------------------------------------- #
def parse_frontmatter(text):
    text = text.replace("\r\n", "\n")
    m = FRONT_MATTER.match(text)
    if not m:
        return None, text, {}
    fm = m.group(1)
    body = text[m.end():]
    d = {}
    for line in fm.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        d[k.strip()] = v.strip()
    return fm, body, d


def tag_style(value):
    return "comma" if "," in value else "space"


def format_tags(tags, style):
    if style == "comma":
        return "[" + ", ".join('"%s"' % t for t in tags) + "]"
    return "[" + " ".join(tags) + "]"


def clean_tags(value):
    """Return a clean list of tags when value is in a standard, merge-safe
    format (all-quoted, or bare comma-separated). Return None when the line is
    in an unusual or mixed format (backticks, space-separated, etc.) that we
    must preserve verbatim so we never corrupt it."""
    v = value.strip()
    if "`" in v:
        return None
    if '"' in v or "'" in v:
        toks = [a or b for a, b in re.findall(r'"([^"]+)"|\'([^\']+)\'', value)]
        return toks if toks else None
    bare = re.findall(r"\[([^\]]*)\]", v)
    if bare and "," in bare[0]:
        toks = [p.strip() for p in bare[0].split(",") if p.strip()]
        return toks if toks else None
    return None


def set_tags_line(fm_text, tags):
    m = re.search(r"^tags\s*:\s*(.+?)\s*$", fm_text, re.M)
    if m:
        existing = clean_tags(m.group(1)) or []
        combined = list(dict.fromkeys(existing + tags))
        style = tag_style(m.group(1))
        return re.sub(r"^tags\s*:.*$", "tags: " + format_tags(combined, style),
                      fm_text, count=1, flags=re.M)
    return re.sub(r"^([^\n]+)$", r"\1\ntags: " + format_tags(tags, "comma"),
                  fm_text, count=1, flags=re.M)


def build_frontmatter(kind, tags, date=None, ftype=None):
    lines = ["---"]
    if kind == "xlog" and date:
        lines.append("date: %s" % date)
    if kind == "course" and ftype:
        lines.append("type: %s" % ftype)
    else:
        type_map = {"xlog": "xlog", "person": "person", "user_profile": "profile",
                    "comfort": "comfort-registry", "concept": "concept",
                    "root_note": "note"}
        lines.append("type: %s" % type_map.get(kind, "note"))
    lines.append("tags: " + format_tags(tags, "comma"))
    lines.append("---")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Links
# --------------------------------------------------------------------------- #
def has_link_path(text, target_rel):
    """Idempotency guard: is this file already linked to target_rel?
    The writer emits path-style links ([[path|Label]]), so we must match those
    too — a bare-title check alone silently misses them and duplicates the link."""
    if re.search(r"\[\[" + re.escape(target_rel) + r"(?:\|[^]]*)?\]\]", text):
        return True
    base = os.path.basename(target_rel).replace(".md", "")
    return bool(re.search(r"\[\[" + re.escape(base) + r"(?:\|[^]]*)?\]\]", text))


def basename_map(root):
    m = {}
    for rel in iter_md_files(root):
        key = re.sub(r"[^a-z0-9]", "", os.path.splitext(os.path.basename(rel))[0].lower())
        if key and key not in m:
            m[key] = rel
    return m


def module_overview(root, course, module):
    if module is None:
        return None
    keywords = ["overview", "module-index", "course-index", "index", "summary", "guide", "syllabus"]
    prefix = "courses/%s/%s/" % (course, module)
    best = None
    for rel in iter_md_files(root):
        if not rel.lower().startswith(prefix):
            continue
        rank = sum(k in os.path.basename(rel).lower() for k in keywords)
        if rank > 0:
            if best is None or rank > best[0] or (rank == best[0] and rel < best[1]):
                best = (rank, rel)
    if best:
        return best[1]
    notes_dir = os.path.join(root, "courses", course, module, "notes")
    if os.path.isdir(notes_dir):
        for fn in sorted(os.listdir(notes_dir)):
            if fn.lower().endswith(".md"):
                return "courses/%s/%s/notes/%s" % (course, module, fn)
    mod_dir = os.path.join(root, "courses", course, module)
    if os.path.isdir(mod_dir):
        for fn in sorted(os.listdir(mod_dir)):
            if fn.lower().endswith(".md"):
                return "courses/%s/%s/%s" % (course, module, fn)
    return None


def matching_problem(root, course, module, lesson_base):
    if module is None:
        return None
    num = re.search(r"\d+", lesson_base)
    if not num:
        return None
    prob_dir = os.path.join(root, "courses", course, module, "problems")
    if not os.path.isdir(prob_dir):
        return None
    for fn in sorted(os.listdir(prob_dir)):
        if fn.lower().endswith(".md") and re.search(r"\d+", os.path.splitext(fn)[0]).group() == num.group():
            return "courses/%s/%s/problems/%s" % (course, module, fn)
    return None


def lesson_number(base):
    m = re.search(r"\d+", base)
    return m.group() if m else None


# --------------------------------------------------------------------------- #
# Per-file processing
# --------------------------------------------------------------------------- #
def process(root, rel, course, module, ftype, bmap, vocab, course_tags, other_tags):
    try:
        text = read(root, rel)
    except OSError:
        return None
    fm, body, d = parse_frontmatter(text)
    kind = classify(rel)[0]
    changed = {"path": rel, "tags_added": False, "links_added": 0, "links": [], "fm_fixed": False}

    # ---- TAGS ----------------------------------------------------------- #
    # structural (path) tags, always correct
    struct = structural_tags(rel, kind, course, module, ftype)

    # content tags (topic match against the vault's own vocabulary).
    # A course note matches only against ITS OWN course's tag set plus the
    # course-agnostic concept tags (concepts/, xlog, profiles). This prevents
    # a note from picking up another course's topic tags.
    if kind in ("xlog", "person", "comfort"):
        content_tags = []
    else:
        if kind == "course" and course:
            pool = set(course_tags.get(course.lower(), set())) | other_tags
        else:
            pool = other_tags
        note_words = content_signal(text)
        content_tags = [t for t in sorted(pool) if matches_tag(note_words, t)]

    if fm is None:
        # no front matter at all -> build a minimal block
        if kind == "xlog":
            m = re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(rel))
            date = m.group(1) if m else None
            tags = ["xlog"]
        else:
            date = None
            tags = struct + content_tags
        new_fm = build_frontmatter(kind, tags, date, ftype)
        body = new_fm + "\n---\n\n" + body.lstrip("\n")
        changed["tags_added"] = True
        changed["fm_fixed"] = True
    else:
        # Only merge into a tags line we can parse cleanly. Lines in an
        # unusual format (backticks, space-separated, mixed) are left untouched
        # so we never corrupt them by appending onto them.
        mergeable = clean_tags(d.get("tags", ""))
        if mergeable is not None:
            existing = {t.lower() for t in mergeable}
            new_tags = [t for t in (struct + content_tags) if t.lower() not in existing]
            if new_tags:
                fm = set_tags_line(fm, new_tags)
                changed["tags_added"] = True

    # ---- LINKS ---------------------------------------------------------- #
    if kind == "course":
        target = module_overview(root, course, module)
        if target and target != rel and exists(root, target) and not has_link_path(body, target):
            name = os.path.basename(target).replace(".md", "").replace("_", " ").strip()
            body = "[[%s|%s]]\n\n%s" % (target, name, body.lstrip("\n"))
            changed["links"].append("[[%s|%s]]" % (target, name))
            changed["links_added"] += 1
        if ftype == "lesson" and module:
            base = os.path.basename(rel).replace(".md", "")
            prob = matching_problem(root, course, module, base)
            if prob and exists(root, prob) and not has_link_path(body, prob):
                name = os.path.basename(prob).replace(".md", "")
                body = "[[%s|%s]]\n\n%s" % (prob, name, body.lstrip("\n"))
                changed["links"].append("[[%s|%s]]" % (prob, name))
                changed["links_added"] += 1

    # resolve dangling bare-title links anywhere in this file
    n_dangling = 0

    def resolve_title(m):
        nonlocal n_dangling
        title = m.group(1).strip()
        if "/" in title:
            return m.group(0)
        dest = bmap.get(re.sub(r"[^a-z0-9]", "", title.lower()))
        if dest and dest != rel:
            n_dangling += 1
            return "[[%s|%s]]" % (dest, title)
        return m.group(0)

    new_body = BARE_LINK.sub(resolve_title, body)
    if n_dangling:
        changed["links_added"] += n_dangling
        for m in BARE_LINK.finditer(new_body):
            title = m.group(1).strip()
            if "/" not in title:
                changed["links"].append("resolved: %s" % title)

    changed["new_text"] = ("---\n" + fm + "\n---\n" + new_body) if fm is not None else new_body
    return changed


def main():
    global DRY
    args = sys.argv[1:]
    DRY = "--dry-run" in args
    positional = [a for a in args if not a.startswith("-")]
    root = find_vault_root(explicit=positional[0] if positional else None)
    if not root:
        print("Could not find a vault root (no 'courses/'/'xlog/'/'profiles/'/'concepts/'). "
              "Pass the path explicitly.", file=sys.stderr)
        sys.exit(1)

    print("Vault root: %s\n" % root)
    bmap = basename_map(root)
    vocab, course_tags, other_tags = build_vocabulary(root)
    print("Content vocabulary: %d tags across the vault\n" % len(vocab))

    results = []
    for rel in sorted(iter_md_files(root)):
        kind, course, module, ftype = classify(rel)
        res = process(root, rel, course, module, ftype, bmap, vocab, course_tags, other_tags)
        if res:
            results.append(res)

    n_tags = sum(1 for r in results if r["tags_added"])
    n_links = sum(r["links_added"] for r in results)
    print("Files processed: %d" % len(results))
    print("Files newly tagged: %d" % n_tags)
    print("Links added/resolved: %d" % n_links)
    print()
    for r in sorted(results, key=lambda x: x["path"]):
        if not (r["tags_added"] or r["links_added"] or r["fm_fixed"]):
            continue
        print("  %s" % r["path"])
        if r["tags_added"]:
            print("    + tags" + (" (+ front-matter block)" if r["fm_fixed"] else ""))
        for l in r["links"]:
            print("    + link: %s" % l)

    if not DRY:
        for r in results:
            if r["tags_added"] or r["links_added"] or r["fm_fixed"]:
                write(root, r["path"], r["new_text"])
        print("\n[%s] Done." % ("DRY-RUN" if DRY else "APPLIED"))


if __name__ == "__main__":
    main()
