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
		type: string
		bbox: [number, number, number, number]
		area: number
		iscrowd: number
		segmentation: number[][]
	}>
}

export interface VerificationAnnotation {
	type: 'verification'
	is_correct: boolean
}

export type Annotation = CocoAnnotation | VerificationAnnotation

export const assignmentsApi = {
	getNext: async (poolId: number): Promise<AssignmentOut | null> => {
		try {
			const { data, status } = await apiClient.post<AssignmentOut>(
				'/assignments/next',
				null,
				{
					params: { pool_id: poolId },
					validateStatus: status => status === 201 || status === 404
				}
			)
			if (status === 404) return null
			return data
		} catch (err) {
			if (axios.isAxiosError(err) && (err.response?.status === 404 || err.response?.status === 500)) {
				return null
			}
			throw err
		}
	},

	submit: (assignmentId: number, annotation: Annotation) =>
		apiClient
			.patch<AssignmentOut>(`/assignments/${assignmentId}`, { annotation })
			.then(r => r.data),

	getMyAssignments: async (): Promise<AssignmentOut[]> => {
		try {
			const { data } = await apiClient.get<AssignmentOut[]>('/assignments/my')
			return data
		} catch (err) {
			if (axios.isAxiosError(err) && (err.response?.status === 404 || err.response?.status === 500)) {
				return []
			}
			throw err
		}
	}
}
