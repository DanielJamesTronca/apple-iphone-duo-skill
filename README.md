# Apple iPhone Duo Skill

An agent skill for preparing, implementing, and reviewing iPhone Duo apps with Apple's iOS 27 and 27.1 guidance.

Built from Apple's six Duo technical talks, both complete group-lab caption tracks, SwiftUI/UIKit/camera Q&As, relevant WWDC sessions, public documentation, and Xcode 27.1 SDK declarations. Research checked **October 1, 2026**. Inspired by [Apple Liquid Glass Skill](https://github.com/DanielJamesTronca/apple-liquid-glass-skill) and Xcode's `app-resizability` skill.

## Install

Using the Skills CLI:

```sh
npx skills add DanielJamesTronca/apple-iphone-duo-skill -g
```

In Codex, ask:

```text
Use $skill-installer to install skills/apple-iphone-duo from
https://github.com/DanielJamesTronca/apple-iphone-duo-skill.
```

For manual installation, copy `skills/apple-iphone-duo` to `~/.agents/skills/apple-iphone-duo` for user-wide discovery, or `.agents/skills/apple-iphone-duo` in a project for repository-scoped discovery. Copy the entire folder, including references and scripts.

To browse it as a Codex plugin, register the repository marketplace:

```sh
codex plugin marketplace add DanielJamesTronca/apple-iphone-duo-skill
```

Then open the Plugins Directory in the ChatGPT desktop app, select **Apple iPhone Duo Skill**, and install **Apple iPhone Duo**. Marketplace registration and plugin installation are separate steps.

In Claude Code:

```text
/plugin marketplace add DanielJamesTronca/apple-iphone-duo-skill
/plugin install apple-iphone-duo@apple-iphone-duo-skill
```

The repo includes a portable `plugin.json`, Codex and Claude compatibility manifests, and marketplace catalogs. It is distributed through GitHub; inclusion in a public plugin directory is a separate submission. The skill itself is self-contained and needs no Apple login, local Xcode skill, Python package, or network access to read. Xcode is needed when building Apple-platform code; the optional audit helper uses Python 3.10+.

## Use

```text
Use $apple-iphone-duo to prepare this iPhone app for Duo.

Use $apple-iphone-duo to review this custom layout for resizing,
asymmetric safe areas, and fold avoidance.

Use $apple-iphone-duo to implement direction-aware capture and
outer-display camera accessory content while keeping our iOS 17 fallback.
```

The examples above use Codex invocation syntax. In Claude Code, invoke the installed plugin skill as `/apple-iphone-duo:apple-iphone-duo`, followed by your request.

## Coverage

| Area | Included |
| --- | --- |
| Adoption | Linked SDK vs minimum OS, phone idiom, launch configuration, compatibility and discrete resizing |
| Resizability | Screen/orientation/idiom migration, local geometry, safe areas, scene ownership and cache invalidation |
| Layout | Division/occlusion regions, grids, displacement, split/overlay arrangements, sizing and collapse |
| Navigation | Vertical bars, tabs/sidebars, axis behavior, overflow priorities, minimization and accessibility |
| Presentations | Sheet placement, fold avoidance, popovers and overflow anchors |
| Hinge and sensors | Hinge callbacks, optional interactions, view-relative motion and heading |
| Scenes | Display transitions, state continuity, optional multiple windows and shared/per-scene ownership |
| Cameras | Virtual/physical devices, direction coordination, mirroring, rotation, aspect ratios, recording gaps, Vision and MultiCam |
| Camera accessories | Shared state, availability, minimal outer-display interaction and corrected ARKit guidance |
| System experiences | Widgets/StandBy, Live Activities, AlarmKit, web content and games—with evidence limits |
| Verification | Device Hub, transition/accessibility matrix, hardware checks and beta release limitations |

Start with [SKILL.md](skills/apple-iphone-duo/SKILL.md). Details load only when relevant. The [API catalog](skills/apple-iphone-duo/references/api-catalog.md) separates 27.1 additions from 27.0 and older APIs. The [research ledger](skills/apple-iphone-duo/references/sources.md) documents coverage, conflicts, and unanswered questions.

## Read-only audit

```sh
python3 skills/apple-iphone-duo/scripts/audit_resizability.py /path/to/app
python3 skills/apple-iphone-duo/scripts/audit_resizability.py /path/to/app --json
```

Findings are review candidates, not proven bugs. The helper scans Swift, Objective-C, and Xcode configuration without editing them; ignores ordinary code comments/strings and generated dependency folders; and reports file/line context. Sensor orientation, analytics idiom checks, and intentional game policies can be valid. It is a lexical aid, not a Swift parser.

## Validation

```sh
python3 -m unittest discover -s tests -v
python3 scripts/validate_package.py
./scripts/check_examples.sh  # macOS, with Xcode 27.1 selected
```

Original examples are checked in Swift 6 with iOS 17 availability fallbacks and Catalyst guards. Compile checks do not verify rendered UI, camera handoffs, or accessory presentation; those require app/device testing. [Behavioral evaluation scenarios](tests/skill_evals.json) exercise the skill's decision-making without asserting its wording.

## Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) for updating evidence and validation. Report beta-specific behavior with the exact Xcode and OS build.

MIT licensed. Independent community skill; not affiliated with or endorsed by Apple. Linked Apple materials retain their own rights.
