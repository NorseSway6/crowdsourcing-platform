import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { analyticsApi, type UserInfo } from '@/api/analytics'
import { Button, Select } from '@/components/ui'

import styles from './Analytics.module.scss'

const fullName = (u: {
	last_name: string
	first_name: string
	middle_name: string
}) => [u.last_name, u.first_name, u.middle_name].filter(Boolean).join(' ')

type SortOption = 'name' | 'accuracy' | 'status'

export const CustomerAnalyticsPage = () => {
	const navigate = useNavigate()
	const [users, setUsers] = useState<UserInfo[]>([])
	const [loading, setLoading] = useState(true)
	const [error, setError] = useState<string | null>(null)
	const [search, setSearch] = useState('')
	const [sort, setSort] = useState<SortOption>('name')

	useEffect(() => {
		const load = async () => {
			setLoading(true)
			try {
				const data = await analyticsApi.getUsersInfo()
				setUsers(data)
			} catch {
				setError('Не удалось загрузить данные')
			} finally {
				setLoading(false)
			}
		}
		load()
	}, [])

	const filtered = users
		.filter(u => {
			if (u.submitted === 0) return false
			if (!search.trim()) return true
			const name = fullName(u).toLowerCase()
			return name.includes(search.toLowerCase())
		})
		.sort((a, b) => {
			if (sort === 'name') return fullName(a).localeCompare(fullName(b))
			if (sort === 'accuracy') return b.user_accuracy - a.user_accuracy
			const aCompleted = a.submitted > 0 && a.user_accuracy >= 0.8 ? 1 : 0
			const bCompleted = b.submitted > 0 && b.user_accuracy >= 0.8 ? 1 : 0
			return bCompleted - aCompleted
		})

	return (
		<div className={styles.page}>
			<h1 className={styles.pageTitle}>Аналитика</h1>

			<div className={styles.filters}>
				<Select
					value={sort}
					onChange={val => setSort(val as SortOption)}
					options={[
						{ value: 'name', label: 'По имени' },
						{ value: 'accuracy', label: 'По точности' },
						{ value: 'status', label: 'По статусу' }
					]}
				/>
				<input
					className={styles.searchInput}
					placeholder='Поиск по имени...'
					value={search}
					onChange={e => setSearch(e.target.value)}
				/>
			</div>

			{loading && <div className={styles.empty}>Загрузка...</div>}
			{error && <div className={styles.empty}>{error}</div>}

			{!loading && !error && (
				<div className={styles.list}>
					{filtered.length === 0 ? (
						<div className={styles.empty}>Нет данных</div>
					) : (
						filtered.map((u, i) => {
							const isCompleted = u.submitted > 0 && u.user_accuracy >= 0.8
							return (
								<div key={i} className={styles.card}>
									<div className={styles.cardLeft}>
										<span className={styles.taskName}>Задание №{i + 1}</span>
										<div className={styles.statusRow}>
											{isCompleted ? (
												<>
													<span className={styles.statusTextDone}>Завершено</span>
													<Button
														variant='secondary'
														onClick={() => navigate('/customer/review')}
													>
														К проверке
													</Button>
												</>
											) : (
												<span className={styles.statusTextPending}>Не завершено</span>
											)}
										</div>
									</div>
									<div className={styles.cardRight}>
										<span className={styles.userName}>{fullName(u)}</span>
									</div>
								</div>
							)
						})
					)}
				</div>
			)}
		</div>
	)
}
