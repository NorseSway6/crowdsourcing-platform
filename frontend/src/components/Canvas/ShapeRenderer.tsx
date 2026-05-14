import { Circle, Line, Rect } from 'react-konva'

import type { Shape, Tool } from '@/types/canvas'

import { getColor, toStageCoord } from './Canvas.utils'

interface Props {
	shapes: Shape[]
	imgScale: number
	imgOffset: { x: number; y: number }
	tool: Tool
}

export const ShapeRenderer = ({ shapes, imgScale, imgOffset, tool }: Props) => (
	<>
		{shapes.map((shape, i) => {
			const color = getColor(i)

			if (shape.type === 'bbox') {
				const { x, y } = toStageCoord(shape.x, shape.y, imgOffset, imgScale)
				return (
					<Rect
						key={shape.id}
						x={x}
						y={y}
						width={shape.width * imgScale}
						height={shape.height * imgScale}
						stroke={color}
						strokeWidth={2}
						fill={color + '22'}
						listening={tool === 'select'}
					/>
				)
			}

			if (shape.type === 'point') {
				const { x, y } = toStageCoord(shape.x, shape.y, imgOffset, imgScale)
				return (
					<Circle
						key={shape.id}
						x={x}
						y={y}
						radius={6}
						fill={color}
						stroke='#fff'
						strokeWidth={1.5}
					/>
				)
			}

			if (shape.type === 'polygon') {
				const pts: number[] = []
				for (let j = 0; j < shape.points.length; j += 2) {
					const { x, y } = toStageCoord(
						shape.points[j],
						shape.points[j + 1],
						imgOffset,
						imgScale
					)
					pts.push(x, y)
				}
				return (
					<Line
						key={shape.id}
						points={pts}
						closed={shape.closed}
						stroke={color}
						strokeWidth={2}
						fill={color + '22'}
					/>
				)
			}

			return null
		})}
	</>
)
