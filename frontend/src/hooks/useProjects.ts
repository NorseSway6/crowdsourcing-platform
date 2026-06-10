import { useEffect, useState } from 'react'

import { assignmentsApi } from '@/api/assignments'
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

				const [pipelines, assignments] = await Promise.all([
					pipelinesApi.getMy(user?.user_id),
					assignmentsApi.getAll()
				])

				const withStats = pipelines.map(pipeline => {
					const poolIds = pipeline.pools.map(p => p.pool_id)
					const pipelineAssignments = assignments.filter(a =>
						poolIds.includes(a.pool_id)
					)
					return {
						...pipeline,
						completedCount: pipelineAssignments.filter(
							a => a.status === 'APPROVED' || a.status === 'PENDING'
						).length,
						totalCount: pipelineAssignments.length
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
