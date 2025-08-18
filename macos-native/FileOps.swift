import Foundation
import AppKit

enum FileOps {
	static func listImages(in folder: String) -> [String] {
		let valid = Set([".jpg",".jpeg",".png",".bmp",".gif"]) 
		guard let urls = try? FileManager.default.contentsOfDirectory(at: URL(fileURLWithPath: folder), includingPropertiesForKeys: nil, options: [.skipsHiddenFiles]) else { return [] }
		return urls.filter { !$0.hasDirectoryPath && valid.contains($0.pathExtension.lowercased().withDot) }
			.sorted { $0.lastPathComponent.localizedStandardCompare($1.lastPathComponent) == .orderedAscending }
			.map { $0.lastPathComponent }
	}

	static func move(srcFolder: String, filename: String, to preset: Preset) throws {
		let src = URL(fileURLWithPath: srcFolder).appendingPathComponent(filename)
		let dstDir = URL(fileURLWithPath: AppPaths.sortRoot).appendingPathComponent(preset.folderName)
		let dst = dstDir.appendingPathComponent(filename)
		try FileManager.default.createDirectory(at: dstDir, withIntermediateDirectories: true)
		try FileManager.default.moveItem(at: src, to: dst)
	}

	static func undoMove(from: URL, to original: URL) throws {
		try FileManager.default.moveItem(at: from, to: original)
	}

	static func revealInFinder(folder: String, file: String?) {
		let url = URL(fileURLWithPath: folder)
		if let file { NSWorkspace.shared.activateFileViewerSelecting([url.appendingPathComponent(file)]) }
		else { NSWorkspace.shared.selectFile(nil, inFileViewerRootedAtPath: folder) }
	}

	static func copyToFavorites(baseFolder: String, filename: String) throws {
		let src = URL(fileURLWithPath: baseFolder).appendingPathComponent(filename)
		let favDir = URL(fileURLWithPath: AppPaths.sortRoot).appendingPathComponent(AppPaths.favorite)
		try FileManager.default.createDirectory(at: favDir, withIntermediateDirectories: true)
		var dst = favDir.appendingPathComponent(filename)
		if FileManager.default.fileExists(atPath: dst.path) {
			let name = src.deletingPathExtension().lastPathComponent
			let ext = src.pathExtension
			var i = 1
			repeat {
				dst = favDir.appendingPathComponent("\(name)_\(i).\(ext)")
				i += 1
			} while FileManager.default.fileExists(atPath: dst.path)
		}
		try FileManager.default.copyItem(at: src, to: dst)
	}
}

private extension String {
	var withDot: String { starts(with: ".") ? self : "." + self }
}

