export type Tool = 'select' | 'bbox' | 'pan' | 'point' | 'polygon'

export interface BBoxShape {
	id: string
	type: 'bbox'
	x: number
	y: number
	width: number
	height: number
}

export interface PointShape {
	id: string
	type: 'point'
	x: number
	y: number
}

export interface PolygonShape {
	id: string
	type: 'polygon'
	points: number[]
	closed: boolean
}

export type Shape = BBoxShape | PointShape | PolygonShape
