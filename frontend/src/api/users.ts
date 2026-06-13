import { apiClient } from './client'

export interface UserProfile {
	last_name: string
	first_name: string
	middle_name: string
	group: string
	institution: string
	skills: string[]
}

export interface UserOut {
	user_id: string
	email: string
	role: string
	profile: UserProfile
	created_at: string
	is_active: boolean
}

export const usersApi = {
	getAll: () => apiClient.get<UserOut[]>('/users/').then(r => r.data),

	getMe: () => apiClient.get<UserOut>('/users/me').then(r => r.data)
}
