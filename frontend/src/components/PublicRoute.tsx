import { Navigate } from 'react-router-dom'

import { PageLoader } from '@/components/PageLoader'

import { useAuth } from '../hooks'

interface Props {
	children: React.ReactNode
}

export const PublicRoute = ({ children }: Props) => {
	const { user, loading } = useAuth()

	if (loading) return <PageLoader fullscreen />

	if (user) {
		return (
			<Navigate
				to={user.role === 'CUSTOMER' ? '/customer' : '/tasks'}
				replace
			/>
		)
	}

	return <>{children}</>
}
