import { LogOut } from 'lucide-react'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { Canvas } from '@/components/Canvas'
import { LabelingSidebar } from '@/components/LabelingSidebar'
import { Toolbar } from '@/components/Toolbar'

import type { Shape, Tool } from '@/types/canvas'

import { shapesToCoco } from '@/utils/coco'

import { useAssignment } from '@/hooks'
import styles from './Labeling.module.scss'

export const LabelingPage = () => {
	const navigate = useNavigate()
	const [tool, setTool] = useState<Tool>('bbox')
	const [shapes, setShapes] = useState<Shape[]>([])
	const [history, setHistory] = useState<Shape[][]>([[]])
	const [historyIndex, setHistoryIndex] = useState(0)

	const { current, submit } = useAssignment()

	const handleSubmit = async () => {
		if (!current || shapes.length === 0) return
		const coco = shapesToCoco(shapes)
		await submit(coco)
		setShapes([])
		setHistory([[]])
		setHistoryIndex(0)
	}

	const handleUndo = () => {
		if (historyIndex <= 0) return
		const i = historyIndex - 1
		setHistoryIndex(i)
		setShapes(history[i])
	}

	const handleRedo = () => {
		if (historyIndex >= history.length - 1) return
		const i = historyIndex + 1
		setHistoryIndex(i)
		setShapes(history[i])
	}

	return (
		<div className={styles.page}>
			<div className={styles.topbar}>
				<div className={styles.topbarLeft}>
					<button
						className={styles.exitBtn}
						onClick={() => navigate('/tasks')}
					>
						<LogOut /> Выйти
					</button>
				</div>
				<div className={styles.topbarCenter}>
					<div className={styles.timer}>10:00</div>
					<div className={styles.taskName}>Задание {1}</div>
				</div>
			</div>

			<div className={styles.body}>
				<Toolbar
					tool={tool}
					onToolChange={setTool}
					onUndo={handleUndo}
					onRedo={handleRedo}
					canUndo={historyIndex > 0}
					canRedo={historyIndex < history.length - 1}
				/>
				<Canvas
					imageUrl={current?.task.image_url ?? ''}
					tool={tool}
					shapes={shapes}
					onShapesChange={setShapes}
					history={history}
					onHistoryChange={setHistory}
					historyIndex={historyIndex}
					onHistoryIndexChange={setHistoryIndex}
				/>
				<LabelingSidebar
					shapes={shapes}
					onSubmit={handleSubmit}
					onSkip={() => navigate('/tasks')}
					submitting={false}
				/>
			</div>
		</div>
	)
}
