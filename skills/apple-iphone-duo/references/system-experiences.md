# Adjacent system experiences

Read this reference when the app already owns one of these features. These are supporting considerations, not a requirement to adopt every framework while preparing for Duo.

## Widgets and StandBy

The group labs discuss extra-large 6×4 widgets on the inner display and in StandBy. The existing `WidgetFamily.systemExtraLarge` symbol is not newly introduced in 27.1—it began in iOS 15 for relevant platforms. Its currently published page still describes iPad/macOS/visionOS availability, so don't infer every new iPhone surface, Lock Screen family, widget count, or StandBy arrangement from the enum's existence. Use actual `widgetFamily` and container geometry, declare only families the widget implements, and check the current WidgetKit documentation/runtime for the requested surface. [Day 1, 20:41](https://developer.apple.com/videos/play/meet-with-apple/285/?time=1241), [day 2, 54:09](https://developer.apple.com/videos/play/meet-with-apple/286/?time=3249), [family documentation](https://developer.apple.com/documentation/widgetkit/widgetfamily/systemextralarge).

Preserve legibility, meaningful content density, tinting, and interactivity as the family changes; don't stretch a small widget or couple it to a model-string check. Existing `.systemExtraLargePortrait` is a different platform-oriented family, not an invented Duo pose enum. Exact outer/inner Lock Screen widget limits were not confirmed by the lab panel.

Xcode 27.1 beta's Duo simulator lacks StandBy, and most app extensions cannot run/debug there. Preview ordinary widget views for layout, but test system placement and availability on supported hardware. [Release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_1-release-notes).

## Live Activities

Duo's Dynamic Island expands vertically and competes with toolbar items for the side's space. Keep ActivityKit content adaptable and concise, honor the system's supplied region/context, and test compact/expanded states together with toolbar overflow. Do not create a custom Dynamic Island or hardcode its screen rect. Ordinary app content still uses local safe areas/reserved regions. No new Duo-only ActivityKit family or dedicated display-detection API was verified in the researched sources; don't invent one. [Design session, 0:28](https://developer.apple.com/videos/play/tech-talks/111466/?time=28), [ActivityKit](https://developer.apple.com/documentation/activitykit).

## AlarmKit and tent mode

The glowing alarm demonstration uses a system AlarmKit experience. The lab says apps can receive the system's alarm behavior; it does not expose a general method to render arbitrary content on the inner display while another scene runs outside. Preserve normal AlarmKit authorization, scheduling, presentation, and dismissal contracts. Don't start a camera session or create an unrelated accessory just to keep both displays on. [Day 2, 13:43–14:32](https://developer.apple.com/videos/play/meet-with-apple/286/?time=823), [AlarmKit](https://developer.apple.com/documentation/alarmkit).

## Web pages and WKWebView

Give embedded web content its actual container size and insets; don't pass `UIScreen.main.bounds` as a viewport or mirror one inset onto both sides. Use responsive layout and test viewport resizing, text zoom, keyboard, and safe areas in the actual Safari/WKWebView host.

The day-1 panel mentioned existing foldable web standards, explicitly had no WebKit expert present, and deferred exact support to the SDK. No authoritative Duo-specific Safari posture/viewport-segment support declaration was verified during this research. Don't assert that `navigator.devicePosture`, CSS viewport-segment values, or a native SwiftUI reserved-region query is automatically available to a page. Verify the current official WebKit support, feature-detect any proposed web API, and keep ordinary responsive fallbacks. [Day 1, 38:51](https://developer.apple.com/videos/play/meet-with-apple/285/?time=2331).

## Games and immersive content

Keep the game playable as the device opens/closes, folds, or shares space. Maintain readable text and consistent control sizes; resize the render surface/projection to the actual scene, and preserve game state. Prefer adapting aspect ratio over empty letter/pillar boxes; artwork in unavoidable padding can maintain a complete visual surface. Immersive media/backgrounds may span the full display while essential controls respect obstructions. [Duo HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo).

An intentional `UIRequiresFullScreen` game still needs [discrete resizing](adoption.md) support. Hinge mechanics are optional and need equivalent ordinary controls for essential actions. A game without standard bars still has system safe areas and camera/status occlusions; opting out of a vertical toolbar doesn't remove hardware.
