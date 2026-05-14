import { useMemo, useState } from 'react'

import type { Task } from '@/types'

export type SortOption = 'newest' | 'oldest'

export const useTaskFilters = (tasks: Task[]) => {
	const [sort, setSort] = useState<SortOption>('newest')

	const filtered = useMemo(() => {
		return [...tasks].sort((a, b) => {
			const da = new Date(a.created_at).getTime()
			const db = new Date(b.created_at).getTime()
			return sort === 'newest' ? db - da : da - db
		})
	}, [tasks, sort])

	return { filtered, sort, setSort }
}
