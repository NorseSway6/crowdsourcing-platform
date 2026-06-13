import { NavLink, useNavigate } from 'react-router-dom'

import { useAuth } from '@/hooks/useAuth'

import type { SidebarItem } from './Sidebar.data'
import {
	bottomItems as defaultBottom,
	navigationItems as defaultNav
} from './Sidebar.data'
import styles from './Sidebar.module.scss'

interface Props {
	navItems?: SidebarItem[]
	bottomItems?: SidebarItem[]
}

export const Sidebar = ({
	navItems = defaultNav,
	bottomItems = defaultBottom
}: Props) => {
	const { logout } = useAuth()
	const navigate = useNavigate()

	const handleBottomClick = async (item: SidebarItem) => {
		if (item.action === 'logout') {
			await logout()
			navigate('/login')
		}
	}

	return (
		<aside className={styles.sidebar}>
			<nav className={styles.nav}>
				{navItems.map(item => {
					const Icon = item.icon
					return (
						<NavLink
							key={item.path}
							to={item.path!}
							className={({ isActive }) =>
								`${styles.navItem} ${isActive ? styles.active : ''}`
							}
						>
							<Icon size={20} />
							<span>{item.label}</span>
						</NavLink>
					)
				})}
			</nav>
			<div className={styles.bottom}>
				{bottomItems.map(item => {
					const Icon = item.icon
					return (
						<a
							key={item.label}
							href='#'
							className={styles.navItem}
							onClick={e => {
								e.preventDefault()
								handleBottomClick(item)
							}}
						>
							<Icon size={20} />
							<span>{item.label}</span>
						</a>
					)
				})}
			</div>
		</aside>
	)
}
