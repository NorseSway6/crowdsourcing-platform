import type { Shape } from '@/types/canvas'

import type { CocoAnnotation } from '@/api/assignments'

export const shapesToCoco = (shapes: Shape[]): CocoAnnotation => ({
	type: 'coco',
	items: shapes.map(shape => {
		if (shape.type === 'bbox') {
			return {
				category_id: 1,
				bbox: [shape.x, shape.y, shape.width, shape.height],
				area: shape.width * shape.height,
				iscrowd: 0 as const,
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
				bbox: [x, y, w, h] as [number, number, number, number],
				area: w * h,
				iscrowd: 0 as const,
				segmentation: [shape.points]
			}
		}
		
		return {
			category_id: 1,
			bbox: [shape.x, shape.y, 1, 1] as [number, number, number, number],
			area: 1,
			iscrowd: 0 as const,
			segmentation: [[shape.x, shape.y]]
		}
	})
})
