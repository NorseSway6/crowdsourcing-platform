import { useEffect, useState } from 'react'
import { IMAGE_FIT_PADDING } from './Canvas.constants'
import type { CanvasSize, ImageState } from './Canvas.types'

export const useContainerSize = (ref: React.RefObject<HTMLDivElement | null>): CanvasSize => {
	const [size, setSize] = useState<CanvasSize>({ w: 800, h: 600 })

	useEffect(() => {
		const el = ref.current
		if (!el) return
		const ro = new ResizeObserver(() => setSize({ w: el.clientWidth, h: el.clientHeight }))
		ro.observe(el)
		return () => ro.disconnect()
	}, [ref])

	return size
}

export const useImage = (imageUrl: string, size: CanvasSize): ImageState | null => {
	const [imageState, setImageState] = useState<ImageState | null>(null)

	useEffect(() => {
		const img = new window.Image()
		img.crossOrigin = 'anonymous'
		img.src = imageUrl
		img.onload = () => {
			const scale = Math.min(size.w / img.width, size.h / img.height, 1) * IMAGE_FIT_PADDING
			setImageState({
				element: img,
				scale,
				offset: {
					x: (size.w - img.width * scale) / 2,
					y: (size.h - img.height * scale) / 2
				}
			})
		}
	}, [imageUrl, size.w, size.h])

	return imageState
}
