#!/bin/bash
set -euo pipefail
duo_repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
duo_ios_sdk="$(xcrun --sdk iphoneos --show-sdk-path)"
duo_mac_sdk="$(xcrun --sdk macosx --show-sdk-path)"
duo_examples=("$duo_repo_root"/skills/apple-iphone-duo/references/examples/*.swift)

xcrun swiftc -typecheck -swift-version 6 -sdk "$duo_ios_sdk" \
  -target arm64-apple-ios17.0 "${duo_examples[@]}"

xcrun swiftc -typecheck -swift-version 6 -sdk "$duo_mac_sdk" \
  -F "$duo_mac_sdk/System/iOSSupport/System/Library/Frameworks" \
  -I "$duo_mac_sdk/System/iOSSupport/usr/include" \
  -target arm64-apple-ios17.0-macabi "${duo_examples[@]}"

echo "Swift 6 examples passed for iOS 17 and Mac Catalyst 17 using the selected SDKs."
