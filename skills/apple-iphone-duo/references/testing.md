# Validation and release

## Verify transitions, not only snapshots

Choose the rows relevant to the affected feature. At each transition, verify both layout and continuity of selection, navigation, draft text, scroll position, playback, or capture.

| Situation | Main checks |
| --- | --- |
| Outer portrait and landscape | Compact width, asymmetric safe areas, reachable items/overflow |
| Inner wide and tall | Both can remain regular/regular; local sizing and meaningful density |
| Flat → partial book → flat | Fold activation/deactivation, related control displacement, retained state |
| Seated/table pose | Stable lower controls, visible upper content, keyboard and presentations |
| Standing/tent pose | Appropriate ordinary layout; don't assume arbitrary dual-display access |
| Repeated open/close while interacting | Same navigation/draft/player; no identity reset or stale cached geometry |
| Both app-level Split View sides | Left/right vertical-bar edge, collapse and per-scene presentation |
| Pinned PiP and keyboard | Height-only changes, overflow, safe-area change without width change |
| Inner camera activates/deactivates | Occlusion handling even without bounds/trait changes |
| Largest Dynamic Type and longer translations | Text fits, controls remain identifiable, no lost actions |
| VoiceOver and Large Content Viewer | Focus/order across collapse, semantic labels, target access |
| RTL | Content mirrors correctly; hardware bars remain physically aligned |
| Reduce Motion/Transparency and increased contrast | Optional hinge effects and custom surfaces remain usable |

Large Content Viewer/scrubbing of system items helps accessibility when a dense icon bar can't enlarge every item; custom narrow controls need equivalent semantic labels and appropriate accessibility support. A compiler pass cannot validate focus or touch behavior. [Bars session](https://developer.apple.com/videos/play/tech-talks/111462/), [Duo HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo).

## Tooling

Use **Xcode 27.1's Device Hub** for the Duo simulator: switch active displays, fold/open/close, rotate, and exercise available poses/hinge controls. Live Previews offer resize handles; the Display override previews alternate displays. Ordinary iPhone resizing, iPad, and iPhone Mirroring help isolate generic resizing bugs but don't emulate all Duo reserved regions, vertical bars, or cameras. [Prepare session, 1:17](https://developer.apple.com/videos/play/tech-talks/111461/?time=77), [running apps](https://developer.apple.com/documentation/xcode/running-your-app-on-simulated-or-physical-devices).

Do not invent a `simctl fold`/`pose`/`unfold` command or presume screenshots alone select the active display. Inspect the installed CLI's actual help and use Device Hub manually where automation isn't documented. The dedicated programmatic unfolding Q&A remains unresolved. Likewise, a developer's reported stale XCUITest frames during live resizing are not a proven universal system bug: inspect current tool support, wait for the UI's actual stable state, and verify interaction on the selected build. Don't silently compensate taps with guessed scale multipliers. [Unfolding question](https://developer.apple.com/forums/thread/847883), [snapshot question](https://developer.apple.com/forums/thread/847880).

Build with the actual supported deployment targets and platform variants. For examples in this repo, run `scripts/check_examples.sh` from the repository root on a Mac with the Duo-supporting Xcode selected. The script type-checks Swift 6 for iOS 17 plus a Catalyst fallback configuration. It verifies names/availability/concurrency, not rendered or camera behavior.

When only the installed skill folder is available, its original examples can be checked directly:

```sh
xcrun swiftc -typecheck -swift-version 6 \
  -sdk "$(xcrun --sdk iphoneos --show-sdk-path)" \
  -target arm64-apple-ios17.0 <skill-path>/references/examples/*.swift
```

Use the consuming project's deployment target and platform when checking its actual code.

## Hardware-only capture verification

Simulator has no real camera; a camera app needs a usable no-camera fallback to exercise other UI. On hardware test:

- Virtual front transitions across displays, camera permission states, interruptions, pressure/thermal behavior, and timestamp gaps.
- Explicit physical selection, coordinator direction updates, unchanged eligible selection, stale async requests, and temporary inner-camera unavailability.
- Preview versus captured-media mirroring, rotation/EXIF, new connections, and sensor orientation compensation.
- Recording across handoffs and dynamic-aspect-ratio changes; validate sample dimensions and final assets.
- Accessory availability and user enablement, navigation away/back, active capture, closing/backgrounding, and shared-model continuity.
- MultiCam and Vision/ARKit workloads actually used by the app.

Do not claim these were tested from a type-check, a preview, or an ordinary simulator view. [Accessory guide](https://developer.apple.com/documentation/avfoundation/registering-a-camera-capture-accessory-on-iphone-duo), [continuity Q&A](https://developer.apple.com/forums/thread/847766).

## Beta and distribution limits

As checked on 2026-10-01, Xcode 27.1 beta documents slow initial simulator launch, no Duo StandBy, and unavailable run/debug for most app extensions. Catalyst has 27.1-specific API/destination issues described in [adoption](adoption.md). Do not rewrite working production layout to work around an unverified simulator-only artifact. File a minimal reproduction with the actual Xcode/OS versions when appropriate. [27.1 release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_1-release-notes).

App Store Connect added Duo screenshot/preview specifications September 9; that announcement said uploads would be available later in the year. It also allows 27.1 beta TestFlight builds as of September 18. Recheck submission support and the live specifications at release time; don't treat beta TestFlight acceptance as App Store production acceptance, invent an “optimized for Duo” badge requirement, or hardcode dimensions from an old screenshot. [Release notes](https://developer.apple.com/help/app-store-connect/release-notes/), [screenshot specs](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications).
