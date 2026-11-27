#!/usr/bin/env python3
"""Sync the labels in .github/labels.yml into every redox-rpi repository.

Usage: scripts/sync-labels.py [--apply] [repo ...]

Without --apply it only prints what it would change. With --apply it
creates missing labels and updates color and description of existing
ones. It never deletes a label; labels that are not in the list are
printed as "extra" so they can be added to the list or removed by hand.
Needs the GitHub CLI (gh) with a token that can write labels.
"""
import json, re, subprocess, sys, pathlib

ORG = "redox-rpi"
LIST = pathlib.Path(__file__).resolve().parent.parent / ".github" / "labels.yml"
ITEM = re.compile(r'^\s*-\s*\{name:\s*"([^"]+)",\s*color:\s*"?([0-9A-Fa-f]{6})"?,\s*description:\s*"([^"]*)"\}\s*$')

def parse():
    shared, topics, repos, section, repo = [], [], {}, None, None
    for line in LIST.read_text().splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if re.match(r"^\w+:\s*$", line):
            section, repo = line.split(":")[0], None
            continue
        m = re.match(r"^  ([\w.-]+):\s*$", line)
        if m and section == "repos":
            repo = m.group(1); repos[repo] = []
            continue
        m = ITEM.match(line)
        if m:
            item = {"name": m.group(1), "color": m.group(2).lower(), "description": m.group(3)}
            {"shared": shared, "topics": topics}.get(section, repos.get(repo, [])).append(item)
            continue
        if line.strip() == "- topics" and repo:
            repos[repo].append("topics")
            continue
        sys.exit(f"cannot parse: {line}")
    return shared, topics, repos

def gh(*args):
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout

def wanted(repo, shared, topics, repos):
    out = list(shared)
    for x in repos.get(repo, []):
        out += topics if x == "topics" else [x]
    return out

def main():
    apply = "--apply" in sys.argv
    names = [a for a in sys.argv[1:] if not a.startswith("--")]
    shared, topics, repos = parse()
    if not names:
        names = json.loads(gh("repo", "list", ORG, "-L", "200", "--no-archived", "--json", "name"))
        names = [r["name"] for r in names]
    for repo in sorted(names):
        have = {l["name"]: l for l in json.loads(gh("label", "list", "-R", f"{ORG}/{repo}", "-L", "500", "--json", "name,color,description"))}
        want = wanted(repo, shared, topics, repos)
        for w in want:
            h = have.get(w["name"])
            if h is None:
                action = "create"
            elif h["color"].lower() != w["color"] or (h["description"] or "") != w["description"]:
                action = "update"
            else:
                continue
            print(f"{repo}: {action} {w['name']}")
            if apply:
                gh("label", "create", w["name"], "-R", f"{ORG}/{repo}", "--color", w["color"], "--description", w["description"], "--force")
        for name in sorted(set(have) - {w["name"] for w in want}):
            print(f"{repo}: extra {name}")

if __name__ == "__main__":
    main()
