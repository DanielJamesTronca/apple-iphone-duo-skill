# Camera capture accessory

## A system-managed outer-display enhancement

Use the iOS 27.1 camera capture accessory for a teleprompter, subject preview, framing cue, countdown, or similar camera task while the main capture UI runs on the inner display. The system decides whether and where it appears. It requires an open device, foreground capture interface, and active capture; availability can disappear when capture stops, the app backgrounds, the device closes, or another registration becomes topmost. Do not depend on the accessory for essential controls. [Registration guide](https://developer.apple.com/documentation/avfoundation/registering-a-camera-capture-accessory-on-iphone-duo).

Current docs allow **minimal touch interaction** on the outer display. This supersedes tentative lab comments about no interaction. It is not an arbitrary second full app UI. There is no documented special entitlement or scene-manifest entry to add for camera accessory registration; the system finds active capture and assigns the accessory scene role. Avoid copied early entitlement speculation. [CameraCaptureAccessory](https://developer.apple.com/documentation/swiftui/cameracaptureaccessory).

## SwiftUI

Attach `.sceneAccessory { CameraCaptureAccessory { ... } }` to the view showing the capture interface, not to the entire app regardless of navigation. The content can capture the same observable model used by the main interface. A `CameraCaptureAccessory(isEnabled: $enabled)` binding offers a user toggle. `.onAvailabilityChange { isAvailable in ... }` reports system availability separately from the toggle.

State that must persist belongs in the shared model, not in accessory-local view state, because accessory views can disappear. Render accessory content as ordinary views for preview/layout checks. The [compile-checked example](examples/CameraAccessory.swift) includes shared observable state, availability, and user enablement; it intentionally doesn't fake an active camera session. [SwiftUI docs](https://developer.apple.com/documentation/swiftui/cameracaptureaccessory).

## UIKit

1. Create `UISceneConfiguration` with an appropriate delegate class.
2. Create `UISceneAccessory.cameraCapture(sceneConfiguration:userInfo:)`, optionally passing the existing shared model as `userInfo`.
3. Call `registerSceneAccessory(_:)` on the capture view controller and strongly retain the resulting `UISceneAccessoryRegistration`.
4. Read observable `isAvailable` while updating the UI (for example in `updateProperties`); set `isEnabled` for the user's toggle. Availability and enablement are different.
5. In the accessory scene delegate, read `connectionOptions.sceneAccessoryUserInfo`, create a `UIWindow(windowScene:)`, and provide content backed by the shared state.
6. Call `unregister()` when the app stops offering that accessory, rather than hiding the main interface's controls and leaving registration behind.

The system-assigned Swift scene role is **`.windowCameraCaptureAccessory`**. Don't set it or create a project-level scene configuration entry for it. Ordinary window scene configuration is a different workflow. Scope registration to the capture controller so navigation away withdraws the enhancement. The topmost registration **of a kind** takes precedence; different accessory kinds don't compete. Retain the shared object yourself—`userInfo` isn't the persistence owner. [Registration guide](https://developer.apple.com/documentation/avfoundation/registering-a-camera-capture-accessory-on-iphone-duo).

## ARKit and other display uses

Apple staff corrected an earlier answer: an active `ARSession` counts as active capture for `CameraCaptureAccessory`. AR world tracking is for the main viewer looking through the device; outer content can help a second person, not duplicate a full independent AR world. AR face tracking uses the inner front camera when open. Don't start a second capture session to satisfy accessory eligibility; it can interrupt ARKit. [Corrected staff answer, including reply history](https://developer.apple.com/forums/thread/847744).

AlarmKit tent-mode glow, StandBy/widgets, and external-display accessories have their own system contracts. Do not use camera capture as a workaround to keep two displays lit for unrelated content. Simulator can validate ordinary accessory view layout, but it cannot validate automatic camera-backed presentation. Verify availability transitions on hardware before shipping.
