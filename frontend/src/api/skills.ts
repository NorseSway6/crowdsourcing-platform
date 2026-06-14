import { apiClient } from './client'

export const skillsApi = {
	getAll: async (): Promise<string[]> => {
		try {
			const { data } = await apiClient.get<string[]>('/skills/')
			return data
		} catch {
			return []
		}
	}
}
