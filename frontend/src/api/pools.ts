import { apiClient } from './client'
import type { PoolStatus, PoolType } from './pipelines'

export interface PoolOut {
	pool_id: number
	pipeline_id: number
	points: number
	skills: string[]
	pool_type: PoolType
	target_institution: string | null
	tasks_limit: number
	time_limit: number
	overlap: number
	order: number
	created_at: string
	status: PoolStatus
}

export interface PoolFilters {
	skills?: string[]
	min_points?: number
	max_points?: number
	institution?: string
}

export const poolsApi = {
	getAll: (filters?: PoolFilters) =>
		apiClient.get<PoolOut[]>('/pools/', { params: filters }).then(r => r.data),

	getById: (poolId: number) =>
		apiClient.get<PoolOut>(`/pools/${poolId}`).then(r => r.data), 
}
