import axios from 'axios'
import { useCallback, useEffect, useState } from 'react'

import type { VerificationAnnotation } from '@/api/assignments'

import { useAuth } from './useAuth'
import type { ActiveAssignment } from '@/services/assignment.service'
import { assignmentService } from '@/services/assignment.service'
import { poolService } from '@/services/pool.service'

interface UseVerificationReturn {
	current: ActiveAssignment | null
	loading: boolean
	error: string | null
	tasksFinished: boolean
	fetchNext: () => void
	submit: (isCorrect: boolean) => Promise<void>
}

export const useVerification = (): UseVerificationReturn => {
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
					poolType: 'VERIFICATION',
					institution: user.user_profile?.institution
				})

				if (!pool) {
					const hasInstitution = Boolean(user.user_profile?.institution?.trim())
					setError(
						hasInstitution
							? 'Нет доступных пулов верификации. Проверьте, что институт совпадает с проектом'
							: 'Нет доступных пулов верификации. Укажите институт в профиле'
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
		async (isCorrect: boolean) => {
			if (!current || !poolId) return
			setLoading(true)
			setError(null)

			try {
				const annotation: VerificationAnnotation = {
					type: 'verification',
					is_correct: isCorrect
				}
				await assignmentService.submitVerification(
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
					setError('Ошибка валидации. Попробуйте снова')
					return
				}
				setError('Ошибка при отправке верификации')
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
