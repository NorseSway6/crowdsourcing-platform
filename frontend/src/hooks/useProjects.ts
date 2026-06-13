import { useEffect, useState } from 'react'

import { analyticsApi } from '@/api/analytics'
import type { PipelineOut } from '@/api/pipelines'
import { pipelinesApi } from '@/api/pipelines'

import { useAuth } from './useAuth'

export interface PipelineWithStats extends PipelineOut {
	completedCount: number
	totalCount: number
}

export const useProjects = () => {
	const [projects, setProjects] = useState<PipelineWithStats[]>([])
	const [loading, setLoading] = useState(false)
	const [error, setError] = useState<string | null>(null)

	const { user } = useAuth()

	useEffect(() => {
		const load = async () => {
			setLoading(true)
			try {
				if (!user) return

				const [pipelines, progress] = await Promise.all([
					pipelinesApi.getMy(),
					analyticsApi.getPoolsProgress().catch(() => [])
				])

				const withStats = pipelines.map(pipeline => {
					const poolIds = pipeline.pools.map(p => p.pool_id)
					const poolProgress = progress.filter(p =>
						poolIds.includes(p.pool_id)
					)
					return {
						...pipeline,
						completedCount: poolProgress.reduce(
							(sum, p) => sum + p.completed_tasks,
							0
						),
						totalCount: poolProgress.reduce(
							(sum, p) => sum + p.total_tasks,
							0
						)
					}
				})

				setProjects(withStats)
			} catch {
				setError('Не удалось загрузить проекты')
			} finally {
				setLoading(false)
			}
		}
		load()
	}, [user])

	return { projects, loading, error }
}
