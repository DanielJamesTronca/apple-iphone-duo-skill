---
name: apple-iphone-duo
description: Prepare, implement, or review iPhone Duo support in SwiftUI, UIKit, and AVFoundation apps. Use for Duo adoption, adaptive layouts, resizing failures, and Duo camera workflows.
license: MIT
---

# iPhone Duo

Build one continuous iPhone experience that adapts as its scene changes size, display, and pose. Prefer system containers and local geometry. Add Duo-specific APIs only where they improve the requested experience.

Research baseline: **2026-10-01**, Xcode **27.1 beta (27A9269)**. Consult [sources](references/sources.md) for provenance, unresolved questions, and update rules. SDK version and deployment target are separate decisions. Recheck availability and beta limitations against the SDK actually selected by the project.

## Choose the relevant references

Read only the references needed for the task:

| Task | Reference |
| --- | --- |
| Adoption, compatibility, device family, build settings | [adoption](references/adoption.md) |
| Screen/orientation/idiom assumptions, safe areas, cached geometry | [resizability](references/resizability.md) |
| Fold/camera avoidance in custom layouts and grids | [reserved regions](references/reserved-regions.md) |
| Two-pane content, split/overlay arrangements, collapse and sizing | [arrangements](references/arrangements.md) |
| Vertical toolbars, tabs, overflow, priority and axis behavior | [bars](references/bars.md) |
| Sheets, popovers, dialogs and presentation anchors | [presentations](references/presentations.md) |
| Hinge-driven interactions, motion/location coordinate spaces | [hinge and motion](references/hinge-and-motion.md) |
| Scene lifecycle, multiple windows, state and display transitions | [scenes](references/scenes.md) |
| Virtual/physical cameras, handoffs, mirroring, rotation and recording | [camera](references/camera.md) |
| Content on the outer display during capture, including ARKit | [camera accessory](references/camera-accessory.md) |
| Widgets, Live Activities, AlarmKit, web content and games | [system experiences](references/system-experiences.md) |
| Device Hub, accessibility, transition tests and release limits | [testing](references/testing.md) |
| Exact new symbols and their introduction versions | [API catalog](references/api-catalog.md) |

Compile-checked [SwiftUI](references/examples/DuoLayout.swift), [UIKit](references/examples/DuoUIKit.swift), [camera direction](references/examples/CameraDirection.swift), [camera accessory](references/examples/CameraAccessory.swift), and [aspect-ratio](references/examples/DynamicAspectRatio.swift) examples accompany the relevant references. They demonstrate API contracts; they are not complete camera apps.

## Workflow

1. Establish the requested scope and inspect the affected UI, navigation/state owners, selected SDK, deployment targets, device family, and resolved scene/launch configuration. For an existing app, start with resizability before adding specialized layouts.
2. Choose structure using local size classes; choose detailed sizing using the actual container's bounds, aspect ratio, and content requirements. Read safe areas and reserved regions from the view that consumes them. The Duo inner display is regular/regular in both orientations; orientation is not a layout proxy.
3. Keep system navigation, tabs, sheets, and overflow where they fit the product. Use arrangements for related content, not navigation. If an arrangement hides a child, retain a route to its essential controls/content.
4. Preserve selection, navigation path, editor drafts, playback, and scroll position across resizing and display transitions. Keep state outside layout branches or accessory views that can disappear. Do not reset view identity with a size class or hinge angle.
5. Gate new APIs for the project's supported OS and platforms; keep a usable existing fallback. Do not raise deployment targets, enable iPad or multiple-window support, remove orientation restrictions, or change product functionality solely to make Duo examples compile.
6. Build the affected target and exercise the relevant transition matrix in [testing](references/testing.md). State which checks actually ran, which need hardware, and what remains unverified.

For a review, report concrete affected behavior, file/line, evidence, and the smallest appropriate fix. A review request does not imply permission to rewrite unrelated UI. For implementation, complete the authorized change and its relevant validation.

## Invariants

- Duo remains the `.phone` idiom. There is no supported `isDuo` switch. Use capabilities and the local layout environment; do not guess from model strings, screen dimensions, or the mere presence of a hinge.
- Neither `UIScreen.main` nor a process-wide orientation, window, or idiom answers how much room a view has. Do not replace one with `connectedScenes.first`, a global key window, or another cached singleton.
- Leading/trailing and top/bottom safe areas can differ and change independently of size. Never mirror one inset to the other edge or apply the same safe area twice.
- Reserved-region geometry drives avoidance. Hinge angle drives optional interactions/effects. Camera direction comes from the direction coordinator. These are different questions.
- Standard bars adapt automatically when linked against 27.1. A floating custom button or standalone bar does not automatically become a standard vertical item. Hardware-aligned bars keep the same physical side in RTL and can move to the left in Split View.
- `UIRequiresFullScreen` enables **discrete resizing** in the documented iOS 27 resizable environments. It does not make scene size constant, and it is not simply ignored. Resolve the built configuration before changing it.
- Camera handoffs may create timestamp gaps without interruption or explicit dropped-frame notifications. Serialize capture changes outside the main actor, retain coordinators, and handle temporary unavailability.
- Outer-display capture content is a system-managed enhancement. Keep essential actions on the main capture interface; no second arbitrary app window or speculative entitlement is needed for a camera accessory.

## Optional read-only audit

For an existing Swift/Objective-C/Xcode project, use Python 3.10+ with no additional packages. Resolve `<skill-path>` from this installed `SKILL.md` directory, independently of the project's working directory:

```sh
python3 <skill-path>/scripts/audit_resizability.py /path/to/project
python3 <skill-path>/scripts/audit_resizability.py /path/to/project --json
```

The helper identifies candidates for inspection, not proven bugs. It does not edit files or parse Swift semantically. Inspect callers and intent: idiom checks for analytics/assets, physical orientation used by a sensor, fixed control sizes, and documented game resizing choices can be valid. Use [resizability](references/resizability.md) to resolve findings.
