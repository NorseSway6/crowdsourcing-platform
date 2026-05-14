export interface CanvasSize {
	w: number
	h: number
}

export interface StageTransform {
	x: number
	y: number
	scale: number
}

export interface DraftRect {
	x: number
	y: number
	w: number
	h: number
}

export interface ImageState {
	element: HTMLImageElement
	scale: number
	offset: { x: number; y: number }
}
