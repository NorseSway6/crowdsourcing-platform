import { useCallback, useEffect, useState } from 'react'

import type { CocoItem } from '@/utils/coco'

import { apiClient } from '@/api/client'

import type { ActiveAssignment } from '@/services/assignment.service'
import { assignmentService } from '@/services/assignment.service'
import { poolService } from '@/services/pool.service'

interface UserMe {
	user_id: string
	email: string
	role: string
	profile: {
		skills: string[]
	}
}

interface UseAssignmentReturn {
	current: ActiveAssignment | null
	loading: boolean
	error: string | null
	fetchNext: () => void
	submit: (annotation: CocoItem[]) => Promise<void>
}

export const useAssignment = (): UseAssignmentReturn => {
	const [current, setCurrent] = useState<ActiveAssignment | null>(null)
	const [loading, setLoading] = useState(false)
	const [error, setError] = useState<string | null>(null)

	const [userId, setUserId] = useState<string | null>(null)
	const [poolId, setPoolId] = useState<number | null>(null)

	const fetchNext = useCallback(async (uid: string, pid: number) => {
		setLoading(true)
		setError(null)

		try {
			const next = await assignmentService.getNext(uid, pid)
			setCurrent(next)
		} catch {
			setError('Нет доступных задач в пуле')
		} finally {
			setLoading(false)
		}
	}, [])

	useEffect(() => {
		const init = async () => {
			setLoading(true)
			try {
				// TODO: вынести в auth
				const TEMP_USER_ID = '5ca80a4b-31f5-42f8-8579-cb4b5cbc74a2'
				
				const me = await apiClient
					.get<UserMe>('/users/me', { params: { id: TEMP_USER_ID } })
					.then(r => r.data)
				const userSkills = me.profile.skills

				const pool = await poolService.findEligiblePool(userSkills)
				if (!pool) {
					setError('Нет доступных пулов для вашего профиля')
					return
				}

				setUserId(me.user_id)
				setPoolId(pool.pool_id)

				await fetchNext(me.user_id, pool.pool_id)
			} catch {
				setError('Не удалось загрузить профиль пользователя')
			} finally {
				setLoading(false)
			}
		}

		init()
	}, [fetchNext])

	const submit = useCallback(
		async (annotation: CocoItem[]) => {
			if (!current || !userId || !poolId) return
			setLoading(true)
			setError(null)

			try {
				await assignmentService.submit(
					current.assignment.assignment_id,
					userId,
					annotation
				)
				try {
					await fetchNext(userId, poolId)
				} catch {
					setCurrent(null)
					setError('Все задания выполнены!')
				}
			} catch {
				setError('Ошибка при отправке разметки')
			} finally {
				setLoading(false)
			}
		},
		[current, userId, poolId, fetchNext]
	)

	return {
		current,
		loading,
		error,
		fetchNext: () => {
			if (userId && poolId) fetchNext(userId, poolId)
		},
		submit
	}
}
