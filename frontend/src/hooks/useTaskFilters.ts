import { useMemo, useState } from 'react'

import type { Task } from '@/types'

export type SortOption = 'newest' | 'oldest'

export interface FilterOption {
	id: string
	label: string
	count: number
}

export const useTaskFilters = (tasks: Task[]) => {
	const [sort, setSort] = useState<SortOption>('newest')
	const [selectedPools, setSelectedPools] = useState<Set<string>>(new Set())

	const poolOptions = useMemo<FilterOption[]>(() => {
		const counts = new Map<number, number>()
		for (const task of tasks) {
			counts.set(task.pool_id, (counts.get(task.pool_id) ?? 0) + 1)
		}
		return [...counts.entries()]
			.sort(([a], [b]) => a - b)
			.map(([poolId, count]) => ({
				id: String(poolId),
				label: `Категория ${poolId}`,
				count
			}))
	}, [tasks])

	const filtered = useMemo(() => {
		let result = [...tasks]

		if (selectedPools.size > 0) {
			result = result.filter(task => selectedPools.has(String(task.pool_id)))
		}

		result.sort((a, b) => {
			const da = new Date(a.created_at).getTime()
			const db = new Date(b.created_at).getTime()
			return sort === 'newest' ? db - da : da - db
		})

		return result
	}, [tasks, sort, selectedPools])

	const togglePool = (poolId: string) => {
		setSelectedPools(prev => {
			const next = new Set(prev)
			if (next.has(poolId)) next.delete(poolId)
			else next.add(poolId)
			return next
		})
	}

	const resetFilters = () => setSelectedPools(new Set())

	return {
		filtered,
		sort,
		setSort,
		poolOptions,
		selectedPools,
		togglePool,
		resetFilters,
		hasActiveFilters: selectedPools.size > 0
	}
}
