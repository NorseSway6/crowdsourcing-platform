import { apiClient } from './client'

export interface DatasetOut {
	dataset_id: number
	name: string
	domain: string
	owner_id: string
	created_at: string
}

export interface TaskOut {
	task_id: number
	pool_id: number
	dataset_id: number
	image_url: string
	created_at: string
}

export const datasetsApi = {
	create: (ownerId: string, data: { name: string; domain: string }) =>
		apiClient
			.post<DatasetOut>('/datasets/', data, { params: { owner_id: ownerId } })
			.then(r => r.data),

	upload: (datasetId: number, files: File[]) => {
		const formData = new FormData()
		files.forEach(file => formData.append('files', file))
		return apiClient
			.post<TaskOut[]>(`/datasets/${datasetId}/upload`, formData, {
				headers: { 'Content-Type': 'multipart/form-data' }
			})
			.then(r => r.data)
	},

	export: (datasetId: number, formatType: 'coco') =>
		apiClient
			.get(`/datasets/${datasetId}/export`, {
				params: { format_type: formatType },
				responseType: 'blob'
			})
			.then(r => r.data)
}
