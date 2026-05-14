import { v4 as uuidv4 } from 'uuid'

import { COLORS } from './Canvas.constants'

export const uid = () => uuidv4()

export const getColor = (i: number) => COLORS[i % COLORS.length]

export const toImageCoord = (
	sx: number,
	sy: number,
	imgOffset: { x: number; y: number },
	imgScale: number
) => ({
	x: (sx - imgOffset.x) / imgScale,
	y: (sy - imgOffset.y) / imgScale
})

export const toStageCoord = (
	ix: number,
	iy: number,
	imgOffset: { x: number; y: number },
	imgScale: number
) => ({
	x: ix * imgScale + imgOffset.x,
	y: iy * imgScale + imgOffset.y
})

export const getStagePointer = (
	rawPos: { x: number; y: number },
	stagePos: { x: number; y: number },
	stageScale: number
) => ({
	x: (rawPos.x - stagePos.x) / stageScale,
	y: (rawPos.y - stagePos.y) / stageScale
})
