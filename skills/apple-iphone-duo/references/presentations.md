# Sheets, popovers, and dialogs

System presentations already adapt to the display and reserved regions. Keep presentation ownership tied to the current view/scene. Do not find a presenter through the first connected scene or assume a sheet's bounds match the full device.

## Sheet placement

On the inner display, sheets usually use a centered placement and horizontal bars. When partially folded, the system moves them clear of the fold. Leading/center sheet placements retain horizontal controls; a trailing placement can use the vertical bar. Outer-display sheet controls can move vertically as well. A sheet with one close action may justify disabling vertical bars within that presentation. [Design session, 8:36](https://developer.apple.com/videos/play/tech-talks/111466/?time=516), [bars session](https://developer.apple.com/videos/play/tech-talks/111462/).

Use SwiftUI `presentationPlacement(_:)` on the presented content, or UIKit `sheetPresentationController.preferredPlacement` (iOS 27). Inspect `PresentationPlacement` / `UISheetPresentationController.Placement` for the exact options supported by the selected SDK. A placement is a persistent preference, not a list of fallback placements the system chooses between. If an app wants centered while flat and trailing around a division, explicitly compute the preference from the current active reserved region and update the presentation; don't infer it from hinge angle alone. Preserve selection and detents across this change. [SwiftUI placement](https://developer.apple.com/documentation/swiftui/view/presentationplacement(_:)), [UIKit placement](https://developer.apple.com/documentation/uikit/uisheetpresentationcontroller/preferredplacement), [placement Q&A](https://developer.apple.com/forums/thread/847797).

Keep interactive content within the presentation's own safe area. A root display safe area is not the sheet's safe area. System detents and keyboard behavior are preferable to hardcoded full-screen heights.

## Contextual presentation and overflow anchors

Alerts, action sheets, menus, and popovers automatically displace to remain usable around a fold. Keep custom presentations near the originating content; if an element and its menu need to move, preserve their relationship. [Layout session](https://developer.apple.com/videos/play/tech-talks/111463/).

In UIKit, `navigationItem.overflowPresentationSource` is an optional `UIPopoverPresentationControllerSourceItem`. When the overflow button exists, it provides an anchor for a custom popover; otherwise it is `nil`, so provide an appropriate source from the current UI. Never force-unwrap an anchor because the originating action once had a visible bar item. [Overflow source](https://developer.apple.com/documentation/uikit/uinavigationitem/overflowpresentationsource).

In SwiftUI, keep presentation state and modifiers on a stable ancestor rather than only inside a toolbar item that may overflow. The Duo SwiftUI Q&A asks about exact confirmation-dialog anchoring from `ToolbarOverflowMenu` but supplies no confirmed special API. Don't invent a SwiftUI overflow-anchor modifier or promise precise anchoring; exercise the actual system behavior on the selected SDK. [Open question](https://developer.apple.com/forums/thread/847865).
