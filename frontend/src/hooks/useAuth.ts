import { useCallback, useEffect, useState } from 'react'

import type { AuthUser, UserRole } from '@/api/auth'
import { authApi } from '@/api/auth'
import { apiClient, clearTokens, setTokens } from '@/api/client'

export const useAuth = () => {
	const [user, setUser] = useState<AuthUser | null>(null)
	const [loading, setLoading] = useState(true)

	const loadUser = useCallback(async () => {
		const token = document.cookie.includes('access_token=')
		if (!token) {
			setLoading(false)
			return
		}
		try {
			const me = await apiClient
				.get<AuthUser>('/users/me', {
					params: { user_id: undefined }
				})
				.then(r => r.data)
			setUser(me)
		} catch {
			clearTokens()
		} finally {
			setLoading(false)
		}
	}, [])

	useEffect(() => {
		loadUser()
	}, [loadUser])

	const login = async (email: string, password: string) => {
		const tokens = await authApi.login(email, password)
		setTokens(tokens.access_token, tokens.refresh_token)
		await loadUser()
	}

	const register = async (data: {
		email: string
		password: string
		role: UserRole
		firstName: string
		lastName: string
	}) => {
		const res = await authApi.register({
			email: data.email,
			password: data.password,
			role: data.role,
			user_profile: {
				first_name: data.firstName,
				last_name: data.lastName,
				middle_name: '',
				group: '',
				institution: '',
				skills: []
			}
		})
		setTokens(res.tokens.access_token, res.tokens.refresh_token)
		setUser(res.user)
	}

	const logout = async () => {
		const refresh = document.cookie
			.split('; ')
			.find(r => r.startsWith('refresh_token='))
			?.split('=')[1]
		if (refresh) await authApi.logout(refresh).catch(() => {})
		clearTokens()
		setUser(null)
	}

	return { user, loading, login, register, logout }
}
