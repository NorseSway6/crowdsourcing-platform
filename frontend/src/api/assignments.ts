import axios from 'axios'

import { apiClient } from './client'

export type AssignmentStatus =
	| 'IN_PROGRESS'
	| 'PENDING'
	| 'APPROVED'
	| 'REJECTED'

export interface AssignmentOut {
	assignment_id: number
	task_id: number
	user_id: string
	pool_id: number
	annotation: Record<string, unknown> | null
	status: AssignmentStatus
	started_at: string
	completed_at: string | null
	expires_at: string | null
}

export interface CocoAnnotation {
	type: 'coco'
	items: Array<{
		category_id: number
		type?: string
		bbox: [number, number, number, number]
		area: number
		iscrowd: 0 | 1
		segmentation: number[][]
	}>
}

export interface VerificationAnnotation {
	type: 'verification'
	is_correct: boolean
}

export type Annotation = CocoAnnotation | VerificationAnnotation

const isNotFound = (err: unknown) =>
	axios.isAxiosError(err) && err.response?.status === 404

export const assignmentsApi = {
	getNext: (poolId: number) =>
		apiClient
			.post<AssignmentOut>('/assignments/next', null, {
				params: { pool_id: poolId }
			})
			.then(r => r.data),

	submit: (assignmentId: number, annotation: Annotation) =>
		apiClient
			.patch<AssignmentOut>(`/assignments/${assignmentId}`, { annotation })
			.then(r => r.data),

	getMyAssignments: async (): Promise<AssignmentOut[]> => {
		try {
			const { data } = await apiClient.get<AssignmentOut[]>('/assignments/my')
			return data
		} catch (err) {
			if (isNotFound(err)) return []
			throw err
		}
	},

	getMyCompleted: async (): Promise<AssignmentOut[]> => {
		try {
			const { data } = await apiClient.get<AssignmentOut[]>(
				'/assignments/my/completed'
			)
			return data
		} catch (err) {
			if (isNotFound(err)) return []
			throw err
		}
	}
}
