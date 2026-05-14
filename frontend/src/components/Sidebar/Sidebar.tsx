import { NavLink } from 'react-router-dom'

import { bottomItems, navigationItems } from './Sidebar.data'
import styles from './Sidebar.module.scss'

export const Sidebar = () => (
	<aside className={styles.sidebar}>
		<nav className={styles.nav}>
			{navigationItems.map(item => {
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
					>
						<Icon size={20} />
						<span>{item.label}</span>
					</a>
				)
			})}
		</div>
	</aside>
)
