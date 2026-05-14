import type { LucideIcon } from 'lucide-react'
import { Bell, Briefcase, CircleHelp, ClipboardList, Clock3, LogOut } from 'lucide-react'

export interface SidebarItem {
	label: string
	path?: string
	icon: LucideIcon
}

export const navigationItems: SidebarItem[] = [
	{
		label: 'Задания',
		path: '/tasks',
		icon: ClipboardList
	},
	{
		label: 'В работе',
		path: '/in-progress',
		icon: Briefcase
	},
	{
		label: 'На проверке',
		path: '/review',
		icon: Clock3
	}
]

export const bottomItems: SidebarItem[] = [
	{
		label: 'Поддержка',
		icon: CircleHelp
	},
	{
		label: 'Уведомления',
		icon: Bell
	},
	{
		label: 'Выйти из аккаунта',
		icon: LogOut
	}
]
