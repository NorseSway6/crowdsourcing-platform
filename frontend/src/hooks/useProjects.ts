import { useEffect, useState } from 'react'

import { TEMP_USER_ID } from '@/config/temp'

import { assignmentsApi } from '@/api/assignments'
import type { PipelineOut } from '@/api/pipelines'
import { pipelinesApi } from '@/api/pipelines'

export interface PipelineWithStats extends PipelineOut {
	completedCount: number
	totalCount: number
}

export const useProjects = () => {
	const [projects, setProjects] = useState<PipelineWithStats[]>([])
	const [loading, setLoading] = useState(false)
	const [error, setError] = useState<string | null>(null)

	useEffect(() => {
		const load = async () => {
			setLoading(true)
			try {
				const [pipelines, assignments] = await Promise.all([
					pipelinesApi.getMy(TEMP_USER_ID),
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
	}, [])

	return { projects, loading, error }
}
