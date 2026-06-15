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
				<div className={styles.list}>
					{projects.length === 0 ? (
						<div className={styles.empty}>Нет проектов</div>
					) : (
						projects.map(pipeline => (
							<div
								key={pipeline.pipeline_id}
								className={styles.card}
								onClick={() =>
									navigate(`/customer/projects/${pipeline.pipeline_id}`)
								}
							>
								<div className={styles.cardHeader}>
									<span className={styles.cardTitle}>{pipeline.name}</span>
									<span className={styles.cardStats}>
										Студентов выполнило: {pipeline.completedCount}
									</span>
								</div>

								<div className={styles.cardActions}>
									<button
										className={styles.btnAnalytics}
										onClick={e => {
											e.stopPropagation()
											navigate('/customer/analytics')
										}}
									>
										Аналитика проекта
									</button>
									<button
										className={styles.btnReview}
										onClick={e => {
											e.stopPropagation()
											navigate('/customer/review')
										}}
									>
										К проверке
									</button>
								</div>
							</div>
						))
					)}
				</div>
			)}
		</div>
	)
}
