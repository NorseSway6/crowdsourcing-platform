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

export const assignmentsApi = {
	getAll: () =>
		apiClient.get<AssignmentOut[]>('/assignments/').then(r => r.data),

	getNext: (userId: string, poolId: number) =>
		apiClient
			.post<AssignmentOut>('/assignments/next', null, {
				params: { user_id: userId, pool_id: poolId }
			})
			.then(r => r.data),

	submit: (assignmentId: number, userId: string, annotation: Annotation) =>
		apiClient
			.patch<AssignmentOut>(
				`/assignments/${assignmentId}`,
				{ annotation },
				{ params: { user_id: userId } }
			)
			.then(r => r.data),

	getMyAssignments: (userId: string) =>
		apiClient
			.get<AssignmentOut[]>('/assignments/my', { params: { user_id: userId } })
			.then(r => r.data),

	getMyCompleted: (userId: string) =>
		apiClient
			.get<
				AssignmentOut[]
			>('/assignments/my/completed', { params: { user_id: userId } })
			.then(r => r.data)
}
