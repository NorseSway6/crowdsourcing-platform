import { useNavigate } from 'react-router-dom'

import { useProjects } from '@/hooks/useProjects'

import styles from './Projects.module.scss'

export const ProjectsPage = () => {
	const { projects, loading, error } = useProjects()
	const navigate = useNavigate()

	return (
		<div className={styles.page}>
			<h1 className={styles.pageTitle}>Ваши проекты</h1>

			{loading && <div className={styles.empty}>Загрузка...</div>}
			{error && <div className={styles.empty}>{error}</div>}

			{!loading && !error && (
				<>
					<div className={styles.list}>
						{projects.length === 0 ? (
							<div className={styles.empty}>Нет проектов</div>
						) : (
							projects.map(pipeline => (
								<div key={pipeline.pipeline_id} className={styles.card}>
									<div className={styles.cardHeader}>
										<span className={styles.cardTitle}>{pipeline.name}</span>
										<span className={styles.cardStats}>
											Студентов выполнило: {pipeline.completedCount}
										</span>
									</div>
									<div className={styles.cardMeta}>
										{pipeline.pools.map(pool => (
											<span key={pool.pool_id} className={styles.poolBadge}>
												{pool.pool_type === 'ANNOTATION'
													? 'Разметка'
													: 'Верификация'}{' '}
												— {pool.status}
											</span>
										))}
									</div>
								</div>
							))
						)}
					</div>

					<div className={styles.actions}>
						<button
							className={styles.btnAnalytics}
							onClick={() => navigate('/customer/analytics')}
						>
							Аналитика проекта
						</button>
						<button
							className={styles.btnReview}
							onClick={() => navigate('/customer/review')}
						>
							К проверке
						</button>
					</div>
				</>
			)}
		</div>
	)
}
