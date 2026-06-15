import { Outlet } from 'react-router-dom'

import { Sidebar } from '@/components/Sidebar/Sidebar'
import { useVerificationAvailable } from '@/hooks'

import styles from './MainLayout.module.scss'

export const MainLayout = () => {
	const verificationAvailable = useVerificationAvailable()

	return (
		<div className={styles.layout}>
			<Sidebar verificationAvailable={verificationAvailable} />
			<main className={styles.content}>
				<Outlet />
			</main>
		</div>
	)
}
