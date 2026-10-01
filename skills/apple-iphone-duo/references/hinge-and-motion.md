# Hinge interactions and sensor coordinates

## Geometry and physical state answer different questions

For unobstructed placement, use [reserved regions](reserved-regions.md) or an arrangement. For an optional game mechanic, sound, scrub action, or visual response to folding, observe the hinge. Neither is a camera-direction API. Do not derive feature availability, screen identity, or a giant pose-specific UI hierarchy from an angle threshold. [Scenes session](https://developer.apple.com/videos/play/tech-talks/111464/), [HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo).

## SwiftUI, iOS 27.1

`onHingeChange(isEnabled:_:)` receives old and new `DeviceHingeContext` values. Each context's optional `hinge` contains a `DeviceHinge`, with:

- `status`: `.closed`, `.partiallyOpen`, or `.fullyOpen`.
- `angle`: a SwiftUI `Angle`; use `.radians` or `.degrees` explicitly rather than guessing units.

A `nil` hinge means the view's current hierarchy doesn't provide one. Handle it and reset an effect that no longer applies. Use semantic status for coarse interactions; don't assume a fully open angle is an exact numeric constant. Disable observation with `isEnabled` when the feature doesn't need it. [Modifier](https://developer.apple.com/documentation/swiftui/view/onhingechange(isenabled:_:)).

Keep frequent angle updates near the small view/effect that consumes them; publishing every update through a broad root model can invalidate the whole app. Clamp input for the interaction's domain, respect Reduce Motion, and provide an ordinary control for essential actions on devices without a hinge. Do not rebuild view identity for every angle. The [SwiftUI example](examples/DuoLayout.swift) demonstrates a small isolated indicator.

## UIKit

Attach `UIHingeInteraction` to the relevant view. Its escaping handler receives the interaction and `UIHingeInteraction.Update`; `update.hinge` is optional, including when the interaction leaves a hierarchy that provides updates. Capture the controller weakly to avoid a view → interaction → handler → controller cycle. `UIHinge.angle` is **radians**, and `UIHinge.Status` also has `.unknown`; use `@unknown default` as appropriate. [Interaction](https://developer.apple.com/documentation/uikit/uihingeinteraction).

`isEnabled = false` stops updates; they are not queued. Re-enabling supplies current state when available. Rate, precision, and thresholds are system policy—do not promise a high-rate sensor or use it as a timing clock. Prefer `.status` when angle precision isn't needed. `UIHinge` cannot be directly constructed as a fake device state; test your own interaction mapping with plain values if it merits tests, and verify hardware behavior separately.

## Motion and location in resizable environments

In iOS 27, UIView conforms to CoreMotion's `CMBodyIdentifiable` and CoreLocation's `CLBodyIdentifiable`. Set `CMMotionManager.deviceMotionBody` and `CLLocationManager.headingBody` to the view that visualizes the readings. A compass/map's owning view is a better reference than a global interface-orientation transform. `headingOrientation` is deprecated in favor of `headingBody`. These are sensor coordinate APIs, not a substitute for reserved regions or a Duo hinge sensor. Preserve physical-device orientation use when it is actually needed for sensors. [Motion body](https://developer.apple.com/documentation/coremotion/cmmotionmanager/devicemotionbody), [heading body](https://developer.apple.com/documentation/corelocation/cllocationmanager/headingbody).

A nil motion body keeps the hardware coordinate frame. Setting a body transforms orientation, rotation rate, gravity, and acceleration into the view's coordinates as it changes orientation/display. Separate managers can track different views independently; avoid applying an old manual orientation rotation again. Use the [UIKit example](examples/DuoUIKit.swift) for both assignments, and preserve normal authorization and manager lifecycle. [WWDC26 UIKit, 7:55](https://developer.apple.com/videos/play/wwdc2026/278/?time=475).
