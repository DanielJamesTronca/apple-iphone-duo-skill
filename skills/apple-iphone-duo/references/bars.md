# Vertical bars, tabs, and overflow

## Let navigation containers own bar adaptation

Linked against iOS 27.1, standard navigation, toolbars, and tab bars share a vertical area along the display edge in the relevant Duo configurations. Inner portrait retains horizontal bars. In app-level Split View multitasking, each app's bar sits on its outer edge—the left app can have a left bar. In RTL, hardware-aligned bars stay on the same physical side. Don't hardcode “right,” calculate it from orientation, or move a custom floating button there manually. [Bars session](https://developer.apple.com/videos/play/tech-talks/111462/), [HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo).

Standalone `UINavigationBar`, `UIToolbar`, and `UITabBar` do not become the system vertical bar by themselves. Prefer navigation/tab controllers. For a split navigation interface, only the appropriate edge/detail column gets the vertical bar; leading/content columns and an expanded inspector retain contextual horizontal controls. A custom action affecting one pane should remain near that pane. [Bars session, 11:55](https://developer.apple.com/videos/play/tech-talks/111462/?time=715).

Read `@Environment(\.toolbarVerticalEdge)` (optional `HorizontalEdge`) or `traitCollection.verticalBarEdge` (`.leading`, `.trailing`, `.unspecified`) from the local view. UIKit exposes `UITraitCollection.systemTraitsAffectingVerticalBarEdge` for explicit trait registration. These reflect the system's preferred edge, even if no vertical bar is currently visible. For standalone custom bars, use this environment plus local safe areas to choose a suitable layout; it isn't a promise of an occupied toolbar. [SwiftUI edge](https://developer.apple.com/documentation/swiftui/environmentvalues/toolbarverticaledge), [UIKit edge](https://developer.apple.com/documentation/uikit/uitraitcollection/verticalbaredge).

## Item placement and representation

| Intent | SwiftUI | UIKit |
| --- | --- | --- |
| Back / close at the navigation end | Standard back, or `.cancellationAction` | Standard back or `leadingItemGroups` |
| Prominent always-available action | `.topBarPinnedTrailing` | `navigationItem.pinnedTrailingGroup` |
| Ordinary upper/lower actions | Existing top/bottom toolbar placements | Navigation/toolbar item groups |
| Always in the system overflow | `ToolbarOverflowMenu` | `navigationItem.additionalOverflowItems` |

Provide **both a localized title and image** with `Label` or `UIBarButtonItem`. The system chooses icon representations in a vertical bar and titles in the overflow; retain meaningful accessibility labels. Prefer a system back action, customizing its indicator image if needed, rather than replacing navigation behavior. `leadingItemGroups` and `leftItemsSupplementBackButton` must be considered together so custom Close does not accidentally duplicate Back. Group related actions rather than inserting fixed spacers. [Pinned placement](https://developer.apple.com/documentation/swiftui/toolbaritemplacement/topbarpinnedtrailing), [leading groups](https://developer.apple.com/documentation/uikit/uinavigationitem/leadingitemgroups), [pinned group](https://developer.apple.com/documentation/uikit/uinavigationitem/pinnedtrailinggroup).

Text-only items and complex custom views normally stay horizontal. Icons with redundant text can become icon items; meaningful numeric information such as a payable amount shouldn't disappear just to fit a side bar. Don't rotate a segmented control vertically. Tabs or explicit glyph actions may express the same choice better. [Segmented-control Q&A](https://developer.apple.com/forums/thread/847811).

`axisBehavior(.horizontalOnly)` / `UIBarButtonItem.axisBehavior = .horizontalOnly` keeps an item's placement stable when its representation changes, such as a pause glyph becoming a textual resume action. `.verticalPreferred` is an opt-in for a custom view that truly supports the narrow vertical bar and menu representation. It does not make a wide view fit. Apply the modifier to `ToolbarItem` / `ToolbarItemGroup`, not to the Button's content. [Axis docs](https://developer.apple.com/documentation/swiftui/toolbarcontent/axisbehavior(_:)), [UIKit axis](https://developer.apple.com/documentation/uikit/uibarbuttonitem/axisbehavior-swift.property).

## Overflow and compression

Controls compete for space with the status bar and Live Activities. Items normally overflow from the bottom upward. `visibilityPriority(.high/.low/.automatic)` supplies relative importance; prioritize groups first, then items only as necessary. Important Compose/record actions and status badges should survive longer. Pinned placement is for a small number of prominent actions, not every action. Confirm all overflow actions remain functional with the keyboard and large text. [Priority](https://developer.apple.com/documentation/swiftui/toolbarcontent/visibilitypriority(_:)).

Use the system overflow and consolidate an app's redundant ellipsis menu into it. Reserve the ellipsis icon for overflow. UIKit `additionalOverflowItems` is a `UIDeferredMenuElement?` whose provider returns menu elements; SwiftUI `ToolbarOverflowMenu` takes view content. UIKit's existing `menuRepresentation` on an item/group can provide an appropriate overflow representation for a custom control. Do not copy every visible action into overflow yourself—the system manages overflow of ordinary items. [SwiftUI overflow](https://developer.apple.com/documentation/swiftui/toolbaroverflowmenu), [UIKit overflow](https://developer.apple.com/documentation/uikit/uinavigationitem/additionaloverflowitems).

Default compression favors navigation destinations. For a task-centered screen, `toolbarVerticalCompressionBehavior(.prefersToolbarItems)` / `navigationItem.verticalBarCompressionBehavior = .prefersBarItems` preserves tools by minimizing the tab bar first. `.prefersTabBar` preserves destinations by overflowing tools first. This is distinct from item visibility priority and scroll minimization. [HIG compression](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo).

Use `toolbarVerticalBehavior(.disabled)` or override `preferredVerticalBarBehavior` only for a justified stable layout, for example a calculator-like control surface or a sheet with one close action. UIKit can forward through `childForPreferredVerticalBarBehavior` and invalidate with `setNeedsUpdateOfVerticalBarConfiguration()`. Don't toggle the preference repeatedly as incidental state changes; use normal bar visibility when the actual intent is hiding controls. [Behavior docs](https://developer.apple.com/documentation/swiftui/view/toolbarverticalbehavior(_:)), [UIKit behavior](https://developer.apple.com/documentation/uikit/uiviewcontroller/preferredverticalbarbehavior).

## Sidebars and accessories

iPhone apps do **not** automatically opt into a tab sidebar merely because width becomes regular. To offer a sidebar, choose `defaultTabBarPlacement(.sidebar)` with the appropriate adaptable tab style, or `tabBarController.sidebar.preferredPlacement = .sidebar` (iOS 27). Expose nested destinations when sidebar availability is false. The default overlay sidebar layout is recommended; force `.tile` only when the content requires it. Don't add `.mode = .tabBar` to suppress an adaptation the app hasn't opted into. [WWDC26 UIKit, 9:18](https://developer.apple.com/videos/play/wwdc2026/278/?time=558), [staff clarification](https://developer.apple.com/forums/thread/847961).

Use Auto Layout for `UITabAccessory` content and allow the system to change its size. Avoid fixed-width root constraints or assumptions that an accessory is always horizontal. SwiftUI's existing `tabViewBottomAccessory` also needs adaptive content and semantic labels. [Accessory sizing](https://developer.apple.com/forums/thread/847812).

### Related iOS 27 toolbar APIs

The installed SDK spells the scroll API **`toolbarMinimizationBehavior(_:for:)`**, even though the WWDC transcript calls it `toolbarMinimizeBehavior`. Related modifiers are `toolbarMinimizationSafeAreaAdjustment(_:for:)` and `toolbarMinimizationRestoration(_:for:)`. UIKit uses `navigationItem.navigationBarMinimization`. Inspect these symbols' declarations rather than transcribing an older slide. They are broader resizability features, not fold detection. The prominent tab role introduced in iOS 27 is similarly optional, for a distinct task destination such as a cart. [WWDC26 SwiftUI](https://developer.apple.com/videos/play/wwdc2026/269/), [API catalog](api-catalog.md).

UIKit also adds `UIBarButtonItem.isPaddingRemoved` in iOS 27 to remove standard item padding. Keep the default unless a particular custom item needs it; removing padding is not a substitute for a meaningful touch target or making an oversized control fit a vertical bar. Its contract was verified in the SDK header; this is not required for ordinary system items.
