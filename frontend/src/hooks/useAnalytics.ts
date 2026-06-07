import { useEffect, useMemo, useState } from 'react'

import type { AssignmentOut } from '@/api/assignments'
import { assignmentsApi } from '@/api/assignments'
import type { PoolOut } from '@/api/pools'
import { poolsApi } from '@/api/pools'
import type { UserOut } from '@/api/users'
import { usersApi } from '@/api/users'

interface UseAnalyticsReturn {
	assignments: AssignmentOut[]
	pools: PoolOut[]
	users: Record<string, UserOut>
	loading: boolean
	error: string | null
	filtered: AssignmentOut[]
	search: string
	setSearch: (v: string) => void
	poolFilter: string
	setPoolFilter: (v: string) => void
	poolOptions: Array<{ value: string; label: string }>
}

export const useAnalytics = (): UseAnalyticsReturn => {
	const [assignments, setAssignments] = useState<AssignmentOut[]>([])
	const [pools, setPools] = useState<PoolOut[]>([])
	const [users, setUsers] = useState<Record<string, UserOut>>({})
	const [loading, setLoading] = useState(false)
	const [error, setError] = useState<string | null>(null)
	const [search, setSearch] = useState('')
	const [poolFilter, setPoolFilter] = useState('all')

	useEffect(() => {
		const load = async () => {
			setLoading(true)
			setError(null)
			try {
				const [allAssignments, allPools, allUsers] = await Promise.all([
					assignmentsApi.getAll(),
					poolsApi.getAll(),
					usersApi.getAll()
				])
				const usersMap = allUsers.reduce<Record<string, UserOut>>((acc, u) => {
					acc[u.user_id] = u
					return acc
				}, {})
				setAssignments(allAssignments)
				setPools(allPools)
				setUsers(usersMap)
			} catch {
				setError('Не удалось загрузить данные')
			} finally {
				setLoading(false)
			}
		}
		load()
	}, [])

	const poolOptions = [
		{ value: 'all', label: 'Все проекты' },
		...pools.map(p => ({
			value: String(p.pool_id),
			label: `Пул #${p.pool_id}`
		}))
	]

	const filtered = useMemo(() => {
		return assignments.filter(a => {
			const user = users[a.user_id]
			const name = user
				? [
						user.profile.last_name,
						user.profile.first_name,
						user.profile.middle_name
					]
						.filter(Boolean)
						.join(' ')
						.toLowerCase()
				: ''
			if (search && !name.includes(search.toLowerCase())) return false
			return true
		})
	}, [assignments, search, users])

	return {
		assignments,
		pools,
		users,
		loading,
		error,
		filtered,
		search,
		setSearch,
		poolFilter,
		setPoolFilter,
		poolOptions
	}
}
