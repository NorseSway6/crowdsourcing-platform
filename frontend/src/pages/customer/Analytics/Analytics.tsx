import { Select } from '@/components/ui'

import { useAnalytics } from '@/hooks/useAnalytics'

import styles from './Analytics.module.scss'

const fullName = (u: {
	last_name: string
	first_name: string
	middle_name: string
}) => [u.last_name, u.first_name, u.middle_name].filter(Boolean).join(' ')

export const CustomerAnalyticsPage = () => {
	const {
		poolsProgress,
		users,
		loading,
		error,
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
				<>
					{poolsProgress.length > 0 && (
						<div className={styles.progressSection}>
							{poolsProgress.map(p => (
								<div key={p.pool_id} className={styles.progressCard}>
									<div className={styles.progressHeader}>
										<span className={styles.cardTitle}>
											Пул #{p.pool_id} — {p.pool_type}
										</span>
										<span className={styles.cardStats}>
											{p.completed_tasks} / {p.total_tasks} задач
										</span>
									</div>
									<div className={styles.progressBar}>
										<div
											className={styles.progressFill}
											style={{ width: `${p.progress_percentage}%` }}
										/>
									</div>
									<div className={styles.progressPercent}>
										{Math.round(p.progress_percentage)}%
									</div>
								</div>
							))}
						</div>
					)}

					<div className={styles.list}>
						{users.length === 0 ? (
							<div className={styles.empty}>Нет данных</div>
						) : (
							users.map((u, i) => (
								<div key={i} className={styles.card}>
									<div className={styles.cardHeader}>
										<span className={styles.cardTitle}>{fullName(u)}</span>
										<span className={styles.cardStudent}>
											{u.institution} · {u.group}
										</span>
									</div>
									<div className={styles.userStats}>
										<span>Отправлено: {u.submitted}</span>
										<span>Одобрено: {u.approved}</span>
										<span>Точность: {Math.round(u.user_accuracy * 100)}%</span>
									</div>
								</div>
							))
						)}
					</div>
				</>
			)}
		</div>
	)
}
