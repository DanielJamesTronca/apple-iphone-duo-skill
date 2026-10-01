import UIKit
import CoreMotion
import CoreLocation

#if !targetEnvironment(macCatalyst)
@available(iOS 27.1, *)
@MainActor
func makeDuoArrangement(primary: UIViewController,
                        secondary: UIViewController) -> UIArrangementViewController {
    let controller = UIArrangementViewController()
    controller.setViewController(primary, for: .primary)
    controller.setViewController(secondary, for: .secondary)
    var arrangement = UISplitArrangement().axes(.horizontal)
    var properties = arrangement.defaultViewProperties
    properties.layoutPriority = 1
    properties.width.preferred = .fractional(0.6)
    arrangement.setViewProperties(properties, for: .primary)
    controller.updateArrangement(arrangement)
    // The containing UI must provide a route to secondary content when hidden.
    return controller
}

@available(iOS 27.1, *)
@MainActor
final class DuoContentExample: UIViewController {
    private let content = UILabel()
    private var hingeInteraction: UIHingeInteraction?

    override func viewDidLoad() {
        super.viewDidLoad()
        content.text = String(localized: "Content")
        content.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(content)
        NSLayoutConstraint.activate([
            content.leadingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.leadingAnchor),
            content.trailingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.trailingAnchor),
            content.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor),
            content.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor)
        ])
        let interaction = UIHingeInteraction { [weak self] _, update in
            // An optional effect, not the source of layout rectangles.
            self?.content.alpha = update.hinge?.status == .partiallyOpen ? 0.95 : 1
        }
        view.addInteraction(interaction)
        hingeInteraction = interaction
    }

    override func viewDidLayoutSubviews() {
        super.viewDidLayoutSubviews()
        // Query local regions when a custom layout actually needs them.
        let regions = view.reservedRegions(kind: .occlusion)
        _ = regions.filter { $0.isActive }
        _ = traitCollection.verticalBarEdge
    }
}

@available(iOS 27.1, *)
@MainActor
func configureDuoActions(_ controller: UIViewController, save: @escaping () -> Void) {
    let item = UIBarButtonItem(
        title: String(localized: "Save"), image: UIImage(systemName: "checkmark"),
        primaryAction: UIAction { _ in save() })
    item.axisBehavior = .verticalPreferred
    item.visibilityPriority = .high
    controller.navigationItem.pinnedTrailingGroup = UIBarButtonItemGroup(
        barButtonItems: [item], representativeItem: nil)
    controller.navigationItem.verticalBarCompressionBehavior = .prefersBarItems
}
#endif

@available(iOS 27.0, *)
@MainActor
func useLocalSensorCoordinates(view: UIView, motion: CMMotionManager,
                               location: CLLocationManager) {
    motion.deviceMotionBody = view
    location.headingBody = view
}
