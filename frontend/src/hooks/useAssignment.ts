import { useCallback, useState } from 'react'

import type { CocoAnnotation } from '@/api/assignments'

import { DEMO_ASSIGNMENTS } from '@/mock/demo'
import type { ActiveAssignment } from '@/services/assignment.service'

interface UseAssignmentReturn {
	current: ActiveAssignment | null
	loading: boolean
	error: string | null
	fetchNext: () => void
	submit: (annotation: CocoAnnotation) => Promise<void>
}

let currentDemoIndex = 0

export const useAssignment = (): UseAssignmentReturn => {
	const available = DEMO_ASSIGNMENTS.filter(
		a => a.assignment.status === 'IN_PROGRESS'
	)
	const [current, setCurrent] = useState<ActiveAssignment | null>(
		available[0] ?? null
	)
	const [loading, setLoading] = useState(false)
	const [error, setError] = useState<string | null>(null)

	const fetchNext = useCallback(() => {
		currentDemoIndex++
		const next = available[currentDemoIndex]
		if (!next) {
			setCurrent(null)
			setError('Все задания выполнены!')
			return
		}
		setCurrent(next)
	}, [available])

	const submit = useCallback(
		async (annotation: CocoAnnotation) => {
			if (!current) return
			setLoading(true)
			console.log(
				'COCO annotation отправлена:',
				JSON.stringify(annotation, null, 2)
			)
			await new Promise(r => setTimeout(r, 600))
			setLoading(false)
			fetchNext()
		},
		[current, fetchNext]
	)

	return { current, loading, error, fetchNext, submit }
}
