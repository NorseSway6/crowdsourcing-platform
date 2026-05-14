import type { Tool } from '@/types/canvas'
import { Hand, MapPin, MousePointer2, Pentagon, Square } from 'lucide-react'

export const toolButtons = [
	{
		tool: 'select' as Tool,
		icon: MousePointer2,
		title: 'Выбор'
	},
	{
		tool: 'bbox' as Tool,
		icon: Square,
		title: 'Bounding Box'
	},
	{
		tool: 'pan' as Tool,
		icon: Hand,
		title: 'Перемещение'
	},
	{
		tool: 'polygon' as Tool,
		icon: Pentagon,
		title: 'Полигон'
	},
	{
		tool: 'point' as Tool,
		icon: MapPin,
		title: 'Точка'
	}
]
