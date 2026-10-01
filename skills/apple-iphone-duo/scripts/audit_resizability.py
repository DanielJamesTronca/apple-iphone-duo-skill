#!/usr/bin/env python3
"""Read-only lexical candidates for a contextual iPhone resizability review."""
import argparse
import bisect
import json
import os
from pathlib import Path
import re

SUFFIXES = {".swift", ".m", ".mm", ".h", ".plist", ".pbxproj", ".xcconfig", ".xcproj"}
CODE_SUFFIXES = {".swift", ".m", ".mm", ".h"}
SKIP_DIRS = {".git", ".build", ".swiftpm", "DerivedData", "Pods", "Carthage", "node_modules", "build"}
RULES = (
    ("main-screen", r"\bUIScreen\s*\.\s*(?:main|mainScreen)\b|\[\s*UIScreen\s+mainScreen\s*\]",
     "Use local bounds/traits, or the owning scene's screen for genuine display information."),
    ("global-window", r"\bconnectedScenes\s*\.\s*first\b|\bkeyWindow\b|UIApplication\s*\.\s*shared\s*\.\s*windows\b",
     "Resolve the action's owning view/window/scene; do not choose a process-wide first window."),
    ("idiom-assumption", r"\b(?:userInterfaceIdiom|IS_PAD|isPad|isiPad)\b",
     "Inspect intent: layout uses local size classes; assets/analytics/platform policies can keep idiom."),
    ("orientation-assumption", r"\b(?:interfaceOrientation|isLandscape|isPortrait)\b|UIDevice\s*\.\s*current\s*\.\s*orientation\b",
     "Layout needs local traits/bounds; keep physical orientation where sensor or product policy needs it."),
    ("edge-inset", r"\bsafeAreaInsets\s*\.\s*(?:left|right|top|bottom)\b",
     "Check all edges independently, freshness, coordinate space, and double-counted scroll adjustment."),
    ("safe-area-bypass", r"\.\s*ignoresSafeArea\s*\(|\.\s*edgesIgnoringSafeArea\s*\(",
     "Inspect the receiving subtree: foreground controls must remain reachable around obstructions."),
    ("layout-identity", r"\.\s*id\s*\(\s*(?:horizontalSizeClass|verticalSizeClass|hingeAngle|orientation)\b",
     "Changing identity during resize can discard navigation, draft, playback, and scroll state."),
    ("application-ui-lifecycle", r"\b(?:applicationWillEnterForeground|applicationDidEnterBackground|applicationDidBecomeActive|applicationWillResignActive)\b",
     "Move scene-owned UI work to scene callbacks; preserve process-wide services and cold/warm routing."),
    ("full-screen-policy", r"\bUIRequiresFullScreen(?:IgnoredStartingWithVersion)?\b",
     "Inspect resolved configuration: iOS 27 supports discrete resizing, not immutable full-screen bounds."),
)
COMPILED = tuple((name, re.compile(pattern), guidance) for name, pattern, guidance in RULES)


def mask_non_code(source):
    """Mask comments and strings while retaining offsets/lines, including nested Swift comments."""
    result = list(source)
    i = 0
    n = len(source)
    while i < n:
        start = i
        if source.startswith("//", i):
            end = source.find("\n", i)
            i = n if end < 0 else end
        elif source.startswith("/*", i):
            depth = 1
            i += 2
            while i < n and depth:
                if source.startswith("/*", i):
                    depth += 1
                    i += 2
                elif source.startswith("*/", i):
                    depth -= 1
                    i += 2
                else:
                    i += 1
        elif source.startswith('"""', i):
            end = source.find('"""', i + 3)
            i = n if end < 0 else end + 3
        elif source[i] in ('"', "'"):
            quote = source[i]
            i += 1
            while i < n:
                if source[i] == "\\":
                    i += 2
                elif source[i] == quote:
                    i += 1
                    break
                else:
                    i += 1
        else:
            i += 1
            continue
        for position in range(start, min(i, n)):
            if result[position] != "\n":
                result[position] = " "
    return "".join(result)


def files_under(root, warnings):
    if root.is_file():
        return [root] if root.suffix in SUFFIXES else []
    paths = []

    def report_error(error):
        warnings.append(str(error))

    for directory, dirs, files in os.walk(root, followlinks=False, onerror=report_error):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not (Path(directory) / d).is_symlink())
        for name in sorted(files):
            path = Path(directory) / name
            if path.suffix in SUFFIXES and not path.is_symlink():
                paths.append(path)
    return sorted(paths)


def audit(root):
    warnings = []
    candidates = []
    scanned = 0
    base = root if root.is_dir() else root.parent
    for path in files_under(root, warnings):
        try:
            source = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            warnings.append(f"{path.relative_to(base)}: {error}")
            continue
        scanned += 1
        if path.suffix in CODE_SUFFIXES:
            searchable = mask_non_code(source)
        else:
            # Preserve quoted plist/project keys; remove XML and C-style comments.
            searchable = re.sub(r"<!--[\s\S]*?-->|/\*[\s\S]*?\*/|//[^\n]*",
                                lambda m: "".join("\n" if c == "\n" else " " for c in m[0]), source)
        starts = [0] + [m.end() for m in re.finditer("\n", source)]
        lines = source.splitlines()
        seen = set()
        for rule, pattern, guidance in COMPILED:
            for match in pattern.finditer(searchable):
                line = bisect.bisect_right(starts, match.start())
                if (rule, line) in seen:
                    continue
                seen.add((rule, line))
                candidates.append({"rule": rule, "path": path.relative_to(base).as_posix(),
                                   "line": line, "excerpt": lines[line - 1].strip(),
                                   "guidance": guidance})
    candidates.sort(key=lambda item: (item["path"], item["line"], item["rule"]))
    return {"files_scanned": scanned, "candidates": candidates, "warnings": warnings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Project directory or one source/config file")
    parser.add_argument("--json", action="store_true", help="Emit a JSON report")
    args = parser.parse_args()
    if not args.path.exists():
        parser.error(f"Path does not exist: {args.path}")
    report = audit(args.path.absolute())
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"{report['files_scanned']} files scanned; {len(report['candidates'])} review candidates (not proven bugs).")
        for item in report["candidates"]:
            print(f"{item['path']}:{item['line']}: [{item['rule']}] {item['excerpt']}")
            print(f"  {item['guidance']}")
        for warning in report["warnings"]:
            print(f"Warning: {warning}")
    return 1 if report["warnings"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
