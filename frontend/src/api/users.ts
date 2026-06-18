import { apiClient } from './client'

import type { UserProfile } from './auth'

export interface UpdateProfileInput {
	last_name: string
	first_name: string
	middle_name?: string
	group?: string
	institution?: string
	skills?: string[]
}

export const usersApi = {
	getMe: () => apiClient.get('/users/me').then(r => r.data),

	updateProfile: (data: UpdateProfileInput) =>
		apiClient.patch('/users/me/profile', data).then(r => r.data)
}

export type { UserProfile }
