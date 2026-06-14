import { Navigate } from 'react-router-dom'

import { PageLoader } from '@/components/PageLoader'

import { useAuth } from '../hooks'

interface Props {
	children: React.ReactNode
	role?: string
}

export const PrivateRoute = ({ children, role }: Props) => {
	const { user, loading } = useAuth()

	if (loading) return <PageLoader fullscreen />
	if (!user) return <Navigate to='/login' replace />

	if (role && user.role !== role) {
		if (user.role === 'CUSTOMER') {
			return <Navigate to='/customer' replace />
		}

		return <Navigate to='/tasks' replace />
	}

	return <>{children}</>
}
