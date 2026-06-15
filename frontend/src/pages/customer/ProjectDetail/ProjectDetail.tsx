import { ArrowLeft } from 'lucide-react'
import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'

import { type PoolProgress, type UserInfo, analyticsApi } from '@/api/analytics'
import type { PipelineOut } from '@/api/pipelines'
import { pipelinesApi } from '@/api/pipelines'
import { type PoolOut, poolsApi } from '@/api/pools'

import styles from './ProjectDetail.module.scss'

interface ProjectData {
	pipeline: PipelineOut
	pools: PoolOut[]
	poolProgress: PoolProgress[]
	users: UserInfo[]
}

export const ProjectDetailPage = () => {
	const { id } = useParams<{ id: string }>()
	const navigate = useNavigate()
	const [data, setData] = useState<ProjectData | null>(null)
	const [loading, setLoading] = useState(true)
	const [error, setError] = useState<string | null>(null)

	useEffect(() => {
		const load = async () => {
			if (!id) return
			setLoading(true)
			try {
				const pipelineId = Number(id)

				const [pipelines, progress, users] = await Promise.all([
					pipelinesApi.getMy(),
					analyticsApi
						.getPoolsProgress({ pipeline_id: pipelineId })
						.catch(() => []),
					analyticsApi.getUsersInfo().catch(() => [])
				])

				const pipeline = pipelines.find(p => p.pipeline_id === pipelineId)
				if (!pipeline) {
					setError('Проект не найден')
					return
				}

				const poolIds = pipeline.pools.map(p => p.pool_id)
				const pools = await Promise.all(
					poolIds.map(pid => poolsApi.getById(pid).catch(() => null))
				)

				const poolProgress = progress.filter(p => poolIds.includes(p.pool_id))

				setData({
					pipeline,
					pools: pools.filter(Boolean) as PoolOut[],
					poolProgress,
					users
				})
			} catch {
				setError('Не удалось загрузить данные проекта')
			} finally {
				setLoading(false)
			}
		}
		load()
	}, [id])

	if (loading) {
		return (
			<div className={styles.page}>
				<div className={styles.empty}>Загрузка...</div>
			</div>
		)
	}

	if (error || !data) {
		return (
			<div className={styles.page}>
				<div className={styles.empty}>{error || 'Проект не найден'}</div>
			</div>
		)
	}

	const { pipeline, pools, poolProgress } = data

	const totalCompleted = poolProgress.reduce((s, p) => s + p.completed_tasks, 0)
	const totalTasks = poolProgress.reduce((s, p) => s + p.total_tasks, 0)
	const progressPercent =
		totalTasks > 0 ? Math.round((totalCompleted / totalTasks) * 100) : 0

	return (
		<div className={styles.page}>
			<button
				className={styles.backBtn}
				onClick={() => navigate('/customer/projects')}
			>
				<ArrowLeft size={18} /> Назад к проектам
			</button>

			<h1 className={styles.pageTitle}>{pipeline.name}</h1>

			<div className={styles.statsRow}>
				<div className={styles.statCard}>
					<div className={styles.statValue}>{pipeline.limit}</div>
					<div className={styles.statLabel}>Всего задач</div>
				</div>
				<div className={styles.statCard}>
					<div className={styles.statValue}>{totalCompleted}</div>
					<div className={styles.statLabel}>Выполнено</div>
				</div>
				<div className={styles.statCard}>
					<div className={styles.statValue}>{progressPercent}%</div>
					<div className={styles.statLabel}>Прогресс</div>
				</div>
				<div className={styles.statCard}>
					<div className={styles.statValue}>{pools.length}</div>
					<div className={styles.statLabel}>Пулов</div>
				</div>
			</div>

			<div className={styles.section}>
				<h2 className={styles.sectionTitle}>Пулы проекта</h2>
				<div className={styles.poolList}>
					{pools.map(pool => {
						const progress = poolProgress.find(p => p.pool_id === pool.pool_id)
						return (
							<div key={pool.pool_id} className={styles.poolCard}>
								<div className={styles.poolHeader}>
									<span className={styles.poolType}>
										{pool.pool_type === 'ANNOTATION'
											? 'Разметка'
											: 'Верификация'}
									</span>
									<span
										className={`${styles.poolStatus} ${styles[pool.status.toLowerCase()]}`}
									>
										{pool.status === 'OPEN' ? 'Открыт' : 'Завершён'}
									</span>
								</div>
								<div className={styles.poolInfo}>
									<span>Очки: {pool.points}</span>
									<span>Лимит: {pool.tasks_limit} на студента</span>
									<span>Время: {pool.time_limit} сек</span>
								</div>
								{progress && (
									<div className={styles.poolProgress}>
										<div className={styles.progressBar}>
											<div
												className={styles.progressFill}
												style={{ width: `${progress.progress_percentage}%` }}
											/>
										</div>
										<span className={styles.progressText}>
											{progress.completed_tasks} / {progress.total_tasks} задач
										</span>
									</div>
								)}
							</div>
						)
					})}
				</div>
			</div>
		</div>
	)
}
