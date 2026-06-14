import type { LucideIcon } from 'lucide-react'
import {
	BarChart2,
	Bell,
	Briefcase,
	CircleHelp,
	ClipboardList,
	Clock3,
	LogOut,
	PlusSquare,
	Shield,
	User
} from 'lucide-react'

export interface SidebarItem {
	label: string
	path?: string
	icon: LucideIcon
	action?: 'logout'
	disabled?: boolean
}

export const navigationItems: SidebarItem[] = [
	{ label: 'Задания', path: '/tasks', icon: ClipboardList },
	{ label: 'В работе', path: '/in-progress', icon: Briefcase },
	{ label: 'Верификация', path: '/verification', icon: Shield },
	{ label: 'На проверке', path: '/review', icon: Clock3 },
	{ label: 'Профиль', path: '/profile', icon: User }
]

export const customerNavigationItems: SidebarItem[] = [
	{ label: 'Создать задание', path: '/customer/create', icon: PlusSquare },
	{ label: 'Проекты', path: '/customer/projects', icon: Briefcase },
	{ label: 'Аналитика', path: '/customer/analytics', icon: BarChart2 },
	{ label: 'К проверке', path: '/customer/review', icon: Clock3 },
	{ label: 'Профиль', path: '/customer/profile', icon: User }
]

export const bottomItems: SidebarItem[] = [
	{ label: 'Поддержка', icon: CircleHelp, disabled: true },
	{ label: 'Уведомления', icon: Bell, disabled: true },
	{ label: 'Выйти из аккаунта', icon: LogOut, action: 'logout' }
]
