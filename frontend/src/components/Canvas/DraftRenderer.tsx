import { Circle, Group, Line, Rect } from 'react-konva'

import type { DraftRect } from './Canvas.types'
import { toStageCoord } from './Canvas.utils'

interface Props {
	draftRect: DraftRect | null
	draftPolygon: number[]
	imgScale: number
	imgOffset: { x: number; y: number }
}

export const DraftRenderer = ({
	draftRect,
	draftPolygon,
	imgScale,
	imgOffset
}: Props) => (
	<>
		{draftRect && (
			<Rect
				x={draftRect.x}
				y={draftRect.y}
				width={draftRect.w}
				height={draftRect.h}
				stroke='#ff5722'
				strokeWidth={2}
				dash={[6, 3]}
				fill='rgba(255,87,34,0.08)'
				listening={false}
			/>
		)}

		{draftPolygon.length >= 2 &&
			(() => {
				const pts: number[] = []
				for (let j = 0; j < draftPolygon.length; j += 2) {
					const { x, y } = toStageCoord(
						draftPolygon[j],
						draftPolygon[j + 1],
						imgOffset,
						imgScale
					)
					pts.push(x, y)
				}

				return (
					<Group>
						<Line
							points={pts}
							stroke='#ff5722'
							strokeWidth={2}
							dash={[6, 3]}
							listening={false}
						/>
						<Circle
							x={pts[0]}
							y={pts[1]}
							radius={7}
							fill='#ff5722'
							opacity={0.7}
							listening={false}
						/>
						{pts.reduce<React.ReactNode[]>((acc, _, idx) => {
							if (idx % 2 === 0) {
								acc.push(
									<Circle
										key={idx}
										x={pts[idx]}
										y={pts[idx + 1]}
										radius={4}
										fill='#fff'
										stroke='#ff5722'
										strokeWidth={1.5}
										listening={false}
									/>
								)
							}
							return acc
						}, [])}
					</Group>
				)
			})()}
	</>
)
