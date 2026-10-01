# Reserved regions

## Query the view that needs avoidance

In iOS 27.1, use `GeometryProxy.reservedRegions(kind:options:layoutDirectionBehavior:)` in SwiftUI and `UIView.reservedRegions(kind:options:)` in UIKit. A region describes an `id`, `kind`, local `frame`, `margins`, and `isActive`. The kinds are singular **`.division`** and **`.occlusion`**, not `.divisions` or `.occlusions`. [SwiftUI query](https://developer.apple.com/documentation/swiftui/geometryproxy/reservedregions(kind:options:layoutdirectionbehavior:)), [UIKit query](https://developer.apple.com/documentation/uikit/uiview/reservedregions(kind:options:)).

| Kind | Meaning | Duo example |
| --- | --- | --- |
| `.division` | Splits an area into usable regions | Fold when partially open |
| `.occlusion` | Obstructs a smaller area | Outer camera/Dynamic Island or active inner camera |

Default queries return active regions according to the layout session and query-option contract. Use `options: .includeInactive` when you need knowledge of a region even when flat/inactive; defensively inspect `isActive` before displacing content. An inactive fold can have zero width. Do not treat an inactive or zero-area rectangle as an obstruction. Query multiple results rather than assuming a single global hinge/camera. One SwiftUI discussion sentence currently says all regions are returned regardless of activity; this conflicts with the explicit option and session. Keep the option explicit when activity matters, and verify behavior in the selected SDK. [Layout session, 6:39](https://developer.apple.com/videos/play/tech-talks/111463/?time=399), [query options](https://developer.apple.com/documentation/swiftui/reservedregion/queryoptions).

The inner camera region may activate because another app is using the camera. The fold is not an extra safe-area inset, and folding does not necessarily change traits. Do not use safe-area changes or size classes as the sole fold signal. [Framework engineer clarification](https://developer.apple.com/forums/thread/847772), [region update Q&A](https://developer.apple.com/forums/thread/847876).

## What should move

Prefer system containers: split views, alerts, sheets, menus, and popovers already incorporate the relevant avoidance. For custom content:

- Move stationary important controls or related groups out of an active region using its frame and margins, keeping movement small and contextual.
- Keep a related control and the content it affects together. Avoid moving a button far away merely to center it in a half-display.
- Preserve content and functionality in every configuration. Displacement changes placement/size, not the product's information hierarchy.
- Let continuous articles, feeds, lists, and documents scroll across the fold. Repositioning an entire scrolling feed interrupts continuity.
- For a grid of important interactive cards, consider an even column count when a division exists (including inactive divisions), then increase the central gap when active. Ordinary SwiftUI grids and collection layouts do not automatically avoid the fold. `UICollectionViewCompositionalLayout` currently has no automatic fold avoidance; compute relevant spacing from actual regions/container geometry.

This does not require a custom half-screen layout in every app or forcing all text around the fold. [HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo), [layout session](https://developer.apple.com/videos/play/tech-talks/111463/), [grid Q&A](https://developer.apple.com/forums/thread/847826), [collection-view clarification](https://developer.apple.com/forums/thread/847879).

## Coordinates, RTL, and updates

Region frames belong to the querying view/proxy. Query at the layout consumer, or convert through the real view hierarchy before comparing against a rect in another space. Include region-provided margins according to that coordinate space; don't hardcode a hinge width, midpoint, pose threshold, or camera radius.

SwiftUI defaults `layoutDirectionBehavior` to `.mirrors`, suitable for a `Layout` that itself mirrors subview placement. Use `.fixed` only for manual geometry that intentionally manages physical coordinates, and handle RTL exactly once. Camera hardware does not physically move in RTL; this differs from the logical direction of a custom content layout. [Geometry documentation](https://developer.apple.com/documentation/swiftui/geometryproxy/reservedregions(kind:options:layoutdirectionbehavior:)).

Read regions during current layout. SwiftUI supports querying in a `GeometryReader` or `onGeometryChange` transform; store only the geometry actually needed if a downstream consumer needs state. UIKit can query the target view during layout and recalculate affected custom layout data when it changes. Do not invent a reserved-region trait or KVO notification: Apple's Q&A doesn't fully specify every UIKit invalidation callback. Verify folding **and camera activation without a bounds change**. If an explicit hinge hook invalidates custom layout, still derive rectangles from the region query rather than the angle. [Update Q&A](https://developer.apple.com/forums/thread/847876).
