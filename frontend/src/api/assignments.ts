import type { CocoItem } from '@/utils/coco'

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
	annotation: Record<string, unknown>
	status: AssignmentStatus
	started_at: string
	completed_at: string | null
}

export interface CocoAnnotation {
	images: Array<{ id: number; file_name: string }>
	annotations: Array<
		| {
				id: number
				image_id: number
				category_id: number
				bbox: [number, number, number, number]
				type: 'bbox'
		  }
		| {
				id: number
				image_id: number
				category_id: number
				segmentation: number[][]
				type: 'polygon'
		  }
		| {
				id: number
				image_id: number
				category_id: number
				point: [number, number]
				type: 'point'
		  }
	>
	categories: Array<{ id: number; name: string }>
}

export const assignmentsApi = {
	getNext: (userId: string, poolId: number) =>
		apiClient
			.post<AssignmentOut>('/assignments/next', null, {
				params: { user_id: userId, pool_id: poolId }
			})
			.then(r => r.data),

	submit: (assignmentId: number, userId: string, annotation: CocoItem[]) =>
		apiClient
			.patch<AssignmentOut>(
				`/assignments/${assignmentId}`,
				{ annotation },
				{ params: { user_id: userId } }
			)
			.then(r => r.data),

	updateStatus: (
		assignmentId: number,
		userId: string,
		status: AssignmentStatus
	) =>
		apiClient
			.patch<AssignmentOut>(`/assignments/${assignmentId}/status`, null, {
				params: { user_id: userId, status }
			})
			.then(r => r.data),

	getMyAssignments: (userId: string) =>
		apiClient
			.get<AssignmentOut[]>('/assignments/my', { params: { user_id: userId } })
			.then(r => r.data)
}
