import { useEffect, useMemo, useState } from 'react'

import type { PoolProgress, UserInfo } from '@/api/analytics'
import { analyticsApi } from '@/api/analytics'
import type { PoolOut } from '@/api/pools'
import { poolsApi } from '@/api/pools'

export const useAnalytics = () => {
	const [pools, setPools] = useState<PoolOut[]>([])
	const [poolsProgress, setPoolsProgress] = useState<PoolProgress[]>([])
	const [users, setUsers] = useState<UserInfo[]>([])
	const [loading, setLoading] = useState(false)
	const [error, setError] = useState<string | null>(null)
	const [search, setSearch] = useState('')
	const [poolFilter, setPoolFilter] = useState('all')

	useEffect(() => {
		const load = async () => {
			setLoading(true)
			setError(null)
			try {
				const [allPools, progress, usersInfo] = await Promise.all([
					poolsApi.getAll().catch(() => []),
					analyticsApi.getPoolsProgress().catch(() => []),
					analyticsApi.getUsersInfo().catch(() => [])
				])
				setPools(allPools)
				setPoolsProgress(progress)
				setUsers(usersInfo)
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

	const filteredUsers = useMemo(() => {
		if (!search) return users
		const q = search.toLowerCase()
		return users.filter(u =>
			`${u.last_name} ${u.first_name} ${u.middle_name}`
				.toLowerCase()
				.includes(q)
		)
	}, [users, search])

	const filteredProgress = useMemo(() => {
		if (poolFilter === 'all') return poolsProgress
		return poolsProgress.filter(p => String(p.pool_id) === poolFilter)
	}, [poolsProgress, poolFilter])

	return {
		pools,
		poolsProgress: filteredProgress,
		users: filteredUsers,
		loading,
		error,
		search,
		setSearch,
		poolFilter,
		setPoolFilter,
		poolOptions
	}
}
