import { Select } from '@/components/ui'

import { useAnalytics } from '@/hooks/useAnalytics'

import type { AssignmentOut } from '@/api/assignments'
import type { UserOut } from '@/api/users'

import styles from './Analytics.module.scss'

const fullName = (user: UserOut) =>
	[user.profile.last_name, user.profile.first_name, user.profile.middle_name]
		.filter(Boolean)
		.join(' ') || user.email

const statusLabel = (status: AssignmentOut['status']) => {
	switch (status) {
		case 'APPROVED':
			return { text: 'Завершено', done: true }
		case 'PENDING':
			return { text: 'На валидации', done: false }
		case 'REJECTED':
			return { text: 'Отклонено', done: false }
		case 'IN_PROGRESS':
			return { text: 'Не завершено', done: false }
	}
}

export const CustomerAnalyticsPage = () => {
	const {
		users,
		loading,
		error,
		filtered,
		search,
		setSearch,
		poolFilter,
		setPoolFilter,
		poolOptions
	} = useAnalytics()

	return (
		<div className={styles.page}>
			<h1 className={styles.pageTitle}>Аналитика</h1>

			<div className={styles.filters}>
				<Select
					value={poolFilter}
					onChange={setPoolFilter}
					options={poolOptions}
				/>
				<input
					className={styles.searchInput}
					placeholder='Иванов Иван Иванович'
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
						filtered.map(a => {
							const user = users[a.user_id]
							const name = user ? fullName(user) : a.user_id.slice(0, 8)
							const { text, done } = statusLabel(a.status)
							return (
								<div key={a.assignment_id} className={styles.card}>
									<div className={styles.cardHeader}>
										<span className={styles.cardTitle}>
											Задание №{a.task_id}
										</span>
										<span className={styles.cardStudent}>Студент: {name}</span>
									</div>
									<div
										className={done ? styles.statusDone : styles.statusPending}
									>
										{text}
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
