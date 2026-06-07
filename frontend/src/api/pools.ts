import { apiClient } from './client'

export interface PoolOut {
	pool_id: number
	points: number
	overlap: number
	is_active: boolean
	created_at: string
	skills: string[]
}

export interface CreatePoolInput {
	points: number
	skills: string[]
	overlap: number
	dataset_id: number
	limit: number
}

export const poolsApi = {
	getAll: () => apiClient.get<PoolOut[]>('/pools/').then(r => r.data),

	getById: (poolId: number) =>
		apiClient.get<PoolOut>(`/pools/${poolId}`).then(r => r.data),

	create: (data: CreatePoolInput) =>
		apiClient.post<PoolOut>('/pools/', data).then(r => r.data)
}
