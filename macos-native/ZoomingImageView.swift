import SwiftUI

struct ZoomingImageView: View {
	let image: NSImage
	@Binding var zoom: CGFloat

	var body: some View {
		GeometryReader { geo in
			ScrollView([.horizontal, .vertical]) {
				Image(nsImage: image)
					.resizable()
					.interpolation(.high)
					.scaledToFit()
					.frame(width: max(1, geo.size.width * zoom), height: max(1, geo.size.height * zoom))
					.onTapGesture(count: 2) { zoom = 1.0 }
			}
		}
	}
}

