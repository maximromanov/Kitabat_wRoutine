import Foundation

struct Preset: Identifiable, Hashable {
	let id: String
	let label: String
	let folderName: String
}

enum AppPaths {
	static let home = FileManager.default.homeDirectoryForCurrentUser.path
	static let sortRoot: String = {
		let cwd = FileManager.default.currentDirectoryPath
		let sort = URL(fileURLWithPath: cwd).appendingPathComponent("../SELECTED/__SORTING").standardizedFileURL.path
		try? FileManager.default.createDirectory(atPath: sort, withIntermediateDirectories: true)
		return sort
	}()
	static let favorite = "__XXZ_FAVORITE"
}

let defaultPresets: [Preset] = [
	Preset(id: "1", label: "1️⃣ R", folderName: "__1A_REVIEW_STEP1_SMALL_TO_1B"),
	Preset(id: "2", label: "2️⃣ R", folderName: "__1B_REVIEW_STEP2_SMALL_TO_2A"),
	Preset(id: "3", label: "🆙 UPSCALE", folderName: "__2A_TO_UPSCALE_NEXT_2B"),
	Preset(id: "4", label: "🗑️ DEL", folderName: "__XXE_TO_DELETE"),
	Preset(id: "5", label: "🆙 READY", folderName: "__6B_UPSCALED_STEP2_TO_7A_or_7B"),
	Preset(id: "6", label: "✅ NSFW", folderName: "__7A_FINAL_NSFW_0000"),
	Preset(id: "7", label: "✅ SFW", folderName: "__7B_FINAL_SFW_0000"),
	Preset(id: "8", label: "📱 SOC", folderName: "__XXB_SOCIAL"),
	Preset(id: "9", label: "📦 ASIDE", folderName: "__XXA_ASIDE"),
	Preset(id: "0", label: "🛠 FIX", folderName: "__XXC_FIXREQUIRED"),
	Preset(id: "-", label: "⛔ BORDER", folderName: "__XXC_BORDERLINE"),
	Preset(id: "=", label: "❓ TEMP", folderName: "__XXD_TEMP"),
]

func ensurePresetFolders() {
	for p in defaultPresets {
		let path = (AppPaths.sortRoot as NSString).appendingPathComponent(p.folderName)
		try? FileManager.default.createDirectory(atPath: path, withIntermediateDirectories: true)
	}
	let fav = (AppPaths.sortRoot as NSString).appendingPathComponent(AppPaths.favorite)
	try? FileManager.default.createDirectory(atPath: fav, withIntermediateDirectories: true)
}

