import { apiClient } from './client'

export interface CategoryOut {
	id: number
	name: string
}

export interface DatasetOut {
	dataset_id: number
	name: string
	domain: string
	owner_id: string
	created_at: string
	categories: CategoryOut[]
}

export interface UploadStatusOut {
	job_id: string
	status: string
	created_count?: number
}

export interface CreateDatasetInput {
	name: string
	domain: string
	categories: string[]
}

const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))

export const datasetsApi = {
	create: (data: CreateDatasetInput) =>
		apiClient.post<DatasetOut>('/datasets/', data).then(r => r.data),

	getCategories: () =>
		apiClient.get<CategoryOut[]>('/datasets/categories').then(r => r.data),

	createCategory: (name: string) =>
		apiClient
			.post<CategoryOut>('/datasets/categories', { name })
			.then(r => r.data),

	upload: (datasetId: number, files: File[]) => {
		const formData = new FormData()
		files.forEach(file => formData.append('files', file))
		return apiClient
			.post<UploadStatusOut>(`/datasets/${datasetId}/upload`, formData, {
				headers: { 'Content-Type': 'multipart/form-data' }
			})
			.then(r => r.data)
	},

	getUploadStatus: (jobId: string) =>
		apiClient
			.get<UploadStatusOut>(`/datasets/upload/status/${jobId}`)
			.then(r => r.data),

	waitForUpload: async (jobId: string, maxAttempts = 60) => {
		for (let i = 0; i < maxAttempts; i++) {
			const status = await datasetsApi.getUploadStatus(jobId)
			if (status.status === 'SUCCESS') return status
			if (status.status === 'FAILURE') {
				throw new Error('Ошибка загрузки файлов')
			}
			await sleep(1000)
		}
		throw new Error('Превышено время ожидания загрузки')
	},

	export: (datasetId: number, formatType: 'coco') =>
		apiClient
			.get(`/datasets/${datasetId}/export`, {
				params: { format_type: formatType },
				responseType: 'blob'
			})
			.then(r => r.data)
}
