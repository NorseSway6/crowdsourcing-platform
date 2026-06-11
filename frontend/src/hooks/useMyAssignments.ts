import { useEffect, useState } from 'react'

import type { AssignmentStatus } from '@/api/assignments'

import { DEMO_ASSIGNMENTS } from '@/mock/demo'
import type { ActiveAssignment } from '@/services/assignment.service'

interface UseMyAssignmentsReturn {
	items: ActiveAssignment[]
	loading: boolean
	error: string | null
}

export const useMyAssignments = (
	filterStatus?: AssignmentStatus
): UseMyAssignmentsReturn => {
	const [items, setItems] = useState<ActiveAssignment[]>([])

	useEffect(() => {
		const filtered = filterStatus
			? DEMO_ASSIGNMENTS.filter(a => a.assignment.status === filterStatus)
			: DEMO_ASSIGNMENTS
		setItems(filtered)
	}, [filterStatus])

	return { items, loading: false, error: null }
}
