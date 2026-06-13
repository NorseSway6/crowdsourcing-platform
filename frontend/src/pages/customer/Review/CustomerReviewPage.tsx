import { useEffect, useMemo, useState } from 'react'
import { Cell, Pie, PieChart } from 'recharts'

import { analyticsApi, type UserInfo } from '@/api/analytics'

import styles from './Review.module.scss'

export const CustomerReviewPage = () => {
	const [users, setUsers] = useState<UserInfo[]>([])
	const [loading, setLoading] = useState(false)

	useEffect(() => {
		const load = async () => {
			setLoading(true)
			try {
				const data = await analyticsApi.getUsersInfo()
				setUsers(data)
			} catch {
				setUsers([])
			} finally {
				setLoading(false)
			}
		}
		load()
	}, [])

	const { approved, errors, percent } = useMemo(() => {
		const approvedCount = users.reduce((sum, u) => sum + u.approved, 0)
		const submittedCount = users.reduce((sum, u) => sum + u.submitted, 0)
		const errorCount = Math.max(submittedCount - approvedCount, 0)
		const total = approvedCount + errorCount
		return {
			approved: approvedCount,
			errors: errorCount,
			percent: total === 0 ? 0 : Math.round((approvedCount / total) * 100)
		}
	}, [users])

	const data = [
		{ name: 'Верно', value: approved || 1 },
		{ name: 'Ошибки', value: errors || 0 }
	]

	return (
		<div className={styles.page}>
			<h1 className={styles.pageTitle}>К проверке</h1>

			{loading ? (
				<div>Загрузка...</div>
			) : (
				<div className={styles.card}>
					<div className={styles.cardTitle}>Статистика разметки</div>
					<div className={styles.cardSubtitle}>
						Агрегированные данные по всем исполнителям
					</div>

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
								Разметка выполнена верно — {approved}
							</div>
							<div className={styles.legendItem}>
								<div
									className={styles.legendDot}
									style={{ background: '#e53935' }}
								/>
								Есть ошибки — {errors}
							</div>
						</div>
					</div>
				</div>
			)}
		</div>
	)
}
