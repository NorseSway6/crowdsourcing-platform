import { apiClient } from './client'

export type TaskStatus = 'AVAILABLE' | 'COMPLETED'

export interface TaskOut {
	task_id: number
	pool_id: number
	dataset_id: number
	image_url: string
	created_at: string
	status: TaskStatus
}

export const tasksApi = {
	getById: (taskId: number) =>
		apiClient.get<TaskOut>(`/tasks/${taskId}`).then(r => r.data),

	getAll: () => apiClient.get<TaskOut[]>('/tasks/').then(r => r.data)
}
