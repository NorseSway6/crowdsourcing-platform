import { useEffect, useState } from 'react'

import { TEMP_USER_ID } from '@/config/temp'

import type { AssignmentStatus } from '@/api/assignments'
import { apiClient } from '@/api/client'

import type { ActiveAssignment } from '@/services/assignment.service'
import { assignmentService } from '@/services/assignment.service'

interface UserMe {
	user_id: string
}

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

	useEffect(() => {
		const load = async () => {
			setLoading(true)
			setError(null)
			try {
				const me = await apiClient
					.get<UserMe>('/users/me', { params: { user_id: TEMP_USER_ID } })
					.then(r => r.data)

				const all = await assignmentService.getMyWithTasks(me.user_id)
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
	}, [filterStatus])

	return { items, loading, error }
}
