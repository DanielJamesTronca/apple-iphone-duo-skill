#!/usr/bin/env python3
"""Validate skill discoverability, packaging, and portable local references."""
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def validate():
    errors = []
    skill_roots = sorted((ROOT / "skills").glob("*/SKILL.md"))
    if not skill_roots:
        errors.append("No discoverable skills/*/SKILL.md")
    for entry in skill_roots:
        text = entry.read_text()
        front = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        if not front:
            errors.append(f"{entry.relative_to(ROOT)}: missing frontmatter")
            continue
        fields = dict(re.findall(r"^([a-z-]+):\s*(.+)$", front[1], re.M))
        if fields.get("name") != entry.parent.name or not re.fullmatch(r"[a-z0-9-]{1,63}", fields.get("name", "")):
            errors.append(f"{entry.relative_to(ROOT)}: skill name must match directory")
        if not fields.get("description"):
            errors.append(f"{entry.relative_to(ROOT)}: missing discovery description")
        metadata = entry.parent / "agents/openai.yaml"
        if not metadata.is_file():
            errors.append(f"{metadata.relative_to(ROOT)}: missing UI metadata")
        else:
            prompt = re.search(r'^\s*default_prompt:\s*"(.*)"$', metadata.read_text(), re.M)
            if not prompt or "$" + entry.parent.name not in prompt[1]:
                errors.append(f"{metadata.relative_to(ROOT)}: prompt must invoke skill")

    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        # Balanced one-level parentheses cover Swift API links as well as ordinary paths.
        links = re.findall(r"\[[^\]]*\]\((<[^>]+>|(?:[^()\s]|\([^()]*\))+)\)", path.read_text())
        for target in links:
            target = target.strip("<>")
            if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                continue
            local = unquote(target.split("#")[0])
            if not (path.parent / local).is_file():
                errors.append(f"{path.relative_to(ROOT)}: missing linked file {local}")

    try:
        codex = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        claude = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        if not (ROOT / codex["skills"]).is_dir():
            errors.append("Codex manifest skills path does not exist")
        if codex["name"] != claude["name"] or codex["version"] != claude["version"]:
            errors.append("Codex and Claude manifests disagree")
        matches = [p for p in market["plugins"] if p["name"] == claude["name"]]
        if len(matches) != 1 or matches[0]["version"] != claude["version"] or matches[0]["source"] != ".":
            errors.append("Claude marketplace cannot resolve the local plugin")
        for path in ROOT.rglob("*.json"):
            if ".git" not in path.parts:
                json.loads(path.read_text())
    except (OSError, KeyError, ValueError) as error:
        errors.append(f"Invalid package metadata: {error}")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise SystemExit(1)
    print("Skill metadata, plugin packaging, JSON, and local reference links are valid.")
