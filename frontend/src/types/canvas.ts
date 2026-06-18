export type Tool = 'select' | 'bbox' | 'pan' | 'point' | 'polygon'

export interface BBoxShape {
	id: string
	type: 'bbox'
	x: number
	y: number
	width: number
	height: number
	category_id: number
}

export interface PointShape {
	id: string
	type: 'point'
	x: number
	y: number
	category_id: number
}

export interface PolygonShape {
	id: string
	type: 'polygon'
	points: number[]
	closed: boolean
	category_id: number
}

export type Shape = BBoxShape | PointShape | PolygonShape
