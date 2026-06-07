import type { LucideIcon } from 'lucide-react'
import {
	BarChart2,
	Bell,
	Briefcase,
	CircleHelp,
	ClipboardList,
	Clock3,
	LogOut,
	PlusSquare
} from 'lucide-react'

export interface SidebarItem {
	label: string
	path?: string
	icon: LucideIcon
}

export const navigationItems: SidebarItem[] = [
	{ label: 'Задания', path: '/tasks', icon: ClipboardList },
	{ label: 'В работе', path: '/in-progress', icon: Briefcase },
	{ label: 'На проверке', path: '/review', icon: Clock3 }
]

export const customerNavigationItems: SidebarItem[] = [
	{ label: 'Создать задание', path: '/customer/create', icon: PlusSquare },
	{ label: 'Проекты', path: '/customer/projects', icon: Briefcase },
	{ label: 'Аналитика', path: '/customer/analytics', icon: BarChart2 },
	{ label: 'К проверке', path: '/customer/review', icon: Clock3 }
]

export const bottomItems: SidebarItem[] = [
	{ label: 'Поддержка', icon: CircleHelp },
	{ label: 'Уведомления', icon: Bell },
	{ label: 'Выйти из аккаунта', icon: LogOut }
]
