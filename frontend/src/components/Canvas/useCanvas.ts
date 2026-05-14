import type Konva from 'konva'
import { useRef, useState } from 'react'

import type {
	BBoxShape,
	PointShape,
	PolygonShape,
	Shape,
	Tool
} from '@/types/canvas'

import {
	CLOSE_POLYGON_THRESHOLD,
	ZOOM_FACTOR,
	ZOOM_MAX,
	ZOOM_MIN
} from './Canvas.constants'
import type { DraftRect } from './Canvas.types'
import { getStagePointer, toImageCoord, uid } from './Canvas.utils'

interface UseCanvasProps {
	tool: Tool
	shapes: Shape[]
	imgScale: number
	imgOffset: { x: number; y: number }
	history: Shape[][]
	historyIndex: number
	onHistoryChange: (h: Shape[][]) => void
	onHistoryIndexChange: (i: number) => void
	onShapesChange: (s: Shape[]) => void
}

export const useCanvas = ({
	tool,
	shapes,
	imgScale,
	imgOffset,
	history,
	historyIndex,
	onHistoryChange,
	onHistoryIndexChange,
	onShapesChange
}: UseCanvasProps) => {
	const stageRef = useRef<Konva.Stage>(null)
	const isPanning = useRef(false)
	const lastPan = useRef({ x: 0, y: 0 })

	const [drawing, setDrawing] = useState(false)
	const [startPos, setStartPos] = useState({ x: 0, y: 0 })
	const [draftRect, setDraftRect] = useState<DraftRect | null>(null)
	const [draftPolygon, setDraftPolygon] = useState<number[]>([])
	const [stagePos, setStagePos] = useState({ x: 0, y: 0 })
	const [stageScale, setStageScale] = useState(1)

	const pushHistory = (next: Shape[]) => {
		const h = [...history.slice(0, historyIndex + 1), next]
		onHistoryChange(h)
		onHistoryIndexChange(h.length - 1)
		onShapesChange(next)
	}

	const getPointer = () => {
		const raw = stageRef.current!.getPointerPosition()!
		return getStagePointer(raw, stagePos, stageScale)
	}

	const onMouseDown = (e: Konva.KonvaEventObject<MouseEvent>) => {
		const pos = getPointer()

		if (tool === 'pan') {
			isPanning.current = true
			lastPan.current = { x: e.evt.clientX, y: e.evt.clientY }
			return
		}

		if (tool === 'bbox') {
			setDrawing(true)
			setStartPos(pos)
			setDraftRect({ x: pos.x, y: pos.y, w: 0, h: 0 })
			return
		}

		if (tool === 'point') {
			const ic = toImageCoord(pos.x, pos.y, imgOffset, imgScale)
			pushHistory([
				...shapes,
				{ id: uid(), type: 'point', x: ic.x, y: ic.y } as PointShape
			])
			return
		}

		if (tool === 'polygon') {
			if (draftPolygon.length >= 4) {
				const dist = Math.hypot(
					pos.x - (draftPolygon[0] * imgScale + imgOffset.x),
					pos.y - (draftPolygon[1] * imgScale + imgOffset.y)
				)
				if (dist < CLOSE_POLYGON_THRESHOLD) {
					pushHistory([
						...shapes,
						{
							id: uid(),
							type: 'polygon',
							points: draftPolygon,
							closed: true
						} as PolygonShape
					])
					setDraftPolygon([])
					return
				}
			}
			const ic = toImageCoord(pos.x, pos.y, imgOffset, imgScale)
			setDraftPolygon(p => [...p, ic.x, ic.y])
		}
	}

	const onMouseMove = (e: Konva.KonvaEventObject<MouseEvent>) => {
		if (tool === 'pan' && isPanning.current) {
			const dx = e.evt.clientX - lastPan.current.x
			const dy = e.evt.clientY - lastPan.current.y
			lastPan.current = { x: e.evt.clientX, y: e.evt.clientY }
			setStagePos(p => ({ x: p.x + dx, y: p.y + dy }))
			return
		}

		if (tool === 'bbox' && drawing) {
			const pos = getPointer()
			setDraftRect({
				x: Math.min(pos.x, startPos.x),
				y: Math.min(pos.y, startPos.y),
				w: Math.abs(pos.x - startPos.x),
				h: Math.abs(pos.y - startPos.y)
			})
		}
	}

	const onMouseUp = () => {
		if (tool === 'pan') {
			isPanning.current = false
			return
		}

		if (
			tool === 'bbox' &&
			drawing &&
			draftRect &&
			draftRect.w > 5 &&
			draftRect.h > 5
		) {
			const ic = toImageCoord(draftRect.x, draftRect.y, imgOffset, imgScale)
			pushHistory([
				...shapes,
				{
					id: uid(),
					type: 'bbox',
					x: ic.x,
					y: ic.y,
					width: draftRect.w / imgScale,
					height: draftRect.h / imgScale
				} as BBoxShape
			])
		}

		setDrawing(false)
		setDraftRect(null)
	}

	const onWheel = (e: Konva.KonvaEventObject<WheelEvent>) => {
		e.evt.preventDefault()
		const oldScale = stageScale
		const pointer = stageRef.current!.getPointerPosition()!
		const newScale = Math.max(
			ZOOM_MIN,
			Math.min(
				e.evt.deltaY < 0 ? oldScale * ZOOM_FACTOR : oldScale / ZOOM_FACTOR,
				ZOOM_MAX
			)
		)
		const mp = {
			x: (pointer.x - stagePos.x) / oldScale,
			y: (pointer.y - stagePos.y) / oldScale
		}
		setStageScale(newScale)
		setStagePos({
			x: pointer.x - mp.x * newScale,
			y: pointer.y - mp.y * newScale
		})
	}

	return {
		stageRef,
		stagePos,
		stageScale,
		drawing,
		draftRect,
		draftPolygon,
		onMouseDown,
		onMouseMove,
		onMouseUp,
		onWheel
	}
}
