import type { Shape } from '@/types/canvas'

export interface CocoItem {
	category_id: number
	bbox: [number, number, number, number]
	area: number
	iscrowd: 0 | 1
	segmentation: number[][]
}

export const shapesToCoco = (shapes: Shape[]): CocoItem[] => {
	return shapes.map(shape => {
		if (shape.type === 'bbox') {
			return {
				category_id: 1,
				bbox: [shape.x, shape.y, shape.width, shape.height],
				area: shape.width * shape.height,
				iscrowd: 0,
				segmentation: []
			}
		}

		if (shape.type === 'polygon') {
			const xs = shape.points.filter((_, i) => i % 2 === 0)
			const ys = shape.points.filter((_, i) => i % 2 !== 0)
			const x = Math.min(...xs)
			const y = Math.min(...ys)
			const w = Math.max(...xs) - x
			const h = Math.max(...ys) - y
			return {
				category_id: 1,
				bbox: [x, y, w, h],
				area: w * h,
				iscrowd: 0,
				segmentation: [shape.points]
			}
		}

		return {
			category_id: 1,
			bbox: [shape.x, shape.y, 1, 1],
			area: 1,
			iscrowd: 0,
			segmentation: [[shape.x, shape.y]]
		}
	})
}
