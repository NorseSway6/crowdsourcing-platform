import { apiClient } from './client'

export type PoolType = 'ANNOTATION' | 'VERIFICATION'
export type PoolStatus = 'OPEN' | 'COMPLETED'

export interface PoolInPipeline {
	points: number
	skills: string[]
	pool_type: PoolType
	target_institution: string | null
	tasks_limit: number
	time_limit: number
	overlap: number
	pool_id: number
	pipeline_id: number
	order: number
	created_at: string
	status: PoolStatus
}

export interface CreatePoolInput {
	points: number
	skills: string[]
	pool_type: PoolType
	target_institution?: string
	tasks_limit: number
	time_limit: number
	order: number
}

export interface PipelineOut {
	pipeline_id: number
	name: string
	dataset_id: number
	limit: number
	owner_id: string
	pools: PoolInPipeline[]
}

export interface CreatePipelineInput {
	name: string
	dataset_id: number
	limit: number
	pools: CreatePoolInput[]
}

export const pipelinesApi = {
	create: (data: CreatePipelineInput) =>
		apiClient.post<PipelineOut>('/pipelines/', data).then(r => r.data),

	getMy: () =>
		apiClient.get<PipelineOut[]>('/pipelines/my').then(r => r.data)
}
