# iOS Vision App Setup Guide

This folder contains the Swift source code for the "Sheldon Eyes" app. Since Xcode projects are complex folders, you need to create the project yourself and drag these files in.

## 1. Create Xcode Project
1.  Open **Xcode**.
2.  Select **Create a new Xcode project**.
3.  Choose **iOS** -> **App**.
4.  **Options**:
    *   Product Name: `SheldonVision`
    *   Interface: **Storyboard**
    *   Language: **Swift**
5.  Save it anywhere (e.g., Desktop).

## 2. Implement Code
1.  **Delete** the default `ViewController.swift` in your new project.
2.  **Drag & Drop** the following files from this folder into your Xcode project (checking "Copy items if needed"):
    *   `CameraManager.swift`
    *   `ESP32Manager.swift`
    *   `ViewController.swift`
    *   `SheldonAudioManager.swift` (New!)

## 3. Permissions & Info.plist (Critical)
You must configure `Info.plist` or the app will fail.

1.  **Camera Access**:
    *   Right-click in Info.plist > **Add Row**.
    *   Key: **Privacy - Camera Usage Description**
    *   Value: `"We need camera access to detect humans and obstacles."`

2.  **Allow HTTP (Local Network)**:
    *   Right-click > **Add Row**.
    *   Key: **App Transport Security Settings** (Type: Dictionary).
    *   Click the arrow (v) to expand it.
    *   Click (+) inside it to add a sub-row.
    *   Key: **Allow Arbitrary Loads** (Type: Boolean).
    *   Value: **YES** (True).


## 4. Wiring the UI (Storyboard)
Since we are using `ViewController.swift` which builds the UI in code, you just need to make sure the Storyboard points to it.
1.  Open `Msain.storyboard`.
2.  Click the white View Controller interface.
3.  In the right sidebar (Identity Inspector), make sure **Class** is set to `ViewController`.
4.  That's it! The code handles the labels and buttons.

## 5. Run it
1.  Connect your iPhone via USB.
2.  Select your iPhone as the build target (Top bar).
3.  Press **Cmd + R** (Run).

*Note: The app will look black until you accept Camera permissions.*
