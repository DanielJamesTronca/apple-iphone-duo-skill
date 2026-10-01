# Resizability migration

This is an independent synthesis of Apple's Xcode 27.1 `app-resizability` guidance and public documentation. Its five useful migration areas are screen references, orientation, scene lifecycle, safe areas, and idiom. Inspect intent and ownership before replacing an API; a lexical match is not proof of a bug.

## 1. Screen references: answer the local question

| Existing use | Better source |
| --- | --- |
| Screen bounds used to size a view | Container/view bounds or layout guides; SwiftUI proposal, `GeometryProxy`, `containerRelativeFrame` |
| Pixel alignment or rendering scale | Local `traitCollection.displayScale` or SwiftUI `@Environment(\.displayScale)` |
| Genuine display hardware information | The owning `view.window?.windowScene?.screen`, passed explicitly if no view is reachable |
| Scene-wide size/orientation information | Owning `UIWindowScene.effectiveGeometry`; scene delegate's geometry update callback |
| Global key window / first connected scene | The scene/window associated with the action or presenting view |

Prefer the smallest relevant container. A root-window size is still wrong for a child in a sheet, sidebar, split column, or embedded controller. An unattached view may lack a window or have unspecified traits; preserve the existing fallback and update when attached. Do not silently bind a helper to a different scene.

`nativeScale` and `nativeBounds` describe physical display properties; `displayScale` is the logical rendering scale. There is no trait replacement for nativeScale, nativeBounds, or the screen's coordinateSpace. Keep a genuine hardware read on the owning scene's screen; don't swap it for logical scale or view bounds merely because both are numbers. Preserve the semantic value of fallback paths rather than introducing a guessed scale or width.

For a private helper, pass only the information it actually needs and update its callers. For a published API, preserve source compatibility when appropriate with a deprecated forwarding overload and a new context-taking overload. Do not impose compatibility wrappers on every private function. No signature change is necessary when an existing argument/property already supplies the local view. [WWDC26 UIKit, 2:51](https://developer.apple.com/videos/play/wwdc2026/278/?time=171), [TN3210](https://developer.apple.com/documentation/technotes/tn3210-optimizing-your-app-for-iphone-mirroring).

## 2. Orientation: distinguish layout from sensor transforms

- Width-dependent structure: horizontal size class.
- Constrained vertical space: vertical size class.
- Wide versus tall within regular/regular: local bounds/aspect ratio or a fitting layout.
- Genuine motion/camera transform: use the coordinate-space API appropriate to the rendered view, not a substitute size-class check.

`UIDevice.orientation` reports physical pose, including face-up/down/unknown. Interface orientation is not a guarantee about a resizable scene's shape; a mirrored iPhone app can stay interface-portrait while its window is wide. Preserve orientation masks that express a game/product policy. Do not rewrite every orientation read or treat `width > height` as the universal replacement for structure. [WWDC26 UIKit, 6:50](https://developer.apple.com/videos/play/wwdc2026/278/?time=410).

## 3. Scene lifecycle: move the right ownership

Move window construction and UI foreground/background behavior to the scene that owns them. Keep process-wide services, APNs registration, and shared persistence in the application/service layer. Preserve cold-launch and warm deep links and activities, restoration, and scene disconnection. Scene lifecycle does not require multiple app windows. See [scenes](scenes.md).

## 4. Safe areas: preserve all edges and update paths

Safe areas can change on the left or right, independently, and without changing bounds. A vertical bar, camera activation, a sheet, keyboard, or multitasking can invalidate an old assumption.

**UIKit:** constrain meaningful foreground content to the receiving view's `safeAreaLayoutGuide`, `layoutMarginsGuide`, or appropriate `layoutGuide(for:)`. Read current insets during layout, or recalculate cached values in `viewSafeAreaInsetsDidChange` / `safeAreaInsetsDidChange`, as appropriate. Use `keyboardLayoutGuide` for local keyboard avoidance. When dealing with notifications in older code, convert keyboard frames from the correct screen/window coordinate space.

Replace deprecated `topLayoutGuide` / `bottomLayoutGuide` or hardcoded status/navigation offsets with the appropriate local guide. Distinguish a deliberate full-bleed background/scroll container from a foreground control before changing superview-edge constraints. For manual corner-aware layout, inspect `UIView.LayoutRegion`'s safe-area/margins/readable-content corner adaptation and edge-inset accessors rather than inventing a device-specific corner constant.

**SwiftUI:** let normal layout honor safe areas. Apply `ignoresSafeArea` to the background/media that should bleed, on only the needed edges. Use `safeAreaBar` or `safeAreaInset` for controls that consume safe-area space. A nested proxy reports its own safe area; padding with an ancestor inset as well can double-count it. Avoid blanket `.ignoresSafeArea()` on a root containing interactive foreground content.

**Scrolling:** full-bounds scroll content with automatic adjustment is often correct. UIKit `adjustedContentInset` already includes system adjustment; don't add `safeAreaInsets` again. Keep intentional content margins separate from obstruction avoidance. Custom layouts need to recompute scroll/collection item widths from their actual container.

Reject symmetry hacks such as `left * 2`, applying `max(left, right)` to both sides, hardcoded notch/status heights, or centering every foreground view in the full screen. A full-width immersive background can coexist with a foreground centered within the usable area. Respect corner geometry too: iOS 26's concentric shapes and `UICornerConfiguration` avoid stale constant-radius assumptions. `backgroundExtensionEffect` / `UIBackgroundExtensionView` can extend hero backgrounds under system UI without making their controls unsafe. [Layout session](https://developer.apple.com/videos/play/tech-talks/111463/), [WWDC25 flexible UIKit](https://developer.apple.com/videos/play/wwdc2025/282/).

## 5. Idiom: ask about space when that is the intent

An iPad, mirrored iPhone app, and Duo may offer substantial space without the same idiom. Change layout-driven `isPad`, `IS_PAD`, and `UIDevice.current.userInterfaceIdiom` checks at their owning helper/call sites after inspecting their definitions. Width decisions use horizontal size class; height decisions use vertical size class. Preserve legitimate idiom use for analytics, assets, platform behavior, and deliberate orientation policies.

Read genuine UI idiom dependence from the nearest UIKit trait environment when available. SwiftUI has no general `userInterfaceIdiom` environment key: don't invent one. With optional SwiftUI size classes, `== .regular` selects the expanded case; `!= .compact` also accepts `nil` and is not equivalent. [WWDC26 UIKit, 6:17](https://developer.apple.com/videos/play/wwdc2026/278/?time=377).

## Invalidation is part of the migration

A global constant replaced by a local trait is now dynamic. If a trait configures a stored constraint, rendered image, scale, visibility flag, or cached layout choice, ensure it updates:

- Read it fresh in a method supported by automatic trait tracking; use the exact OS-specific list in [Automatic trait tracking](https://developer.apple.com/documentation/uikit/automatic-trait-tracking).
- Otherwise register the relevant traits with `registerForTraitChanges` (iOS 17+) and recalculate the owner. Initialize from a meaningful attached environment, for example `viewIsAppearing`, as well as handling subsequent changes.
- For an older deployment target, gate the newer API and retain an older `traitCollectionDidChange` path as necessary. Do not remove the old path without considering supported OS versions.
- In SwiftUI, read environment/geometry in the view body or appropriate geometry observation. Don't put one-time size-class snapshots in a model or a `lazy` global. Representables need to respond in `updateUIView` / `updateUIViewController`, not only in creation.

Avoid assuming registration always delivers an initial callback. Bounds changes within a size class still need layout/geometry handling. Preserve meaningful existing guards and branch semantics; do not make sensor behavior or product capabilities disappear because a layout migration changed a predicate. [Traits guidance](https://developer.apple.com/documentation/uikit/adapting-your-app-when-traits-change).
