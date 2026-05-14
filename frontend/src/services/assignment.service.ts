import type { CocoItem } from '@/utils/coco'

import type { AssignmentOut } from '@/api/assignments'
import { assignmentsApi } from '@/api/assignments'
import type { TaskOut } from '@/api/tasks'
import { tasksApi } from '@/api/tasks'

export interface ActiveAssignment {
	assignment: AssignmentOut
	task: TaskOut
}

export const assignmentService = {
	getNext: async (
		userId: string,
		poolId: number
	): Promise<ActiveAssignment> => {
		const assignment = await assignmentsApi.getNext(userId, poolId)
		const task = await tasksApi.getById(assignment.task_id)
		return { assignment, task }
	},

	submit: async (
		assignmentId: number,
		userId: string,
		annotation: CocoItem[]
	): Promise<AssignmentOut> => {
		return assignmentsApi.submit(assignmentId, userId, annotation)
	},

	getMyWithTasks: async (userId: string): Promise<ActiveAssignment[]> => {
		const assignments = await assignmentsApi.getMyAssignments(userId)
		const withTasks = await Promise.all(
			assignments.map(async assignment => {
				const task = await tasksApi.getById(assignment.task_id)
				return { assignment, task }
			})
		)
		return withTasks
	}
}
