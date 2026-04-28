# SmartDrone Mobile App (iOS & Android)

Built with Capacitor — wraps the live SmartDrone web app into a native shell.

## Prerequisites

### For iOS (requires a Mac):
- Xcode 15+ installed
- CocoaPods: `sudo gem install cocoapods`
- Apple Developer account (free works for simulator, paid for real device)

### For Android:
- Android Studio installed
- Android SDK 33+

---

## Setup (one time)

```bash
cd drone_store/mobile
npm install
```

Update `capacitor.config.ts` — set `server.url` to your actual Render URL:
```ts
server: {
  url: 'https://YOUR-APP.onrender.com',
}
```

---

## Build & Open iOS (on Mac)

```bash
# Sync web assets
npx cap sync ios

# Install CocoaPods dependencies
cd ios/App && pod install && cd ../..

# Open in Xcode
npx cap open ios
```

In Xcode:
1. Select your target device or simulator
2. Set your Team in Signing & Capabilities
3. Press ▶ Run

---

## Build & Open Android

```bash
npx cap sync android
npx cap open android
```

In Android Studio:
1. Wait for Gradle sync
2. Select device/emulator
3. Press ▶ Run

---

## Update after code changes

```bash
npx cap sync
```

---

## App details
- App ID: `com.smartdrone.app`
- App Name: SmartDrone
- Background: `#0a0608` (dark wine)
- Splash color: `#0a0608`
- Status bar: Dark style with gold spinner
