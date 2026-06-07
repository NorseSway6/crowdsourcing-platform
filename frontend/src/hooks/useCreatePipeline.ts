import { useState } from 'react'

import { datasetsApi } from '@/api/datasets'
import { pipelinesApi } from '@/api/pipelines'

export interface CreatePipelineParams {
	ownerId: string
	name: string
	files: File[]
	points: number
	tasksLimit: number
	timeLimit: number
	institution?: string
}

export const useCreatePipeline = () => {
	const [loading, setLoading] = useState(false)
	const [error, setError] = useState<string | null>(null)
	const [success, setSuccess] = useState(false)

	const create = async (params: CreatePipelineParams) => {
		setLoading(true)
		setError(null)
		setSuccess(false)
		try {
			const dataset = await datasetsApi.create(params.ownerId, {
				name: params.name,
				domain: 'general'
			})

			await datasetsApi.upload(dataset.dataset_id, params.files)

			await pipelinesApi.create(params.ownerId, {
				name: params.name,
				dataset_id: dataset.dataset_id,
				limit: params.files.length,
				pools: [
					{
						points: params.points,
						skills: [],
						pool_type: 'ANNOTATION',
						target_institution: params.institution,
						tasks_limit: params.tasksLimit,
						time_limit: params.timeLimit,
						order: 1
					},
					{
						points: Math.floor(params.points / 2),
						skills: [],
						pool_type: 'VERIFICATION',
						target_institution: params.institution,
						tasks_limit: params.tasksLimit,
						time_limit: params.timeLimit,
						order: 2
					}
				]
			})

			setSuccess(true)
		} catch {
			setError('Не удалось создать проект')
		} finally {
			setLoading(false)
		}
	}

	return { loading, error, success, create }
}
