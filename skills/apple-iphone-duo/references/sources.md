# Research coverage and maintenance

Checked **2026-10-01**, with **Xcode 27.1 beta (27A9269)**. The skill contains original guidance and original examples; Apple documentation and recordings retain their respective rights. Apple is not the author or endorser of this skill.

## Core source coverage

| Source | Material examined | Where applied |
| --- | --- | --- |
| [iPhone Duo developer hub](https://developer.apple.com/iphone-duo/) | Linked sessions, labs, Q&As, docs and design resources | Discovery and scope |
| [Preparing your app for iPhone Duo](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo) | Public DocC overview and linked API documentation | Adoption and API inventory |
| [Duo Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) | Full DocC article; September 9, 2026 change log | Consistency, dynamic layouts, controls and games |
| [Design for iPhone Duo — 111466](https://developer.apple.com/videos/play/tech-talks/111466/) | Full transcript and chapter summaries | Design, asymmetry, sheets, continuity |
| [Prepare your app — 111461](https://developer.apple.com/videos/play/tech-talks/111461/) | Full transcript and code | SDK behavior, traits, tooling |
| [Raise the bar — 111462](https://developer.apple.com/videos/play/tech-talks/111462/) | Full transcript and code | Vertical bars, axes, overflow, accessibility |
| [Strike a pose with adaptive layouts — 111463](https://developer.apple.com/videos/play/tech-talks/111463/) | Full transcript and code | Reserved regions, displacement, arrangements |
| [Leverage multiple displays and scenes — 111464](https://developer.apple.com/videos/play/tech-talks/111464/) | Full transcript and code | Scenes, hinge, windows, outer-display capture |
| [Build a great camera experience — 111465](https://developer.apple.com/videos/play/tech-talks/111465/) | Full transcript and code | Virtual/physical cameras, direction and mirroring |
| [Group Lab — day 1, 285](https://developer.apple.com/videos/play/meet-with-apple/285/) | Entire English HLS subtitle track, 1,207 normalized cues | Resizing, poses, widgets, camera, sidebar and web caveats |
| [Group Lab — day 2, 286](https://developer.apple.com/videos/play/meet-with-apple/286/) | Entire English HLS subtitle track, 1,298 normalized cues | Games, bar decisions, scenes/audio, tent mode, widgets |
| [SwiftUI Q&A](https://developer.apple.com/forums/activities/1664080) | Activity index and relevant linked threads/replies | Grids, arrangements, unsupported assumptions, test limitations |
| [UIKit Q&A](https://developer.apple.com/forums/activities/1670080) | Activity index and relevant linked threads/replies | Sidebar opt-in, accessories, custom bars/collections |
| [Photos & Camera Q&A](https://developer.apple.com/forums/activities/1659080) | Activity index and relevant linked threads/replies | Frame gaps, sustained analysis, MultiCam and ARKit correction |
| [WWDC26: Modernize your UIKit app — 278](https://developer.apple.com/videos/play/wwdc2026/278/) | Resizability, lifecycle, bars and Body protocols; transcript/code | Five migration areas and related iOS 27 APIs |
| [WWDC26: What's new in SwiftUI — 269](https://developer.apple.com/videos/play/wwdc2026/269/) | Relevant resizability/toolbar transcript and code | Overflow, pinned actions, minimization, prominent tabs |
| [WWDC26: Support the Center Stage front camera — 341](https://developer.apple.com/videos/play/wwdc2026/341/) | Full transcript and code | Aspect ratios, framing, compensation, recording and calls |
| [WWDC25: Make your UIKit app more flexible — 282](https://developer.apple.com/videos/play/wwdc2025/282/) | Relevant container, safe-area, trait and scene guidance | Existing resizability foundations |
| [TN3192](https://developer.apple.com/documentation/technotes/tn3192-migrating-your-app-from-the-deprecated-uirequiresfullscreen-key), [TN3208](https://developer.apple.com/documentation/technotes/tn3208-preparing-your-apps-launch-screen-to-meet-app-store-requirements), [TN3210](https://developer.apple.com/documentation/technotes/tn3210-optimizing-your-app-for-iphone-mirroring) | Public DocC technotes | Full-screen compatibility, launch screen, mirroring |
| [Xcode 27.1 notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_1-release-notes), [27.2 notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_2-release-notes) | Current release-note guidance | Correct Duo toolchain and beta limitations |
| [App Store Connect release notes](https://developer.apple.com/help/app-store-connect/release-notes/) | Dated submission/screenshot announcements | Distribution limits |

[source-index.json](source-index.json) records **73 retrieved public documentation pages**, canonical URLs, check date, and published iOS introduction metadata when present. It is provenance, not a replacement for the relevant discussion or installed SDK. API references link directly from each topic and the [catalog](api-catalog.md).

## SDK and local skill cross-check

Inspected iPhoneOS SDK public Swift interfaces and headers for SwiftUI/SwiftUICore, UIKit, AVFoundation, AVKit, CoreMotion, CoreLocation, and the relevant system frameworks. The API catalog distinguishes iOS 27.1 additions, iOS 27.0 supporting features, and existing APIs reused by Duo.

The locally bundled Xcode 27.1 `app-resizability` prompt and all five task references informed the independent resizability workflow. They are not copied into this repository, and the skill works without that local package. The user's [Liquid Glass skill](https://github.com/DanielJamesTronca/apple-liquid-glass-skill) informed repository packaging and progressive references.

## Resolve conflicts explicitly

| Conflict | Chosen evidence and consequence |
| --- | --- |
| Local modernization text says FullScreen is ignored | TN3192 and WWDC26 describe **discrete resizing**; preserve valid game policies |
| Early lab speculation about entitlement/no touch for capture accessory | Current registration docs specify registration, no project-level role entry, and minimal interaction |
| ARKit Q&A's initially accepted negative answer | Later Apple staff correction: active ARSession qualifies, without a second independent AR experience |
| Reserved-region discussion says inactive regions are always returned | Session and explicit `.includeInactive` query contract; choose options explicitly and filter active geometry |
| WWDC transcript uses `toolbarMinimizeBehavior` | Installed SDK/public docs use `toolbarMinimizationBehavior(_:for:)` |
| Objective-C aspect-ratio type appears in prose | Swift imports `AVCaptureDevice.AspectRatio`; original example compiled against SDK |
| Accessory cleanup described as `registration.unregister()` | Current registration guide and `UIViewController.h` declare `UIViewController.unregisterSceneAccessory(_:)`; corrected guidance and type-checked the original UIKit example |
| Developer assumes phone sidebar auto-promotes | Framework staff clarifies explicit opt-in is required |

Prefer the selected SDK for declarations and compile-time availability, current API docs/technotes for contracts, recent framework-engineer corrections for behavior, and recorded sessions for design rationale. Clearly label inference where these do not settle a question. A Q&A answer is not reliable merely because it is the first or accepted reply; inspect the full reply history.

## Access and validation limits

- Both lab pages lacked usable inline transcripts, so the complete **English captions** were retrieved from their official HLS subtitle playlists. Captions are not a visual review of every slide/demo and can contain transcription errors; verify symbol spelling in docs/SDK.
- The linked consolidated Group Lab summary (`apple.co/iPhoneDuo-QA01`, resolving to forum thread `847644`) was blocked by verification/fetch errors. It is not treated as read; the full lab captions and accessible individual Q&As supply the lab coverage.
- Dedicated documentation for some new container-margin and bar-region helpers, an iOS 27.1 release-note page, and the detailed AR world-tracking-across-fold thread could not be retrieved. SDK-only APIs and open questions are labeled accordingly.
- Exact Safari foldable-standard support, Lock Screen widget counts, SwiftUI overflow confirmation anchoring, and CLI pose control remain unconfirmed. They are not generated as established features.
- Examples are type-checked, not hardware-validated. Real camera, accessory presentation, thermal behavior, and rendered accessibility must be checked by the consuming app.

## Updating the skill

1. Revisit the Duo hub, current release notes, HIG change log, technotes, and linked Q&A corrections when Apple's SDK changes.
2. Retrieve relevant public DocC JSON (`/tutorials/data/<documentation-or-design-path>.json`) or official Markdown representations, and official session transcripts/captions. Don't publish copied transcripts or private/authenticated material.
3. Cross-check new or renamed symbols and platform availability in the selected SDK. Keep iOS 27.0 and earlier features labeled separately from 27.1 additions.
4. Update the affected reference and provenance date. Resolve contradictions at their owner rather than piling repeated rules into SKILL.md.
5. Run audit CLI tests, the skill/package validator, and the example compile check. Use realistic skill evaluations for routing/decision changes; don't test exact prose or headings as a substitute for behavior.
