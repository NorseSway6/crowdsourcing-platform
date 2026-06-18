import axios from 'axios'
import { useState } from 'react'

import { datasetsApi } from '@/api/datasets'
import { pipelinesApi } from '@/api/pipelines'

export interface CreatePipelineParams {
	name: string
	files: File[]
	categories: string[]
	points: number
	tasksLimit: number
	timeLimit: number
	institution?: string
}

const getErrorMessage = (err: unknown): string => {
	if (axios.isAxiosError(err)) {
		const detail = err.response?.data?.detail
		if (typeof detail === 'string') return detail
		if (Array.isArray(detail)) {
			return detail.map((d: { msg?: string }) => d.msg).filter(Boolean).join(', ')
		}
		const errorCode = err.response?.data?.error_code
		if (errorCode === 'categories_not_found') {
			return 'Указанные категории не найдены в системе'
		}
	}
	return 'Не удалось создать проект'
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
			const dataset = await datasetsApi.create({
				name: params.name,
				domain: 'general',
				categories: params.categories
			})

			const uploadJob = await datasetsApi.upload(dataset.dataset_id, params.files)
			await datasetsApi.waitForUpload(uploadJob.job_id)

			await pipelinesApi.create({
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
		} catch (err) {
			setError(getErrorMessage(err))
		} finally {
			setLoading(false)
		}
	}

	return { loading, error, success, create }
}
