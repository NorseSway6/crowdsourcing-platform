import axios from 'axios'
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
	tasksFinished: boolean
	fetchNext: () => void
	submit: (annotation: CocoAnnotation) => Promise<void>
}

export const useAssignment = (): UseAssignmentReturn => {
	const [current, setCurrent] = useState<ActiveAssignment | null>(null)
	const [loading, setLoading] = useState(false)
	const [error, setError] = useState<string | null>(null)
	const [poolId, setPoolId] = useState<number | null>(null)
	const [tasksFinished, setTasksFinished] = useState(false)

	const { user } = useAuth()

	const fetchNext = useCallback(async (pid: number) => {
		setLoading(true)
		setError(null)
		setTasksFinished(false)

		try {
			const next = await assignmentService.getNext(pid)
			if (!next) {
				setCurrent(null)
				setTasksFinished(true)
				return
			}
			setCurrent(next)
		} catch (err) {
			if (axios.isAxiosError(err) && err.response?.status === 404) {
				setError('Нет доступных задач. Возможно, все задания уже взяты другими студентами')
				setTasksFinished(true)
				return
			}
			setError('Не удалось получить задание')
			console.log(err)
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
					setTasksFinished(true)
					return
				}
				setCurrent(next)
			} catch (err) {
				if (axios.isAxiosError(err) && err.response?.status === 422) {
					setError('Неверный формат разметки. Проверьте фигуры и попробуйте снова')
					return
				}
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
		tasksFinished,
		fetchNext: () => {
			if (poolId && !tasksFinished) fetchNext(poolId)
		},
		submit
	}
}
