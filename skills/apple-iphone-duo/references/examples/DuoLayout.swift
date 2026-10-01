// Original API examples. Type-check with the iOS 27.1 SDK; no app entry point.
import SwiftUI

#if !targetEnvironment(macCatalyst)
@available(iOS 27.1, *)
struct DuoPlayerExample: View {
    // State stays above the arrangement and survives secondary-pane collapse.
    @State private var showsQueue = false
    @State private var isPlaying = false

    var body: some View {
        NavigationStack {
            ArrangementView {
                VStack {
                    Text("Now Playing")
                    Button(isPlaying ? "Pause" : "Play") { isPlaying.toggle() }
                    HingeIndicatorExample()
                }
                .layoutPriority(1)
                .splitArrangementLayoutRatio(0.6)
            } secondary: {
                QueueExample()
            }
            .arrangementViewStyle(.split.axes(.horizontal))
            .navigationTitle("Audio")
            .toolbar {
                // The secondary remains reachable even when the arrangement hides it.
                ToolbarItem(placement: .topBarPinnedTrailing) {
                    Button { showsQueue = true } label: {
                        Label("Up Next", systemImage: "list.bullet")
                    }
                }
                ToolbarOverflowMenu {
                    Button { isPlaying = false } label: {
                        Label("Stop Playback", systemImage: "stop.fill")
                    }
                }
            }
            .sheet(isPresented: $showsQueue) { QueueExample() }
        }
    }
}

@available(iOS 27.1, *)
private struct QueueExample: View {
    var body: some View { Text("Up Next") }
}

@available(iOS 27.1, *)
private struct HingeIndicatorExample: View {
    @State private var openness = 1.0
    var body: some View {
        Image(systemName: "book")
            .scaleEffect(0.8 + 0.2 * openness)
            .accessibilityHidden(true)
            .onHingeChange { _, context in
                guard let hinge = context.hinge,
                      hinge.status == .partiallyOpen else {
                    openness = 1
                    return
                }
                openness = min(1, max(0, hinge.angle.radians / .pi))
            }
    }
}

@available(iOS 27.1, *)
struct RegionDiagnosticsExample: View {
    var body: some View {
        GeometryReader { proxy in
            let activeDivisions = proxy.reservedRegions(kind: .division)
                .filter { $0.isActive && !$0.frame.isEmpty }
            let knownDivisions = proxy.reservedRegions(
                kind: .division, options: .includeInactive)
            Text(verbatim: "Active: \(activeDivisions.count), known: \(knownDivisions.count)")
        }
    }
}

@available(iOS 27.1, *)
struct OverlayControlsExample: View {
    @Environment(\.overlayArrangementZIndex) private var zIndex
    @Environment(\.splitArrangementAxis) private var splitAxis
    @Environment(\.toolbarVerticalEdge) private var verticalEdge
    var body: some View {
        Text(verbatim: "Overlay: \(zIndex), split: \(String(describing: splitAxis)), bar: \(String(describing: verticalEdge))")
    }
}
#endif

// Keep a functional existing layout on older OS versions and Catalyst.
struct PlayerFallbackExample: View {
    var body: some View {
        if #available(iOS 27.1, *) {
            #if !targetEnvironment(macCatalyst)
            DuoPlayerExample()
            #else
            Text("Now Playing")
            #endif
        } else {
            Text("Now Playing")
        }
    }
}
