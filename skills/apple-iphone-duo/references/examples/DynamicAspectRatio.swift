import AVFoundation
import CoreMedia

#if !targetEnvironment(macCatalyst)
// Call on the existing serial capture owner, with an already chosen active format.
// Completion communicates the first buffer's timestamp to recording/processing.
@available(iOS 26.0, *)
func changeSupportedAspectRatio(
    camera: AVCaptureDevice,
    ratio: AVCaptureDevice.AspectRatio,
    completion: @escaping @Sendable (CMTime, (any Error)?) -> Void
) throws {
    guard camera.activeFormat.supportedDynamicAspectRatios.contains(ratio) else {
        throw AspectRatioExampleError.unsupported
    }
    try camera.lockForConfiguration()
    defer { camera.unlockForConfiguration() }
    camera.setDynamicAspectRatio(ratio, completionHandler: completion)
}

enum AspectRatioExampleError: Error { case unsupported }
#endif
