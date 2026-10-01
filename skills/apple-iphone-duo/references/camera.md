# Cameras, direction, and capture continuity

Contents: device selection; direction coordinator; capture ownership; mirroring/rotation; aspect ratio and framing; recording gaps; MultiCam and Vision.

## Choose the least specialized selection strategy

| Requirement | Approach |
| --- | --- |
| A normal selfie/call camera that follows the active display | Discover `.front` with existing `.builtInWideAngleCamera` / `.builtInUltraWideCamera` types; Duo can supply its virtual front camera |
| Pick a physical camera or expose explicit choices | New `.builtInOuterUltraWideCamera` / `.builtInInnerUltraWideCamera` and a direction coordinator |
| Rear/front directions relative to a particular preview display | `AVCaptureDeviceDirectionCoordinator` with that preview's UIView |
| Need to inspect actual physical lens used by a virtual device | `isVirtualDevice` and `activePrimaryConstituent`, after capture begins |

There is no new public `.builtInVirtualFrontCamera` type. The virtual front device manages handoff between the outer and inner cameras. Use `DiscoverySession` for new physical Duo types; don't assume `AVCaptureDevice.default` finds them. Treat no device, permission denial, interruption, backgrounding, and inner-camera unavailability while closed as normal states. [Camera session](https://developer.apple.com/videos/play/tech-talks/111465/), [physical device declarations](https://developer.apple.com/documentation/avfoundation/avcapturedevice/devicetype-swift.struct).

Published hardware maxima differ: outer capture supports up to 4K/120, inner up to 1080p/60; the virtual front offers their common 1080p/60 capability and does not provide depth. These are not universal selected-format guarantees. Query formats, frame-rate ranges, output support, and depth support at runtime. Don't extrapolate outer-camera quality to the inner camera or make a virtual front inherit all physical capabilities. [Camera session, 1:34](https://developer.apple.com/videos/play/tech-talks/111465/?time=94).

## Direction coordinator, iOS 27.1

`AVCaptureDeviceDirectionCoordinator`, `AVCaptureDeviceDirectionMap`, and `AVCaptureDeviceDescriptor` are declared by **AVKit**, with the actual devices in AVFoundation. Import both when generating coordinator code. A device's static `.position` is not the direction it faces relative to the active display on Duo. A rear camera may face the person viewing the outer display. Hinge angle alone doesn't resolve this. [Direction guide](https://developer.apple.com/documentation/avkit/choosing-a-camera-by-the-direction-it-faces).

Initialize `AVCaptureDeviceDirectionCoordinator(view:deviceTypes:changeHandler:)` on the main actor and retain it for the preview's lifetime. The handler runs on the main queue and supplies a sendable map with `forwardFacingDeviceDescriptors` and `backwardFacingDeviceDescriptors`. `deviceDirections` is empty until its first callback; don't interpret that initial snapshot as permanent absence. Its physical-camera filter excludes virtual devices and unsupported external/Continuity/Desk View types. For multiple previews on different displays, each relevant view needs its own directional context. [Coordinator](https://developer.apple.com/documentation/avkit/avcapturedevicedirectioncoordinator).

Pass a sendable descriptor or its `uniqueID` to the serialized capture owner, resolve the device there, and handle a missing/stale device. Preserve the current selection if it still satisfies the requested direction/capabilities. Don't choose a new arbitrary first camera on every callback. Check the selected descriptor against the current generation when asynchronous work completes.

See [CameraDirection.swift](examples/CameraDirection.swift): it passes descriptors through an actor boundary and rejects stale selections. Integrate it with the app's existing capture owner rather than creating a competing session for each view.

## Serialize the capture pipeline

Keep session configuration and `startRunning` / `stopRunning` off the main actor, on a dedicated serial capture queue or appropriately serialized actor. Plain actors are reentrant across `await`; don't assume two asynchronous configuration requests can't interleave. Device locking, begin/commit configuration, format changes, and input replacement need a coherent transaction. Preserve a working input if a replacement cannot be added, balance every configuration/lock, and surface an actual error/fallback. Don't block the UI in the coordinator callback. [Direction guide](https://developer.apple.com/documentation/avkit/choosing-a-camera-by-the-direction-it-faces).

Reconfigure dependent rotation, mirroring, and outputs when a connection/device changes. Scene movement is not a reason to reconstruct unrelated UI state or the entire capture pipeline.

## Mirroring and rotation

Mirror a preview for the forward-facing direction and normally don't mirror a backward-facing preview, regardless of static front/back `.position`. Check `isVideoMirroringSupported`. Set `automaticallyAdjustsVideoMirroring = false` **before** assigning `isVideoMirrored`; assigning while automatic adjustment is enabled can throw an exception. Reapply a manual policy to replacement connections. Preview mirroring and saved-media policy can differ intentionally. [Direction guide](https://developer.apple.com/documentation/avkit/choosing-a-camera-by-the-direction-it-faces), [mirroring contract](https://developer.apple.com/documentation/avfoundation/avcaptureconnection/isvideomirrored).

Use `AVCaptureDevice.RotationCoordinator` (iOS 17, not a new Duo API) with the selected camera and preview layer. Recreate the coordinator for camera changes; apply the appropriate preview/capture angles with supported-connection checks. Follow updated rotation data across display changes. Fixed historical front-sensor mounting assumptions can produce sideways photos.

`AVCapturePhotoOutput.isCameraSensorOrientationCompensationEnabled` (iOS 26) preserves older processed-photo orientation by physically rotating buffers and updating metadata. RAW/ProRAW have different treatment. Disable compensation only after adopting a correct rotation pipeline and verifying output orientation; this can improve performance, but blindly disabling it breaks legacy apps. [WWDC26 Center Stage, 9:24](https://developer.apple.com/videos/play/wwdc2026/341/?time=564).

## Square-sensor aspect ratio and smart framing

These APIs started in iOS 26; availability on a format/camera is separate from OS availability. Check the physical or virtual camera's actual format. Outer capabilities don't imply inner/virtual capabilities. [WWDC26 Center Stage](https://developer.apple.com/videos/play/wwdc2026/341/).

- `activeFormat.supportedDynamicAspectRatios` lists allowed Swift `AVCaptureDevice.AspectRatio` values (Objective-C `AVCaptureAspectRatio`). Use supported square formats; not every resolution supports every ratio.
- `dynamicAspectRatio` is **read-only**. Change it with `setDynamicAspectRatio(_:completionHandler:)` or its async Swift form **while locked for configuration**. Its completion timestamp identifies the first buffer using the new ratio. Never generate `camera.dynamicAspectRatio = ...`.
- `AVCaptureSmartFramingMonitor` recommends an aspect ratio and zoom factor for supported photo formats. Configure `enabledFramings` under the device lock, observe `recommendedFraming`, apply ratio before zoom, and retain/invalidate observations. Stop monitoring when the feature is disabled.
- `isCenterStageSupported` is a format capability. `centerStageControlMode` and `isCenterStageEnabled` operate per process, with cooperative/app/user control policy; don't override user control without the intended app policy.
- Query stabilization support before selecting face-aware cinematic modes or `.lowLatency` for a call. Don't promise every Duo camera supports the same modes.

The [aspect-ratio example](examples/DynamicAspectRatio.swift) uses the completion form to avoid holding a device lock across an actor-reentrant `await`. Integrate completion timestamps with output processing; it is an API demonstration, not a complete format-selection policy. [Setter docs](https://developer.apple.com/documentation/avfoundation/avcapturedevice/setdynamicaspectratio(_:completionhandler:)).

## Recording and handoff discontinuities

Virtual-front handoffs can pause frames and change intrinsics/distortion metadata. Apple confirms there need not be an explicit dropped-frame reason or session interruption; video-data timestamps can have a gap. Measure timestamps and track `activePrimaryConstituent` rather than relying exclusively on notifications. Refresh geometry-dependent processing when the camera changes; temporal Vision/tracking algorithms may need to reset. A frozen/covered preview should end when new frames arrive, not after a guessed universal latency. [Frame continuity Q&A](https://developer.apple.com/forums/thread/847766).

QuickTime tracks require consistent sample dimensions. Changing dynamic aspect ratio during `AVCaptureMovieFileOutput` recording can stop recording automatically. For `AVCaptureVideoDataOutput` + `AVAssetWriter`, use the aspect-ratio completion timestamp to finish the old-dimension segment and begin a suitable new one. Don't silently append new-sized buffers to the existing track or promise seamless output merely because preview handoff is automatic. [WWDC26 Center Stage, 11:53](https://developer.apple.com/videos/play/wwdc2026/341/?time=713).

## MultiCam, ARKit, and sustained analysis

Use `DiscoverySession.supportedMultiCamDeviceSets`, session capability checks, and hardware/system-pressure costs for simultaneous physical cameras. Duo can support three-camera combinations, but not every combination or requested format is guaranteed. A virtual rear and a front camera are not a single virtual device supporting constituent photo delivery. [MultiCam Q&A](https://developer.apple.com/forums/thread/847763), [constituent delivery Q&A](https://developer.apple.com/forums/thread/847781).

An inner-camera feed can support sustained 2D Vision/body analysis within its native formats. Design for the real low-light/noise/diffraction characteristics and inference cost; use `alwaysDiscardsLateVideoFrames` where low-latency analysis should discard rather than backlog frames. Measure thermal/pressure behavior and treat dropped analysis work separately from capture continuity. Don't promise medical/tracking accuracy from hardware specs. [Sustained analysis Q&A](https://developer.apple.com/forums/thread/847809).

For ARKit, use its existing session; a second AVCaptureSession can steal the camera. A later Apple staff correction confirms an active `ARSession` qualifies for a camera accessory. That does not create two independent AR experiences. See [camera accessory](camera-accessory.md). Detailed AR world-tracking continuity across fold transitions remains unconfirmed in the accessible Q&A; test rather than guarantee it.
