import { useEffect, useState } from 'react'

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
				// TODO: переделать на auth
				const TEMP_USER_ID = '5ca80a4b-31f5-42f8-8579-cb4b5cbc74a2'
				
				const me = await apiClient
					.get<UserMe>('/users/me', { params: { id: TEMP_USER_ID } })
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
