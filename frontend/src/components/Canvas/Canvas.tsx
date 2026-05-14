import { useRef } from 'react'
import { Image as KImage, Layer, Stage } from 'react-konva'

import type { Shape, Tool } from '@/types/canvas'

import { useContainerSize, useImage } from './Canvas.hooks'
import styles from './Canvas.module.scss'
import { DraftRenderer } from './DraftRenderer'
import { ShapeRenderer } from './ShapeRenderer'
import { useCanvas } from './useCanvas'

interface Props {
	imageUrl: string
	tool: Tool
	shapes: Shape[]
	onShapesChange: (s: Shape[]) => void
	history: Shape[][]
	onHistoryChange: (h: Shape[][]) => void
	historyIndex: number
	onHistoryIndexChange: (i: number) => void
}

export const Canvas = ({
	imageUrl,
	tool,
	shapes,
	onShapesChange,
	history,
	onHistoryChange,
	historyIndex,
	onHistoryIndexChange
}: Props) => {
	const containerRef = useRef<HTMLDivElement>(null)
	const size = useContainerSize(containerRef)
	const imageState = useImage(imageUrl, size)

	const imgScale = imageState?.scale ?? 1
	const imgOffset = imageState?.offset ?? { x: 0, y: 0 }

	const {
		stageRef,
		stagePos,
		stageScale,
		draftRect,
		draftPolygon,
		onMouseDown,
		onMouseMove,
		onMouseUp,
		onWheel
	} = useCanvas({
		tool,
		shapes,
		imgScale,
		imgOffset,
		history,
		historyIndex,
		onHistoryChange,
		onHistoryIndexChange,
		onShapesChange
	})

	return (
		<div
			ref={containerRef}
			className={`${styles.wrapper} ${tool === 'pan' ? styles.panMode : tool === 'select' ? styles.selectMode : ''}`}
		>
			<Stage
				ref={stageRef}
				width={size.w}
				height={size.h}
				x={stagePos.x}
				y={stagePos.y}
				scaleX={stageScale}
				scaleY={stageScale}
				onMouseDown={onMouseDown}
				onMouseMove={onMouseMove}
				onMouseUp={onMouseUp}
				onWheel={onWheel}
			>
				<Layer>
					{imageState && (
						<KImage
							image={imageState.element}
							x={imgOffset.x}
							y={imgOffset.y}
							width={imageState.element.width * imgScale}
							height={imageState.element.height * imgScale}
						/>
					)}
					<ShapeRenderer
						shapes={shapes}
						imgScale={imgScale}
						imgOffset={imgOffset}
						tool={tool}
					/>
					<DraftRenderer
						draftRect={draftRect}
						draftPolygon={draftPolygon}
						imgScale={imgScale}
						imgOffset={imgOffset}
					/>
				</Layer>
			</Stage>
		</div>
	)
}
