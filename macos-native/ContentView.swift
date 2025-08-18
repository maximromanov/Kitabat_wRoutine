import SwiftUI

struct ContentView: View {
	@State private var baseFolder: String = FileManager.default.homeDirectoryForCurrentUser.path
	@State private var images: [String] = []
	@State private var index: Int = 0
	@State private var zoom: CGFloat = 1.0
	@State private var undoStack: [(from: URL, to: URL)] = []

	var currentImagePath: String? {
		guard images.indices.contains(index) else { return nil }
		return (baseFolder as NSString).appendingPathComponent(images[index])
	}

	var body: some View {
		VStack(spacing: 8) {
			// Presets row
			ScrollView(.horizontal, showsIndicators: false) {
				HStack { ForEach(defaultPresets) { p in Button("\(p.label)") { switchToPreset(p) } } }
			}

			Group {
				if let path = currentImagePath, let nsImg = NSImage(contentsOfFile: path) {
					ZoomingImageView(image: nsImg, zoom: $zoom)
						.background(Color.white)
						.frame(maxWidth: .infinity, maxHeight: .infinity)
				} else {
					Text("No images").frame(maxWidth: .infinity, maxHeight: .infinity)
				}
			}

			HStack(spacing: 8) {
				Button("Choose Folder") { pickFolder() }
				Button("Reveal") { reveal() }
				Button("Save ⭐") { saveStar() }
				Slider(value: $zoom, in: 0.25...4.0) { Text("Zoom") }.frame(width: 200)
				Spacer()
				Text(baseFolder).font(.system(size: 12, weight: .regular, design: .monospaced))
			}
			.padding(.horizontal)

			HStack {
				Text(statusLeft).font(.system(size: 12, weight: .regular, design: .monospaced))
				Spacer()
				Text(statusRight).font(.system(size: 12, weight: .regular, design: .monospaced))
			}
			.padding(.horizontal)
		}
		.onAppear {
			ensurePresetFolders()
			reloadImages()
		}
		.keyboardShortcutHandlers(
			next: { next() }, prev: { prev() },
			zoomIn: { zoom = min(zoom + 0.1, 4.0) }, zoomOut: { zoom = max(zoom - 0.1, 0.25) },
			resetZoom: { zoom = 1.0 }, undo: undoLast
		)
	}

	var statusLeft: String {
		images.isEmpty ? "No images" : "\(index + 1) of \(images.count) | Alphabetical"
	}

	var statusRight: String {
		guard let path = currentImagePath, let img = NSImage(contentsOfFile: path) else { return "" }
		let dims = "\(Int(img.size.width))×\(Int(img.size.height))"
		let sizeMB = (try? FileManager.default.attributesOfItem(atPath: path)[.size] as? NSNumber)?.doubleValue ?? 0
		return "\(dims) | \(String(format: "%.1f", sizeMB / (1024*1024)))MB | Zoom: \(String(format: "%.2f", zoom))x"
	}

	func pickFolder() {
		let panel = NSOpenPanel()
		panel.canChooseDirectories = true
		panel.canChooseFiles = false
		panel.allowsMultipleSelection = false
		if panel.runModal() == .OK, let url = panel.url {
			baseFolder = url.path
			reloadImages()
		}
	}

	func reloadImages() {
		images = FileOps.listImages(in: baseFolder)
		index = 0
	}

	func next() { if index < images.count - 1 { index += 1 } }
	func prev() { if index > 0 { index -= 1 } }

	func switchToPreset(_ p: Preset) {
		guard images.indices.contains(index) else { return }
		let name = images[index]
		let src = URL(fileURLWithPath: baseFolder).appendingPathComponent(name)
		do {
			try FileOps.move(srcFolder: baseFolder, filename: name, to: p)
			let dstDir = URL(fileURLWithPath: AppPaths.sortRoot).appendingPathComponent(p.folderName)
			undoStack.append((from: dstDir.appendingPathComponent(name), to: src))
			images.remove(at: index)
			if index >= images.count { index = max(0, images.count - 1) }
		} catch { NSSound.beep() }
	}

	func undoLast() {
		guard let last = undoStack.popLast() else { return }
		do {
			try FileOps.undoMove(from: last.from, to: last.to)
			reloadImages()
			if let pos = images.firstIndex(of: last.to.lastPathComponent) { index = pos }
		} catch { NSSound.beep() }
	}

	func reveal() {
		FileOps.revealInFinder(folder: baseFolder, file: images.indices.contains(index) ? images[index] : nil)
	}

	func saveStar() {
		guard images.indices.contains(index) else { return }
		do { try FileOps.copyToFavorites(baseFolder: baseFolder, filename: images[index]) } catch { NSSound.beep() }
	}
}

private struct KeyboardShortcutHandlers: ViewModifier {
	let next: () -> Void
	let prev: () -> Void
	let zoomIn: () -> Void
	let zoomOut: () -> Void
	let resetZoom: () -> Void
	let undo: () -> Void

	func body(content: Content) -> some View {
		content
			.onReceive(NotificationCenter.default.publisher(for: NSApplication.didBecomeActiveNotification)) { _ in }
			.onKeyPress(.rightArrow, perform: next)
			.onKeyPress(.leftArrow, perform: prev)
			.onKeyPress(Character("j"), perform: next)
			.onKeyPress(Character("k"), perform: prev)
			.onKeyPress(Character("["), perform: zoomOut)
			.onKeyPress(Character("]"), perform: zoomIn)
			.onKeyPress(Character("Z"), perform: resetZoom)
			.onKeyPress(.escape, perform: undo)
	}
}

private extension View {
	func keyboardShortcutHandlers(next: @escaping () -> Void, prev: @escaping () -> Void, zoomIn: @escaping () -> Void, zoomOut: @escaping () -> Void, resetZoom: @escaping () -> Void, undo: @escaping () -> Void) -> some View {
		modifier(KeyboardShortcutHandlers(next: next, prev: prev, zoomIn: zoomIn, zoomOut: zoomOut, resetZoom: resetZoom, undo: undo))
	}
}

// Simple key press handler for SwiftUI
private struct KeyPressModifier: ViewModifier {
	let key: KeyEquivalent?
	let char: Character?
	let perform: () -> Void
	func body(content: Content) -> some View {
		content.background(KeyPressRepresentable(key: key, char: char, perform: perform))
	}
}

private extension View {
	func onKeyPress(_ key: KeyEquivalent, perform: @escaping () -> Void) -> some View { modifier(KeyPressModifier(key: key, char: nil, perform: perform)) }
	func onKeyPress(_ char: Character, perform: @escaping () -> Void) -> some View { modifier(KeyPressModifier(key: nil, char: char, perform: perform)) }
}

private struct KeyPressRepresentable: NSViewRepresentable {
	let key: KeyEquivalent?
	let char: Character?
	let perform: () -> Void

	func makeNSView(context: Context) -> KeyPressView {
		let v = KeyPressView()
		v.onPress = { [perform] pressed in
			if let key = key, pressed == key.character { perform() }
			if let c = char, pressed == c { perform() }
		}
		return v
	}

	func updateNSView(_ nsView: KeyPressView, context: Context) {}
}

private final class KeyPressView: NSView {
	var onPress: ((Character) -> Void)?
	override var acceptsFirstResponder: Bool { true }
	override func keyDown(with event: NSEvent) {
		if let chars = event.charactersIgnoringModifiers, let c = chars.first { onPress?(c) }
	}
}

