import { Outlet } from 'react-router-dom'

import { Sidebar } from '@/components/Sidebar/Sidebar'
import {
	bottomItems,
	customerNavigationItems
} from '@/components/Sidebar/Sidebar.data'

import styles from './MainLayout.module.scss'

export const CustomerLayout = () => (
	<div className={styles.layout}>
		<Sidebar navItems={customerNavigationItems} bottomItems={bottomItems} />
		<main className={styles.content}>
			<Outlet />
		</main>
	</div>
)
