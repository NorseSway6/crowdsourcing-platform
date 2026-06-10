import { createContext, useContext, useEffect, useState } from 'react'

import type { AuthUser, UserRole } from '@/api/auth'
import { authApi } from '@/api/auth'

interface AuthContextValue {
	user: AuthUser | null
	loading: boolean
	login: (email: string, password: string) => Promise<void>
	register: (data: {
		email: string
		password: string
		role: UserRole
		firstName: string
		lastName: string
	}) => Promise<void>
	logout: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | null>(null)

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
	const [user, setUser] = useState<AuthUser | null>(null)
	const [loading, setLoading] = useState(true)

	// при старте проверяем есть ли токен
	useEffect(() => {
		const token = localStorage.getItem('access_token')
		if (!token) {
			setLoading(false)
			return
		}
		// TODO: GET /users/me для получения данных юзера
		// пока просто помечаем что авторизован
		setLoading(false)
	}, [])

	const login = async (email: string, password: string) => {
		const tokens = await authApi.login(email, password)
		localStorage.setItem('access_token', tokens.access_token)
		localStorage.setItem('refresh_token', tokens.refresh_token)
		// TODO: загрузить профиль юзера после логина
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
		localStorage.setItem('access_token', res.tokens.access_token)
		localStorage.setItem('refresh_token', res.tokens.refresh_token)
		setUser(res.user)
	}

	const logout = async () => {
		const refresh = localStorage.getItem('refresh_token')
		if (refresh) await authApi.logout(refresh)
		localStorage.removeItem('access_token')
		localStorage.removeItem('refresh_token')
		setUser(null)
	}

	return (
		<AuthContext.Provider value={{ user, loading, login, register, logout }}>
			{children}
		</AuthContext.Provider>
	)
}

export const useAuth = () => {
	const ctx = useContext(AuthContext)
	if (!ctx) throw new Error('useAuth must be used within AuthProvider')
	return ctx
}
