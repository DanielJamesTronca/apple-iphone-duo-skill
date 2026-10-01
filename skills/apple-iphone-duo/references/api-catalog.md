# API catalog and introduction versions

Checked against the public docs and **Xcode 27.1 beta, build 27A9269**. This is an inventory of APIs relevant to Duo adoption, not every WWDC26 addition. The version below is the **iOS introduction**, not a promise of support on every platform. Runtime device/format capability checks remain necessary. Some SDK interfaces use `anyAppleOS`; inspect platform-specific unavailability and the [Catalyst beta caveat](adoption.md).

## New Duo layout and interaction surface: iOS 27.1

| Swift API | Important contract / reference |
| --- | --- |
| `ReservedRegion` | `id`, `kind`, `frame`, `margins`, `isActive`; [type](https://developer.apple.com/documentation/swiftui/reservedregion) |
| `ReservedRegion.Kind.occlusion`, `.division` | Occlusion and division are distinct; [regions](reserved-regions.md) |
| `ReservedRegion.QueryOptions.includeInactive` | Explicit inactive-region query; [options](https://developer.apple.com/documentation/swiftui/reservedregion/queryoptions) |
| `GeometryProxy.reservedRegions(kind:options:layoutDirectionBehavior:)` | Defaults `[]` and `.mirrors`; [query](https://developer.apple.com/documentation/swiftui/geometryproxy/reservedregions(kind:options:layoutdirectionbehavior:)) |
| `UIView.ReservedRegion`, `.Kind`, `.QueryOptions` | Swift refined types; ObjC `UIViewReservedRegion`; [type](https://developer.apple.com/documentation/uikit/uiview/reservedregion) |
| `UIView.reservedRegions(kind:options:)` | Local UIKit geometry; [query](https://developer.apple.com/documentation/uikit/uiview/reservedregions(kind:options:)) |
| `ArrangementView(primary:secondary:)` | Two related content areas; [type](https://developer.apple.com/documentation/swiftui/arrangementview) |
| `arrangementViewStyle(_:)` | `.automatic`, `.split`, `.overlay`; [styles](https://developer.apple.com/documentation/swiftui/arrangementviewstyle) |
| `AutomaticArrangementViewStyle` | Automatic resolves to split in current guidance; SDK declaration |
| `SplitArrangementViewStyle.axes(_:)` | Restricts supported axes, can collapse; [split](https://developer.apple.com/documentation/swiftui/splitarrangementviewstyle) |
| `OverlayArrangementViewStyle.axes(_:)` | Overlay when flat, split around active division; SDK declaration / [arrangements](arrangements.md) |
| `splitArrangementLayoutRatio(_:)` | Preferred fractional share; [ratio](https://developer.apple.com/documentation/swiftui/view/splitarrangementlayoutratio(_:)) |
| `splitArrangementLayoutRatio(minHorizontal:idealHorizontal:maxHorizontal:minVertical:idealVertical:maxVertical:)` | Separate fractional constraints per axis; SDK declaration |
| `splitArrangementLayoutSize(minWidth:idealWidth:maxWidth:minHeight:idealHeight:maxHeight:)` | Point-based size constraints; [sizes](https://developer.apple.com/documentation/swiftui/view/splitarrangementlayoutsize(minwidth:idealwidth:maxwidth:minheight:idealheight:maxheight:)) |
| `splitArrangementFixedLayoutSize(horizontal:vertical:)` | Intrinsic/fixed child sizing; SDK declaration |
| `EnvironmentValues.splitArrangementAxis` | Optional axis in the arrangement child |
| `overlayArrangementEdge(_:)` | Separate `VerticalEdge?` and `HorizontalEdge?` overloads |
| `EnvironmentValues.overlayArrangementZIndex` | Int in the arrangement child; positive when overlaid |
| `ArrangementViewStyle`, `ArrangementViewStyleConfiguration` | Custom styles, configuration's primary/secondary views; advanced rather than a default custom-layout requirement |
| `UIArrangementViewController` | `setViewController`, `updateArrangement`, `state`, `placement`, `viewController`; [controller](https://developer.apple.com/documentation/uikit/uiarrangementviewcontroller) |
| `UIArrangementViewController.Arrangement`, `.ViewPlacement`, `.ViewState` | Swift protocol/refined value surface; state has `zIndex`, `splitAxis`, `isHidden` |
| `UIViewController.arrangementViewController` | Nearest arrangement ancestor |
| `UISplitArrangement` | `axes`, `defaultViewProperties`, `setViewProperties`; [arrangements](arrangements.md) |
| `UISplitArrangement.Dimension`, `.DimensionRange`, `.ViewProperties` | Automatic/intrinsic/fractional/absolute dimensions; min/preferred/max, width/height/priority |
| `UIOverlayArrangement`, `.ViewProperties` | Axes and directional edge preference |
| `EnvironmentValues.toolbarVerticalEdge` | Optional `HorizontalEdge`; [edge](https://developer.apple.com/documentation/swiftui/environmentvalues/toolbarverticaledge) |
| `UITraitCollection.verticalBarEdge`, `UIVerticalBarEdge` | `.unspecified`, `.leading`, `.trailing`; [trait](https://developer.apple.com/documentation/uikit/uitraitcollection/verticalbaredge) |
| `UITraitCollection.systemTraitsAffectingVerticalBarEdge` | Dependency traits for explicit change registration; SDK declaration |
| `ToolbarContent.axisBehavior(_:)`, `CustomizableToolbarContent.axisBehavior(_:)` | `ToolbarItemAxisBehavior.automatic/.horizontalOnly/.verticalPreferred`; [modifier](https://developer.apple.com/documentation/swiftui/toolbarcontent/axisbehavior(_:)) |
| `UIBarButtonItem.axisBehavior`, `.AxisBehavior` | Equivalent UIKit axis preference; [property](https://developer.apple.com/documentation/uikit/uibarbuttonitem/axisbehavior-swift.property) |
| `toolbarVerticalBehavior(_:)`, `ToolbarVerticalBehavior` | `.automatic`, `.disabled`; [modifier](https://developer.apple.com/documentation/swiftui/view/toolbarverticalbehavior(_:)) |
| `UIViewController.preferredVerticalBarBehavior` | `UIVerticalBarBehavior`, `childForPreferredVerticalBarBehavior`, `setNeedsUpdateOfVerticalBarConfiguration`; [preference](https://developer.apple.com/documentation/uikit/uiviewcontroller/preferredverticalbarbehavior) |
| `toolbarVerticalCompressionBehavior(_:)`, `ToolbarVerticalCompressionBehavior` | `.automatic`, `.prefersToolbarItems`, `.prefersTabBar`; [bars](bars.md) |
| `UINavigationItem.verticalBarCompressionBehavior`, `UIVerticalBarCompressionBehavior` | `.automatic`, `.prefersBarItems`, `.prefersTabBar` |
| `DeviceHinge`, `.Status`, `DeviceHingeContext` | Optional hinge, status, SwiftUI Angle; [hinge](hinge-and-motion.md) |
| `onHingeChange(isEnabled:_:)` | Old/new context callback; [modifier](https://developer.apple.com/documentation/swiftui/view/onhingechange(isenabled:_:)) |
| `UIHinge`, `.Status`, `UIHingeInteraction`, `.Update` | UIKit angle in radians, optional hinge; [interaction](https://developer.apple.com/documentation/uikit/uihingeinteraction) |

### Additional SDK-only layout helpers

These public symbols exist in the checked SDK, but dedicated public documentation endpoints were unavailable during research. Confirm their declarations and behavior in the selected SDK before adopting them; don't invent semantics beyond the signature:

- `ContentMarginGuide.container`.
- `View.contentMargins(for:edges:alignment:)` and `GeometryProxy.contentMargins(for:edges:)`.
- `UIView.LayoutRegion.bar(onEdge:extent:)`, with `UIRectEdge` and `NSDirectionalRectEdge` overloads (one edge per region). Consume it with the existing `layoutGuide(for:)`, `edgeInsets(for:)`, or `directionalEdgeInsets(for:)` API. A [reported bar-guide offset issue](https://developer.apple.com/forums/thread/847784) is an unresolved developer report, not a verified fixed workaround. Validate resulting frames in the actual hierarchy.

## New capture/display support: iOS 27.1

| API | Contract |
| --- | --- |
| `AVCaptureDevice.DeviceType.builtInOuterUltraWideCamera` | Physical outer camera, DiscoverySession only |
| `AVCaptureDevice.DeviceType.builtInInnerUltraWideCamera` | Physical inner camera, DiscoverySession only |
| `AVCaptureDeviceDirectionCoordinator` (AVKit) | `init(view:deviceTypes:changeHandler:)`, `deviceDirections`; [guide](https://developer.apple.com/documentation/avkit/choosing-a-camera-by-the-direction-it-faces) |
| `AVCaptureDeviceDirectionMap` (AVKit) | Forward/backward descriptor arrays; sendable |
| `AVCaptureDeviceDescriptor` (AVKit) | `uniqueID`, `position`, `deviceType`, `mediaTypes`, `localizedName`; sendable |
| `CameraCaptureAccessory` | Content and `isEnabled` binding initializers; iOS-only surface, Catalyst unavailable; [SwiftUI](https://developer.apple.com/documentation/swiftui/cameracaptureaccessory) |
| `UISceneAccessory.cameraCapture(sceneConfiguration:)`, `...(sceneConfiguration:userInfo:)` | UIKit factory for capture content; [registration](https://developer.apple.com/documentation/avfoundation/registering-a-camera-capture-accessory-on-iphone-duo) |
| `UISceneSession.Role.windowCameraCaptureAccessory` | System-assigned accessory scene role; don't set it |

Base scene accessory registration, `.sceneAccessory`, `SceneAccessoryContent`, `.onAvailabilityChange`, `UISceneAccessoryRegistration`, `UIViewController.registerSceneAccessory(_:)`, `UIViewController.unregisterSceneAccessory(_:)`, and `sceneAccessoryUserInfo` were introduced in **iOS 27.0**; the camera-specific kind is **27.1**. These aren't ordinary multi-window APIs. Unregister through the owning view controller, not the registration object.

## Related iOS 27 features used by Duo apps

| API | iOS introduction / caveat |
| --- | --- |
| `ToolbarContent.visibilityPriority(_:)`, `ToolbarItemVisibilityPriority` | 27.0; `.automatic/.low/.high`, `init(higherThan:)`, `init(lowerThan:)`; macOS low/high began 26.1 |
| `ToolbarOverflowMenu` | 27.0; [overflow](https://developer.apple.com/documentation/swiftui/toolbaroverflowmenu) |
| `ToolbarItemPlacement.topBarPinnedTrailing` | 27.0 |
| `UIBarButtonItem.visibilityPriority`, `UIBarButtonItemVisibilityPriority` | 27.0; relative priority constructors available |
| `UIBarButtonItem.isPaddingRemoved` | 27.0; removes standard item padding, defaults false; preserve touch target |
| `toolbarMinimizationBehavior(_:for:)` | 27.0; exact SDK spelling; [modifier](https://developer.apple.com/documentation/swiftui/view/toolbarminimizationbehavior(_:for:)) |
| `toolbarMinimizationSafeAreaAdjustment(_:for:)` | 27.0; [adjustment](https://developer.apple.com/documentation/swiftui/view/toolbarminimizationsafeareaadjustment(_:for:)) |
| `toolbarMinimizationRestoration(_:for:)` | 27.0; [restoration](https://developer.apple.com/documentation/swiftui/view/toolbarminimizationrestoration(_:for:)) |
| `UINavigationItem.navigationBarMinimization`, `UIBarMinimization` | 27.0; configure system minimization rather than a custom scroll animator |
| `defaultTabBarPlacement(_:)` / `UITabBarController.Sidebar.preferredPlacement` | 27.0; sidebar support on phone is opt-in |
| Prominent SwiftUI tab role | 27.0; distinct task destination, not Duo-only navigation |
| `presentationPlacement(_:)`, `PresentationPlacement` | 27.0; `.automatic/.center/.leading/.trailing`; sheet preference |
| `UISheetPresentationController.preferredPlacement`, `.Placement` | 27.0; leading/trailing cases have additional availability constraints—inspect SDK |
| `CMMotionManager.deviceMotionBody`, `CMBodyIdentifiable` | 27.0; view-referenced motion; [motion](https://developer.apple.com/documentation/coremotion/cmmotionmanager/devicemotionbody) |
| `CLLocationManager.headingBody`, `CLBodyIdentifiable` | 27.0; replaces headingOrientation; [heading](https://developer.apple.com/documentation/corelocation/cllocationmanager/headingbody) |

## Existing APIs often mistaken for new Duo APIs

| API | iOS introduction / purpose |
| --- | --- |
| `UINavigationItem.leadingItemGroups`, `.pinnedTrailingGroup`, `.additionalOverflowItems`, `.overflowPresentationSource` | **16.0**; adapted by the 27.1 system vertical bar. `additionalOverflowItems` is a `UIDeferredMenuElement?`, not an array |
| `registerForTraitChanges` and trait types | **17.0**; explicit cached-trait invalidation |
| `AVCaptureDevice.RotationCoordinator` | **17.0**; preview/capture rotation |
| `safeAreaBar`, `backgroundExtensionEffect`, `UIBackgroundExtensionView`, concentric corner/layout-region helpers | **26.0**; useful for adaptive margins and backgrounds |
| `UIView.layoutGuide(for:)`, `edgeInsets(for:)`, `directionalEdgeInsets(for:)` | **26.0**; region consumption; the bar-region constructors are 27.1 |
| `tabViewBottomAccessory` | **26.0**, further overloads 26.1; adaptive accessory content |
| `AVCaptureDevice.AspectRatio`, `supportedDynamicAspectRatios`, `dynamicAspectRatio`, `setDynamicAspectRatio` | **26.0**; read-only property, locked setter with completion timestamp |
| `AVCaptureSmartFramingMonitor`, supported/recommended framings | **26.0**; photo framing recommendations on supported formats |
| `AVCapturePhotoOutput.isCameraSensorOrientationCompensationEnabled` | **26.0**; legacy processed-photo sensor compensation |
| `.lowLatency` video stabilization | **26.0**; capability check required |
| `WidgetFamily.systemExtraLarge` | **15.0**; newly discussed Duo contexts don't make the enum new |

For exact Objective-C declarations and cross-platform gates, use the installed framework headers. For behavior, follow the corresponding reference and current official docs. Prefer a supported existing API over inventing a Duo-specific equivalent.
