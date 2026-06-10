import { useEffect, useState } from 'react'

import type { AssignmentStatus } from '@/api/assignments'

import { useAuth } from './useAuth'
import type { ActiveAssignment } from '@/services/assignment.service'
import { assignmentService } from '@/services/assignment.service'

interface UseMyAssignmentsReturn {
	items: ActiveAssignment[]
	loading: boolean
	error: string | null
}

export const useMyAssignments = (
	filterStatus?: AssignmentStatus
): UseMyAssignmentsReturn => {
	const [items, setItems] = useState<ActiveAssignment[]>([])
	const [loading, setLoading] = useState(false)
	const [error, setError] = useState<string | null>(null)

	const { user } = useAuth()

	useEffect(() => {
		const load = async () => {
			setLoading(true)
			setError(null)
			try {
				if (!user) return

				const all = await assignmentService.getMyWithTasks(user.user_id)
				const filtered = filterStatus
					? all.filter(a => a.assignment.status === filterStatus)
					: all

				setItems(filtered)
			} catch {
				setError('Не удалось загрузить задания')
			} finally {
				setLoading(false)
			}
		}
		load()
	}, [filterStatus, user])

	return { items, loading, error }
}
