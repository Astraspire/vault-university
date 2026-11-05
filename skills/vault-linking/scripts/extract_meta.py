#!/usr/bin/env python3
"""
extract_meta.py — Index every markdown file in an Obsidian "second brain" vault.

Generic / course-agnostic. Scans ALL areas of the vault (courses, concepts, xlog,
profiles, root notes), extracts front matter + first heading + a short body preview,
and prints a compact per-area summary. By default it only prints — it writes a JSON
index only when you pass --write <path>, so it never drops an artifact into the vault.

Run:
    python3 extract_meta.py <VAULT_ROOT>            # print summary only (default)
    python3 extract_meta.py <VAULT_ROOT> --write meta.json   # also write JSON to <path>
    python3 extract_meta.py --dry-run               # print summary only, no file write
"""
import os
import re
import sys
import json


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
                yield os.path.relpath(os.path.join(dirpath, fn), root).replace(os.sep, "/")


def parse_frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    fm = {}
    if not m:
        return fm, text
    body = text[m.end():]
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, body


def first_heading(body):
    m = re.search(r"^#\s+(.+)$", body, re.M)
    return m.group(1).strip() if m else ""


def preview(body, n=200):
    b = body.replace("\f", " ").strip()
    return re.sub(r"\s+", " ", b)[:n].strip()


def main():
    args = sys.argv[1:]
    dry = "--dry-run" in args
    write_to = None
    positional = []
    for a in args:
        if a == "--write":
            write_to = "STDERR"  # placeholder; next positional is the path
        elif a.startswith("--write="):
            write_to = a.split("=", 1)[1]
        elif not a.startswith("-"):
            positional.append(a)
    if write_to == "STDERR" and positional:
        write_to = positional.pop()

    root = find_vault_root(explicit=positional[0] if positional else None)
    if not root:
        print("Could not find a vault root (no 'courses/'/'xlog/'/'profiles/'/'concepts/'). "
              "Pass the path explicitly.", file=sys.stderr)
        sys.exit(1)

    out = {"vault": root, "areas": {}}
    for area in ("courses", "concepts", "xlog", "profiles", "root"):
        out["areas"][area] = []

    for rel in sorted(iter_md_files(root)):
        try:
            with open(os.path.join(root, rel), encoding="utf-8") as f:
                text = f.read()
        except OSError as e:
            continue
        fm, body = parse_frontmatter(text)
        rec = {
            "path": rel,
            "type": fm.get("type", ""),
            "tags": fm.get("tags", ""),
            "heading": first_heading(body),
            "preview": preview(body),
        }
        parts = rel.split("/")
        head = parts[0]
        if head == "courses":
            out["areas"]["courses"].append(rec)
        elif head.lower().endswith("concept") or head == "concepts":
            out["areas"]["concepts"].append(rec)
        elif head == "xlog":
            out["areas"]["xlog"].append(rec)
        elif head == "profiles":
            out["areas"]["profiles"].append(rec)
        else:
            out["areas"]["root"].append(rec)

    if write_to:
        with open(os.path.join(root, write_to), "w") as f:
            json.dump(out, f, indent=2)

    for area in ("courses", "concepts", "xlog", "profiles", "root"):
        rows = out["areas"][area]
        print("===== %s (%d files) =====" % (area, len(rows)))
        for r in rows:
            print("   [%s] %s  ::  %s" % (r["type"] or "-", r["path"], r["heading"][:60]))
        print()
    total = sum(len(v) for v in out["areas"].values())
    print("[OK] %d files across %d areas." % (total, len(out["areas"])))
    if write_to:
        print("[OK] Wrote %s" % os.path.join(root, write_to))


if __name__ == "__main__":
    main()
