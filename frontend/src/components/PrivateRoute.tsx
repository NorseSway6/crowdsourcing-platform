import { useAuth } from '../hooks'

interface Props {
	children: React.ReactNode
	role?: string
}

export const PrivateRoute = ({ children }: Props) => {
	const { loading } = useAuth()

	if (loading) return <div>Загрузка...</div>
	// if (!user) return <Navigate to='/login' replace />
	// if (role && user.role !== role) {
	// 	return <Navigate to='/tasks' replace />
	// }

	return <>{children}</>
}
