# Arrangements

## Select the container by purpose

| Purpose | Container |
| --- | --- |
| Navigate a hierarchy, with columns that collapse into a stack | `NavigationSplitView` / `UISplitViewController` |
| Linear navigation through a flow | `NavigationStack` / `UINavigationController` |
| Mutually exclusive destinations | `TabView` / `UITabBarController` |
| Arrange two related content areas without owning navigation | `ArrangementView` / `UIArrangementViewController` |
| Continuous scrolling content | Existing `List`, `ScrollView`, table, or collection container |

Keep navigation outside an arrangement. An arrangement is not a custom split-navigation system. Place it within the appropriate content destination; do not put navigation controllers/stacks inside its primary and secondary children. Do not mechanically replace every HStack, VStack, or ZStack: an arrangement can hide a child, unlike an ordinary stack. Avoid using one where a scrolling row or List needs all content continuously available. [HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo), [layout session](https://developer.apple.com/videos/play/tech-talks/111463/), [navigation Q&A](https://developer.apple.com/forums/thread/847795).

## Split and overlay in iOS 27.1

**Split:** `ArrangementView` takes `primary` and `secondary` closures. Its automatic style resolves to split. Split generally follows the container's wide/tall aspect ratio, and incorporates active divisions. `.arrangementViewStyle(.split.axes(.horizontal))` restricts allowed axes; it does not force both children to remain visible when the preferred axis is unavailable. A child can collapse out of the layout.

Prioritize the more important content with `.layoutPriority(...)`. In a child, `@Environment(\.splitArrangementAxis)` is an optional axis; `nil` describes a collapsed split. Provide a toolbar/sheet/navigation route or equivalent compact representation for essential content/actions otherwise lost with the secondary pane. Own its state above the arrangement so presentation changes don't create a fresh document/player. [ArrangementView](https://developer.apple.com/documentation/swiftui/arrangementview), [split style](https://developer.apple.com/documentation/swiftui/splitarrangementviewstyle).

**Overlay:** `.arrangementViewStyle(.overlay)` places primary content above secondary content when flat, then separates them around the active fold. This suits media behind playback controls. In the default folded layouts, the primary controls go toward the trailing/bottom region and the secondary background/media toward the leading/top region. `.overlayArrangementEdge(...)` adjusts a child's preference; `.axes(...)` limits supported split axes. Read `@Environment(\.overlayArrangementZIndex)` **inside the child**: a positive value denotes its overlay position; zero denotes its non-overlaid placement. Use this to vary compact/expanded controls while preserving the same commands. [Layout session, 13:21](https://developer.apple.com/videos/play/tech-talks/111463/?time=801).

Environment values read above an arrangement don't describe that arrangement's children. A safe-area bar attached to the primary child can remain in that child's region; a bar attached outside the arrangement still spans the surrounding area. [safeAreaBar Q&A](https://developer.apple.com/forums/thread/847790).

## Sizing controls beyond the session examples

Apply these to the **child**, not the arrangement container:

- `splitArrangementLayoutRatio(_:)`: preferred fractional share. Higher-layout-priority children size first; remaining space and container filling can change the final ratio.
- `splitArrangementLayoutRatio(minHorizontal:idealHorizontal:maxHorizontal:minVertical:idealVertical:maxVertical:)`: separate ratio ranges for horizontal/vertical splitting.
- `splitArrangementLayoutSize(minWidth:idealWidth:maxWidth:minHeight:idealHeight:maxHeight:)`: point-based min/ideal/max per axis. Keep minima modest enough for the smallest supported content area.
- `splitArrangementFixedLayoutSize(horizontal:vertical:)`: request fixed/intrinsic sizing on selected axes. It is not a fixed-device-width workaround.
- `.layoutPriority(...)`: controls sizing precedence and which view remains when collapsing.

These are preferences constrained by available geometry. Do not promise a fixed 30/70 or 50/50 ratio across a division. Inspect the installed SDK if a sizing API is missing in an older Xcode. [Ratio docs](https://developer.apple.com/documentation/swiftui/view/splitarrangementlayoutratio(_:)), [size docs](https://developer.apple.com/documentation/swiftui/view/splitarrangementlayoutsize(minwidth:idealwidth:maxwidth:minheight:idealheight:maxheight:)), [SDK catalog](api-catalog.md).

## UIKit equivalents

Set child controllers with `setViewController(_:for:)` and apply `updateArrangement(.split.axes(.horizontal))` or `.overlay`. `state(for:)` provides the child's `splitAxis`, `zIndex`, and `isHidden`. A child can find its nearest `arrangementViewController`. Preserve usual view-controller containment and state ownership; use the controller's provided placement APIs rather than manually adding its children again. [Controller docs](https://developer.apple.com/documentation/uikit/uiarrangementviewcontroller).

`UISplitArrangement` exposes `defaultViewProperties`, then `setViewProperties(_:for:)` for each placement. Its `ViewProperties` have `width`, `height`, and `layoutPriority`; each `DimensionRange` has `minimum`, `preferred`, and `maximum`. A `Dimension` can be `.automatic`, `.intrinsic`, `.fractional(...)`, or `.absolute(...)`. `UIOverlayArrangement.ViewProperties.edge` chooses a directional edge; both arrangements have `.axes(...)`. Swift overlay types are value types even though Objective-C headers expose refined class names. Do not paste Objective-C initializer spellings into Swift. [API catalog](api-catalog.md).

See the compile-checked [SwiftUI example](examples/DuoLayout.swift) for an accessible secondary sheet route and [UIKit example](examples/DuoUIKit.swift) for arrangement construction. Layout APIs also adapt on other supported platforms; retain a normal pre-27.1 layout and check target-specific availability.
