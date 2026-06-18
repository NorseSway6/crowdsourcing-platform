import { createContext } from 'react'

import type { AuthUser, RegisterData } from '@/api/auth'

export interface AuthContextValue {
	user: AuthUser | null
	loading: boolean
	login: (email: string, password: string) => Promise<void>
	register: (data: RegisterData) => Promise<void>
	logout: () => Promise<void>
	refreshUser: () => Promise<void>
}

export const AuthContext = createContext<AuthContextValue | null>(null)
