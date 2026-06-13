import { Navigate } from 'react-router-dom'

import { useAuth } from '../hooks'

interface Props {
	children: React.ReactNode
}

export const PublicRoute = ({ children }: Props) => {
	const { user, loading } = useAuth()

	if (loading) return <div>Загрузка...</div>

	if (user) {
		return <Navigate to='/' replace />
	}

	return <>{children}</>
}
