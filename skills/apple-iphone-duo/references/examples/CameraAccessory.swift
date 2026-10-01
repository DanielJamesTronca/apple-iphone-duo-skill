import SwiftUI
import Observation

#if !targetEnvironment(macCatalyst)
@available(iOS 27.1, *)
@MainActor @Observable
final class CaptureScriptExample {
    var text = ""
    var isEnabled = true
    var isAvailable = false
}

@available(iOS 27.1, *)
struct CameraAccessoryExample: View {
    @State private var script = CaptureScriptExample()

    var body: some View {
        @Bindable var script = script
        VStack {
            // Replace with the app's real capture preview. This placeholder cannot
            // make an accessory available; an active capture session is required.
            Text("Capture Preview")
            TextEditor(text: $script.text)
            if script.isAvailable {
                Toggle("Show Script on Outer Display", isOn: $script.isEnabled)
            }
        }
        .sceneAccessory {
            CameraCaptureAccessory(isEnabled: $script.isEnabled) {
                Text(script.text)
                    .font(.title)
                    .padding()
            }
            .onAvailabilityChange { script.isAvailable = $0 }
        }
    }
}
#endif
