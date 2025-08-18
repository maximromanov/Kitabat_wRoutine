## PolkaDot Image Reviewer

Python/Tk app for fast image review and sorting, plus packaging to a macOS .app and a SwiftUI native macOS project scaffold.

### Features
- Alphabetical browsing with next/prev (arrow keys, j/k, w/q)
- Zoom slider and shortcuts: `[` and `]` to zoom out/in, `Z` to reset, double-click image to reset
- Toggle hide image: `space` or `h`
- Reveal in Finder/Explorer: `Return` or `0`
- Save filename to TSV and copy to Favorites: `s`
- Move to preset folders with number/symbol keys
- Undo last move: `u`
- Drag-and-drop folder onto the window (if `tkinterdnd2` available)

### Run (Python)
1. Create a venv and install requirements:
   - macOS/Linux:
     ```bash
     python3 -m venv .venv && source .venv/bin/activate
     pip install -r requirements.txt
     ```
2. Start the app:
   ```bash
   python polkadot_image_reviewer.py
   ```

### macOS .app via py2app (wraps the Tk app)
1. On macOS, in a venv with requirements installed:
   ```bash
   cd macos_app
   python py2app_setup.py py2app
   ```
2. The app bundle appears in `dist/PolkaDot Image Reviewer.app`.

### Native macOS SwiftUI app (scaffold)
The `macos-native/` folder contains SwiftUI source files you can drop into an Xcode macOS App project (SwiftUI, Swift). Steps:
1. Open Xcode → Create a new project → macOS App → SwiftUI interface.
2. Name it “PolkaDotImageReviewer”.
3. Replace the generated `App` and `ContentView` with the files from `macos-native/`:
   - `PolkaDotImageReviewerApp.swift`
   - `ContentView.swift`
   - `Presets.swift`
   - `FileOps.swift`
   - `ZoomingImageView.swift`
4. In Signing & Capabilities, ensure you have a valid team or use “Sign to Run Locally”.
5. Build and run. The Swift app supports:
   - Folder selection and alphabetical image browsing
   - Zoom with trackpad pinch or slider; double-click to reset
   - Move current image to preset folders, undo last move
   - Save to Favorites and reveal in Finder

Note: The Swift scaffold assumes your sort root is `../SELECTED/__SORTING` relative to the current working directory. Adjust constants in `Presets.swift` to fit your setup.

