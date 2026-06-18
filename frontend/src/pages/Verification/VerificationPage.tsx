import { LogOut } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { Button } from '@/components/ui'
import { useVerification } from '@/hooks/useVerification'

import styles from './Verification.module.scss'

const TIMER_SECONDS = 300

const formatTime = (s: number) => {
	const m = Math.floor(s / 60)
		.toString()
		.padStart(2, '0')
	const sec = (s % 60).toString().padStart(2, '0')
	return `${m}:${sec}`
}

interface Annotation {
	category_id: number
	type: string
	bbox: [number, number, number, number]
	area: number
	iscrowd: number
	segmentation: number[][]
}

export const VerificationPage = () => {
	const navigate = useNavigate()
	const [timeLeft, setTimeLeft] = useState(TIMER_SECONDS)
	const timerRef = useRef<ReturnType<typeof setInterval> | null>(null)

	const { current, submit, fetchNext, tasksFinished, loading, error } =
		useVerification()

	const annotation = current?.assignment.annotation as
		| { items?: Annotation[] }
		| null
	const items = annotation?.items ?? []

	useEffect(() => {
		if (tasksFinished) {
			navigate('/tasks')
		}
	}, [tasksFinished, navigate])

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

	useEffect(() => {
		if (timeLeft === 0) {
			fetchNext()
		}
	}, [timeLeft, fetchNext])

	const handleVerify = async (isCorrect: boolean) => {
		await submit(isCorrect)
		setTimeLeft(TIMER_SECONDS)
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
						{current ? `Верификация #${current.task.task_id}` : '—'}
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
				<div className={styles.imageContainer}>
					{current?.task.image_url && (
						<img
							src={current.task.image_url}
							alt='Задание'
							className={styles.image}
						/>
					)}
					{items.map((item, i) => {
						const [x, y, w, h] = item.bbox
						return (
							<div
								key={i}
								className={styles.annotationBox}
								style={{
									left: `${x}px`,
									top: `${y}px`,
									width: `${w}px`,
									height: `${h}px`
								}}
							>
								<span className={styles.annotationLabel}>
									#{item.category_id}
								</span>
							</div>
						)
					})}
				</div>

				<div className={styles.sidebar}>
					<div className={styles.question}>
						Разметка выполнена корректно?
					</div>

					{items.length > 0 && (
						<div className={styles.annotationInfo}>
							Найдено объектов: {items.length}
						</div>
					)}

					{error && <div className={styles.error}>{error}</div>}

					<Button
						full
						onClick={() => handleVerify(true)}
						disabled={loading || !current}
					>
						{loading ? 'Отправка...' : 'Верно'}
					</Button>
					<Button
						variant='danger'
						full
						onClick={() => handleVerify(false)}
						disabled={loading || !current}
					>
						{loading ? 'Отправка...' : 'Неверно'}
					</Button>
					<Button
						variant='secondary'
						full
						onClick={() => navigate('/tasks')}
						disabled={loading}
					>
						Пропустить
					</Button>
				</div>
			</div>
		</div>
	)
}
