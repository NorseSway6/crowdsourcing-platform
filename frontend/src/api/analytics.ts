import { apiClient } from './client'

export interface PoolProgress {
	pool_id: number
	pool_type: string
	total_tasks: number
	completed_tasks: number
	progress_percentage: number
}

export interface UserInfo {
	last_name: string
	first_name: string
	middle_name: string
	group: string
	institution: string
	submitted: number
	approved: number
	user_accuracy: number
}

export const analyticsApi = {
	getPoolsProgress: (params?: { pipeline_id?: number; pool_type?: string }) =>
		apiClient
			.get<PoolProgress[]>('/analytics/pools-progress', { params })
			.then(r => r.data),

	getUsersInfo: (params?: {
		first_name?: string
		last_name?: string
		institution?: string
		group?: string
	}) =>
		apiClient
			.get<UserInfo[]>('/analytics/user-info', { params })
			.then(r => r.data)
}
