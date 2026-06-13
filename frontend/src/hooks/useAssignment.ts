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
	const [poolId, setPoolId] = useState<number | null>(null)

	const { user } = useAuth()

	const fetchNext = useCallback(async (pid: number) => {
		setLoading(true)
		setError(null)

		try {
			const next = await assignmentService.getNext(pid)
			if (!next) {
				setCurrent(null)
				setError('Нет доступных задач в пуле')
				return
			}
			setCurrent(next)
		} catch (err) {
			if (err instanceof Error && err.message === 'TASK_ACCESS_DENIED') {
				setError(
					'Бэкенд не отдаёт задачи студенту. Попросите добавить роль STUDENT на GET /tasks/{task_id}'
				)
				return
			}
			setError('Не удалось получить задание')
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
				const pool = await poolService.findEligiblePool(userSkills, {
					poolType: 'ANNOTATION',
					institution: user.user_profile?.institution
				})

				if (!pool) {
					const hasInstitution = Boolean(user.user_profile?.institution?.trim())
					setError(
						hasInstitution
							? 'Нет доступных пулов разметки. Проверьте, что институт совпадает с проектом'
							: 'Нет доступных пулов. Укажите институт в профиле — он должен совпадать с проектом'
					)
					return
				}

				setPoolId(pool.pool_id)
				await fetchNext(pool.pool_id)
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
			if (!current || !poolId) return
			setLoading(true)
			setError(null)

			try {
				await assignmentService.submit(
					current.assignment.assignment_id,
					annotation
				)
				const next = await assignmentService.getNext(poolId)
				if (!next) {
					setCurrent(null)
					setError('Все задания выполнены!')
					return
				}
				setCurrent(next)
			} catch {
				setError('Ошибка при отправке разметки')
			} finally {
				setLoading(false)
			}
		},
		[current, poolId]
	)

	return {
		current,
		loading,
		error,
		fetchNext: () => {
			if (poolId) fetchNext(poolId)
		},
		submit
	}
}
