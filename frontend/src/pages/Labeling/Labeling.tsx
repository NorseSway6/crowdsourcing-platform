import { LogOut } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { Canvas } from '@/components/Canvas'
import { LabelingSidebar } from '@/components/LabelingSidebar'
import { Toolbar } from '@/components/Toolbar'

import type { Shape, Tool } from '@/types/canvas'

import { shapesToCoco } from '@/utils/coco'

import styles from './Labeling.module.scss'
import { useAssignment } from '@/hooks'

const TIMER_SECONDS = 600

const formatTime = (s: number) => {
	const m = Math.floor(s / 60)
		.toString()
		.padStart(2, '0')
	const sec = (s % 60).toString().padStart(2, '0')
	return `${m}:${sec}`
}

export const LabelingPage = () => {
	const navigate = useNavigate()
	const [tool, setTool] = useState<Tool>('bbox')
	const [shapes, setShapes] = useState<Shape[]>([])
	const [history, setHistory] = useState<Shape[][]>([[]])
	const [historyIndex, setHistoryIndex] = useState(0)
	const [timeLeft, setTimeLeft] = useState(TIMER_SECONDS)
	const timerRef = useRef<ReturnType<typeof setInterval> | null>(null)

	const { current, submit } = useAssignment()

	// сбрасываем таймер при смене задания
	useEffect(() => {
		setTimeLeft(TIMER_SECONDS)

		if (timerRef.current) clearInterval(timerRef.current)

		timerRef.current = setInterval(() => {
			setTimeLeft(t => {
				if (t <= 1) {
					clearInterval(timerRef.current!)
					return 0
				}
				return t - 1
			})
		}, 1000)

		return () => {
			if (timerRef.current) clearInterval(timerRef.current)
		}
	}, [current?.assignment.assignment_id])

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

	const isTimeLow = timeLeft < 60

	return (
		<div className={styles.page}>
			<div className={styles.topbar}>
				<div className={styles.topbarLeft}>
					<button className={styles.exitBtn} onClick={() => navigate('/tasks')}>
						<LogOut /> Выйти
					</button>
				</div>
				<div className={styles.topbarCenter}>
					<div
						className={styles.timer}
						style={{ color: isTimeLow ? '#e53935' : undefined }}
					>
						{formatTime(timeLeft)}
					</div>
					<div className={styles.taskName}>
						{current ? `Задание #${current.task.task_id}` : '—'}
					</div>
				</div>
				<div className={styles.topbarRight}>
					{current && (
						<span className={styles.taskBadge}>
							Пул #{current.task.pool_id}
						</span>
					)}
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
