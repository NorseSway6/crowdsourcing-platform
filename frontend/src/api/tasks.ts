import { apiClient } from './client'

export interface TaskOut {
	task_id: number
	pool_id: number
	dataset_id: number
	image_url: string
	created_at: string
}

export const tasksApi = {
	getById: (taskId: number) =>
		apiClient.get<TaskOut>(`/tasks/${taskId}`).then(r => r.data)
}
