import { apiClient } from './client'

export type UserRole = 'STUDENT' | 'CUSTOMER' | 'ADMIN'

export interface UserProfile {
	last_name: string
	first_name: string
	middle_name: string
	group: string
	institution: string
	skills: string[]
}

export interface AuthUser {
	user_id: string
	email: string
	role: UserRole
	user_profile: UserProfile | null
	created_at: string
	is_active: boolean
}

export interface Tokens {
	access_token: string
	refresh_token: string
	token_type: string
}

export const authApi = {
	register: (data: {
		email: string
		password: string
		role: UserRole
		user_profile: Partial<UserProfile>
	}) =>
		apiClient
			.post<{ user: AuthUser; tokens: Tokens }>('/auth/register', data)
			.then(r => r.data),

	login: (email: string, password: string) =>
		apiClient
			.post<Tokens>('/auth/login', { email, password })
			.then(r => r.data),

	logout: (refreshToken: string) =>
		apiClient
			.post('/auth/logout', { refresh_token: refreshToken })
			.then(r => r.data),

	refresh: (refreshToken: string) =>
		apiClient
			.post<Tokens>('/auth/update_tokens', { refresh_token: refreshToken })
			.then(r => r.data)
}
