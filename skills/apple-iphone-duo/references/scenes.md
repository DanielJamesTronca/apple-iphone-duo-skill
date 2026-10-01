# Scenes and continuous state

## One scene can change display and size

A full-screen app moves its existing scene between displays when Duo opens/closes. In Split View multitasking, the most recently active app continues on the outer display and the other backgrounds. Reopening restoration involves system heuristics; don't encode an exact timing guarantee. Pinned PiP can reduce app height independently of opening, orientation, or width. Display movement isn't equivalent to a background/foreground cycle, and the scene can resize while remaining active. [Scenes session](https://developer.apple.com/videos/play/tech-talks/111464/), [design session](https://developer.apple.com/videos/play/tech-talks/111466/).

Own selection, navigation paths, drafts, playback, and meaningful scroll state above ephemeral layout branches. Do not use `.id(horizontalSizeClass)`, hinge angles, or screen changes to “refresh” the root; that destroys state. Keep a single model for a document/player as its representation expands or collapses. Avoid independent copies of editable state in each pane.

## UIKit lifecycle migration

Scene lifecycle is the required foundation for SDK 27-era apps, including apps that offer only one window. App-level Split View multitasking doesn't require supporting multiple scenes. Multiple-window support is a separate optional product capability. [WWDC26 UIKit](https://developer.apple.com/videos/play/wwdc2026/278/), [staff clarification](https://developer.apple.com/forums/thread/847966).

When migrating:

1. Create and retain a `UIWindow(windowScene:)` in the connecting scene delegate, then assign that scene's root controller. Do not recreate a process-wide window or bind it to a global screen.
2. Move UI activation, foreground, background, and disconnection work to the corresponding scene callbacks. Do not move process-wide initialization into every connection; keep shared services and APNs setup at their process owner.
3. Preserve cold-launch `connectionOptions.urlContexts` and `userActivities`, and warm `scene(_:openURLContexts:)` / `scene(_:continue:)` routing. Deliver the event to the correct scene's navigation model.
4. Preserve restoration activities and document identity. Clean up per-scene observations/resources when disconnecting, without deleting app-wide state still needed by another scene.
5. For scene-wide geometry, inspect the owning scene's `effectiveGeometry` and `windowScene(_:didUpdateEffectiveGeometry:)`; for child layout use the child's own bounds.

Inspect actual scene configurations in the built Info.plist or programmatic delegate. Don't blindly add a second lifecycle mechanism to an app already using SwiftUI scenes. [Scene migration](https://developer.apple.com/documentation/uikit/transitioning-to-the-uikit-scene-based-life-cycle), [flexible UIKit](https://developer.apple.com/videos/play/wwdc2025/282/).

## Multiple windows, when the app offers them

New app windows are available on the inner display, not universally in every Duo configuration. Check `UIApplication.shared.supportsMultipleWindows` when performing the action and handle scene-activation errors. `UIWindowSceneActivationAction` automatically adapts its visibility where activation isn't supported; custom commands need an equivalent capability check. Do not cache availability at startup or assume a previously successful action still applies after closing. [Scenes session, 3:38](https://developer.apple.com/videos/play/tech-talks/111464/?time=218).

Keep navigation and editing selection per scene (`SceneStorage` when appropriate); use `AppStorage`/shared persistence only for truly shared preferences/data. Different windows are not independent app processes. Coordinate concurrent edits with the existing persistence design. There is still a shared process-wide audio session; don't create an imaginary per-display AVAudioSession. Scene-phase changes are appropriate for lifecycle work, not fold-layout classification. [Group lab, day 2, 33:33](https://developer.apple.com/videos/play/meet-with-apple/286/?time=2013).

## Second-display content

Ordinary window creation doesn't grant arbitrary simultaneous inner/outer interfaces. For active camera capture, use the system-managed [camera accessory](camera-accessory.md). For a connected external display, use its supported scene/accessory mechanism. AlarmKit's system tent-mode glow and widgets are separate system experiences; they don't authorize a general second scene on Duo's outer display.
