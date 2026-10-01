import AVFoundation
import AVKit
import UIKit

#if !targetEnvironment(macCatalyst)
@available(iOS 27.1, *)
actor DirectionSelectionExample {
    // Keep this session actor-owned. Integrate into the app's existing capture owner.
    private let session = AVCaptureSession()
    private var input: AVCaptureDeviceInput?
    private var lastGeneration: UInt64 = 0

    func choose(_ descriptor: AVCaptureDeviceDescriptor?, generation: UInt64) throws -> String? {
        // Main-actor Tasks can arrive at this actor in a different order.
        guard generation > lastGeneration else { return input?.device.uniqueID }
        lastGeneration = generation
        guard let descriptor else { return nil }
        if input?.device.uniqueID == descriptor.uniqueID { return descriptor.uniqueID }
        guard let device = AVCaptureDevice(uniqueID: descriptor.uniqueID) else {
            throw DirectionSelectionError.unavailable
        }
        let replacement = try AVCaptureDeviceInput(device: device)

        // No await inside this configuration transaction.
        session.beginConfiguration()
        defer { session.commitConfiguration() }
        let previous = input
        if let previous { session.removeInput(previous) }
        if session.canAddInput(replacement) {
            session.addInput(replacement)
            input = replacement
            return descriptor.uniqueID
        } else {
            if let previous, session.canAddInput(previous) {
                session.addInput(previous)
                input = previous
            } else {
                input = nil
            }
            throw DirectionSelectionError.unsupportedInput
        }
    }
}

private enum DirectionSelectionError: Error { case unavailable, unsupportedInput }

@available(iOS 27.1, *)
@MainActor
final class DirectionPreviewExample: UIView {
    private let capture: DirectionSelectionExample
    private var coordinator: AVCaptureDeviceDirectionCoordinator?
    private var generation: UInt64 = 0
    private(set) var selectionError: String?
    private(set) var hasForwardCamera = false
    private var selectedID: String?

    init(capture: DirectionSelectionExample) {
        self.capture = capture
        super.init(frame: .zero)
        coordinator = AVCaptureDeviceDirectionCoordinator(
            view: self,
            deviceTypes: [.builtInWideAngleCamera, .builtInOuterUltraWideCamera,
                          .builtInInnerUltraWideCamera]) { [weak self] directions in
                guard let self else { return }
                let candidates = directions.forwardFacingDeviceDescriptors
                // Preserve an eligible selection; product policy chooses among others.
                let descriptor = candidates.first { $0.uniqueID == self.selectedID }
                    ?? candidates.first
                self.hasForwardCamera = descriptor != nil
                self.generation += 1
                let request = self.generation
                Task {
                    do {
                        let selected = try await self.capture.choose(descriptor, generation: request)
                        if self.generation == request {
                            self.selectedID = selected
                            self.selectionError = nil
                        }
                    } catch {
                        if self.generation == request {
                            self.selectionError = error.localizedDescription
                        }
                    }
                }
            }
    }

    required init?(coder: NSCoder) { nil }
}

@MainActor
func applyDirectionalPreviewMirroring(_ connection: AVCaptureConnection,
                                      isForwardFacing: Bool) {
    guard connection.isVideoMirroringSupported else { return }
    connection.automaticallyAdjustsVideoMirroring = false
    connection.isVideoMirrored = isForwardFacing
}
#endif
