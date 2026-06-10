import { useEffect, useState } from 'react'
import { Cell, Pie, PieChart } from 'recharts'

import { type AssignmentOut, assignmentsApi } from '@/api/assignments'

import styles from './Review.module.scss'

export const CustomerReviewPage = () => {
	const [assignments, setAssignments] = useState<AssignmentOut[]>([])
	const [loading, setLoading] = useState(false)

	useEffect(() => {
		const load = async () => {
			setLoading(true)
			try {
				const all = await assignmentsApi.getAll()
				setAssignments(all)
			} catch {
				setAssignments([])
			} finally {
				setLoading(false)
			}
		}
		load()
	}, [])

	const approved = assignments.filter(a => a.status === 'APPROVED').length
	const pending = assignments.filter(a => a.status === 'PENDING').length
	const rejected = assignments.filter(a => a.status === 'REJECTED').length

	const total = approved + pending + rejected
	const percent = total === 0 ? 0 : Math.round((approved / total) * 100)

	const data = [
		{ name: 'Верно', value: approved || 1 },
		{ name: 'Ошибки', value: pending + rejected || 0 }
	]

	return (
		<div className={styles.page}>
			<h1 className={styles.pageTitle}>К проверке</h1>

			{loading ? (
				<div>Загрузка...</div>
			) : (
				<div className={styles.card}>
					<div className={styles.cardTitle}>Статистика разметки</div>
					<div className={styles.cardSubtitle}>Описание</div>

					<div className={styles.chartRow}>
						<PieChart width={220} height={220}>
							<Pie
								data={data}
								cx={105}
								cy={105}
								innerRadius={70}
								outerRadius={105}
								dataKey='value'
								startAngle={90}
								endAngle={-270}
							>
								<Cell fill='#4caf50' />
								<Cell fill='#e53935' />
							</Pie>
							<text
								x={110}
								y={110}
								textAnchor='middle'
								dominantBaseline='middle'
								className={styles.chartLabel}
							>
								{percent}%
							</text>
						</PieChart>

						<div className={styles.legend}>
							<div className={styles.legendItem}>
								<div
									className={styles.legendDot}
									style={{ background: '#4caf50' }}
								/>
								Разметка выполнена верно
							</div>
							<div className={styles.legendItem}>
								<div
									className={styles.legendDot}
									style={{ background: '#e53935' }}
								/>
								Есть ошибки
							</div>
						</div>
					</div>
				</div>
			)}
		</div>
	)
}
