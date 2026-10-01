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
        name = fields.get("name", "")
        if (name != entry.parent.name or len(name) > 64
                or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)):
            errors.append(f"{entry.relative_to(ROOT)}: skill name must match directory")
        if not 1 <= len(fields.get("description", "")) <= 1024:
            errors.append(f"{entry.relative_to(ROOT)}: discovery description must contain 1–1024 characters")
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
            resolved = (path.parent / local).resolve()
            if not resolved.is_file():
                errors.append(f"{path.relative_to(ROOT)}: missing linked file {local}")
            for entry in skill_roots:
                skill_root = entry.parent.resolve()
                if path.resolve().is_relative_to(skill_root) and not resolved.is_relative_to(skill_root):
                    errors.append(f"{path.relative_to(ROOT)}: linked file {local} leaves the installed skill")

    try:
        portable = json.loads((ROOT / "plugin.json").read_text())
        codex = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        claude = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        if not (ROOT / codex["skills"]).is_dir():
            errors.append("Codex manifest skills path does not exist")
        if portable["$schema"] != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
            errors.append("Portable manifest must declare the Agent Plugins 1.0.0 schema")
        for field in ("name", "version"):
            if len({portable[field], codex[field], claude[field]}) != 1:
                errors.append(f"Portable, Codex, and Claude manifest {field} values disagree")
        overlay = portable.get("extensions", {}).get("com.openai")
        if overlay is not None and overlay.get("interface") != codex.get("interface"):
            errors.append("Portable and Codex compatibility presentation metadata disagree")
        matches = [p for p in market["plugins"] if p["name"] == claude["name"]]
        if len(matches) != 1 or matches[0]["version"] != claude["version"] or matches[0]["source"] != ".":
            errors.append("Claude marketplace cannot resolve the local plugin")
        native_market = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
        matches = [p for p in native_market["plugins"] if p["name"] == portable["name"]]
        if len(matches) != 1:
            errors.append("Codex marketplace must resolve the published plugin exactly once")
        else:
            plugin = matches[0]
            source = plugin.get("source", {})
            local = source.get("path", "")
            if (source.get("source") != "local" or not local.startswith("./")
                    or (ROOT / local).resolve() != ROOT):
                errors.append("Codex marketplace source must resolve to this plugin root")
            policy = plugin.get("policy", {})
            if (policy.get("installation") not in {"AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE"}
                    or policy.get("authentication") not in {"ON_INSTALL", "ON_USE"}
                    or not plugin.get("category")):
                errors.append("Codex marketplace must declare installation, authentication, and category")
        for path in ROOT.rglob("*.json"):
            if ".git" not in path.parts:
                json.loads(path.read_text())
    except (OSError, KeyError, ValueError, TypeError, AttributeError) as error:
        errors.append(f"Invalid package metadata: {error}")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise SystemExit(1)
    print("Skill metadata, plugin packaging, JSON, and local reference links are valid.")
