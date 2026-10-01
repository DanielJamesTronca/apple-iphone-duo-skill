# Forward evaluation — 2026-10-01

One independent agent used the completed skill with an isolated, synthetic SwiftUI/UIKit app extract. It received the user request and raw source/configuration only; it was not given expected findings or author conclusions. This was a review, not a runnable full app or hardware test.

The request preserved an iOS 17 minimum, iPhone-only distribution, existing single-window scene delegate, landscape policy, and deliberate discrete resizing. The source included cached global screen sizing, asymmetric manual insets, orientation-dependent visibility, an arrangement with an editor in its secondary child, navigation identity tied to size class, and an analytics idiom check.

The review identified four behavior issues and supplied focused fixes: stale/local sizing and safe-area handling, physical-orientation hiding, loss of access to secondary editing during collapse, and navigation-subtree recreation. It preserved the full-screen/orientation/device-family/window choices and the legitimate analytics check. It correctly distinguished state owned above an identity modifier from state potentially destroyed inside its subtree; it did not assert an unobserved draft reset.

The evaluating agent successfully type-checked the extract using Swift 6, the iPhoneSimulator27.1 SDK, and an iOS 17 target, and validated the plist. It reported the limits of the missing project/renderer and left device interaction checks unclaimed. The audit helper's five candidates were interpreted contextually rather than treated as five defects.

No substantive skill usability issue blocked the review. The portable installed-skill compile command was clarified afterward because the repository's maintenance compile script is outside the installed skill directory.

The other scenarios in `skill_evals.json` are maintained evaluation inputs; they are not claimed as executed independent trials. CI verifies the audit CLI and package contracts. Camera, rendered layout, thermal behavior, and actual accessory presentation remain app/device validation responsibilities.

## Publication audit — 2026-10-01, version 1.0.1

Reviewed packaging and discovery against current OpenAI skill guidance, the Agent Skills specification, and OpenAI's portable plugin guidance. Shortened the discovery description, clarified standalone installation and host-specific invocation, added the portable root manifest and native Codex marketplace, and supplied Claude marketplace descriptive metadata.

An API spot-check against Apple's current capture-accessory guide and Xcode 27.1 `UIViewController.h` found incorrect cleanup guidance. Replaced `registration.unregister()` with the owning controller's `unregisterSceneAccessory(_:)`, and added a type-checked original UIKit example.

Validation completed:

- All nine audit/package CLI tests pass. New regression cases first failed against the previous validator for version drift, unresolved marketplace sources, missing install policy, and links outside the installed skill.
- Root `plugin.json` passes the official Agent Plugins 1.0.0 JSON schema; skill frontmatter passes Codex's bundled skill validator, and UI metadata parses as YAML.
- Claude plugin and marketplace manifests pass `claude plugin validate --strict` without warnings.
- The Skills CLI discovers exactly one skill with the updated description.
- Codex registers the local marketplace and installs version 1.0.1 in a disposable configuration. The installed copy retains scripts, references, examples, and UI metadata; the normal user configuration was not changed.
- Swift 6 examples type-check with Xcode 27.1 beta (27A9269) for iOS 17 and Mac Catalyst 17, including the corrected cleanup call.

This audit did not rerun the independent behavioral scenarios, re-research every Apple source, test rendered UI or camera hardware, or publish the local changes to GitHub or a public plugin directory.
