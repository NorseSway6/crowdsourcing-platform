import { createContext } from 'react'

import type { AuthUser, UserRole } from '@/api/auth'

export interface AuthContextValue {
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

export const AuthContext = createContext<AuthContextValue | null>(null)
