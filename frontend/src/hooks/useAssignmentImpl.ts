import { useCallback, useEffect, useState } from 'react'

import type { CocoAnnotation } from '@/api/assignments'

import { useAuth } from './useAuth'
import type { ActiveAssignment } from '@/services/assignment.service'
import { assignmentService } from '@/services/assignment.service'
import { poolService } from '@/services/pool.service'

interface UseAssignmentReturn {
	current: ActiveAssignment | null
	loading: boolean
	error: string | null
	fetchNext: () => void
	submit: (annotation: CocoAnnotation) => Promise<void>
}

export const useAssignment = (): UseAssignmentReturn => {
	const [current, setCurrent] = useState<ActiveAssignment | null>(null)
	const [loading, setLoading] = useState(false)
	const [error, setError] = useState<string | null>(null)

	const [userId, setUserId] = useState<string | null>(null)
	const [poolId, setPoolId] = useState<number | null>(null)

	const { user } = useAuth()

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
				if (!user) return
				const userSkills = user.user_profile?.skills ?? []
				const pool = await poolService.findEligiblePool(userSkills)
				if (!pool) {
					setError('Нет доступных пулов')
					return
				}
				setUserId(user.user_id)
				setPoolId(pool.pool_id)
				await fetchNext(user.user_id, pool.pool_id)
			} catch {
				setError('Не удалось загрузить профиль пользователя')
			} finally {
				setLoading(false)
			}
		}

		init()
	}, [fetchNext, user])

	const submit = useCallback(
		async (annotation: CocoAnnotation) => {
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
