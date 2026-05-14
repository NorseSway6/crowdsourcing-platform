import { Outlet } from 'react-router-dom'

import { Sidebar } from '@/components/Sidebar/Sidebar'

import styles from './MainLayout.module.scss'

export const MainLayout = () => {
	return (
		<div className={styles.layout}>
			<Sidebar />
			<main className={styles.content}>
				<Outlet />
			</main>
		</div>
	)
}
