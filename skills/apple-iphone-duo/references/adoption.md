# Adoption and compatibility

## Linking versus deployment

| Linked SDK | Duo behavior to expect |
| --- | --- |
| Before iOS 27 | Familiar iPhone compatibility frame; letterboxing can remain |
| iOS 27 | Resizable app; compatibility status-bar strip remains |
| iOS 27.1 | Edge-to-edge layout and automatic vertical standard bars |

These are compatibility behaviors controlled by linking, not a reason to raise the app's minimum OS. Xcode 27.1 supplies the Duo SDK and simulator. The concurrently released 27.2 beta is not a substitute: Apple's 27.2 release notes specifically direct Duo development to 27.1. Recheck this distinction when updating toolchains. [Prepare session](https://developer.apple.com/videos/play/tech-talks/111461/), [27.1 notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_1-release-notes), [27.2 notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_2-release-notes).

There is no separate foldable-layout entitlement or Info.plist opt-in. Start with an adaptive iPhone app. Supporting iPad helps test a large layout but is not required; adding `TARGETED_DEVICE_FAMILY = 2` changes distribution and is not a Duo prerequisite. An iPad-only app must add iPhone support to run on Duo. Duo continues to report `.phone`; no `.duo` idiom or supported model-detection API exists. [Device-family Q&A](https://developer.apple.com/forums/thread/847945), [detection Q&A](https://developer.apple.com/forums/thread/847775).

## Local layout environment

| Full display | Horizontal | Vertical |
| --- | --- | --- |
| Outer, portrait | Compact | Regular |
| Outer, landscape | Compact | Compact |
| Inner, either orientation | Regular | Regular |

Use the traits of the actual view, not this table as a pose classifier. Split View, presentations, and pinned PiP can change the available area. The inner display can become wide or tall without a size-class change. Size classes select structure; local bounds and content fitting refine it. Use `NavigationSplitView` / `UISplitViewController` for hierarchy and expand existing content when appropriate. Keep the same destinations and tasks on both displays. [Prepare session](https://developer.apple.com/videos/play/tech-talks/111461/), [HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo).

## Configuration inspection

Inspect target settings, xcconfigs, any generated Info.plist settings, and the built product's merged Info.plist. Neither a source plist nor a single `.pbxproj` line is universally authoritative. `xcodebuild -showBuildSettings` with the actual scheme/configuration exposes resolved build settings. Check:

- Scene lifecycle adoption (`UIApplicationSceneManifest` for UIKit or SwiftUI scene declarations). The latest SDK requires scene lifecycle; multi-window support is a separate optional feature.
- A compliant launch screen, including storyboard or generated launch screen. Remove legacy launch-image assumptions as appropriate; don't replace a valid configuration blindly. Follow [TN3208](https://developer.apple.com/documentation/technotes/tn3208-preparing-your-apps-launch-screen-to-meet-app-store-requirements).
- `UISupportedInterfaceOrientations` and its device-specific variants. Orientation declarations remain system preferences and matter to discrete resizing; deleting them is a product choice, not a mechanical Duo fix.
- `UIRequiresFullScreen`, `UIRequiresFullScreenIgnoredStartingWithVersion`, and app/game assumptions about fixed render surfaces.

### Full-screen compatibility is discrete resizing

The exact key is **`UIRequiresFullScreen`**. It is deprecated on iPadOS 26. For apps linked against iOS/iPadOS 27, `YES` enables the documented discrete-resizing behavior in resizable environments unless `UIRequiresFullScreenIgnoredStartingWithVersion` disables it for that OS. The system can still change scene configurations as the device opens/closes or multitasking changes. The setting honors supported orientations; it does not guarantee immutable bounds or disable Duo multitasking. Scale/render surfaces using the supplied scene configuration. [TN3192](https://developer.apple.com/documentation/technotes/tn3192-migrating-your-app-from-the-deprecated-uirequiresfullscreen-key), [WWDC26 UIKit, 5:46](https://developer.apple.com/videos/play/wwdc2026/278/?time=346).

Prefer continuous resizing for ordinary apps. For a game that deliberately uses discrete resizing, preserve that choice and verify all resulting sizes. Do not auto-delete the key, force all orientations, or announce that iOS 27 ignores it. An early local modernization prompt can conflict with the newer technote; the technote and SDK take precedence.

## Availability and fallback

Use `if #available(iOS 27.1, *)` or isolated `@available` types for Duo layout APIs; maintain the existing functional layout below that version. Some related features began in iOS 27.0 or earlier—see [API catalog](api-catalog.md). Other platforms have individual availability constraints.

Xcode 27.1 beta has a documented Catalyst issue: iOS 27.1-specific API references can fail to compile. Isolate affected code with `#if !targetEnvironment(macCatalyst)` and keep a Catalyst fallback; a runtime availability check alone cannot resolve missing declarations. If Catalyst has no destination with a 27.1 minimum, Apple documents a Catalyst 27.0 minimum workaround. Apply only when relevant to that target. [Release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_1-release-notes).
