import axios from 'axios'

import type { CocoAnnotation, VerificationAnnotation } from '@/api/assignments'
import type { AssignmentOut } from '@/api/assignments'
import { assignmentsApi } from '@/api/assignments'
import type { TaskOut } from '@/api/tasks'
import { tasksApi } from '@/api/tasks'

export interface ActiveAssignment {
	assignment: AssignmentOut
	task: TaskOut
}

const isAccessDenied = (err: unknown) =>
	axios.isAxiosError(err) &&
	(err.response?.status === 403 || err.response?.data?.error_code === 'role_access_error')

export const assignmentService = {
	getNext: async (poolId: number): Promise<ActiveAssignment | null> => {
		try {
			const assignment = await assignmentsApi.getNext(poolId)
			if (!assignment) return null

			const task = await tasksApi.getById(assignment.task_id)
			return { assignment, task }
		} catch (err) {
			if (isAccessDenied(err)) {
				throw new Error('TASK_ACCESS_DENIED')
			}
			throw err
		}
	},

	submit: async (
		assignmentId: number,
		annotation: CocoAnnotation
	): Promise<AssignmentOut> => {
		return assignmentsApi.submit(assignmentId, annotation)
	},

	submitVerification: async (
		assignmentId: number,
		annotation: VerificationAnnotation
	): Promise<AssignmentOut> => {
		return assignmentsApi.submit(assignmentId, annotation)
	},

	getMyWithTasks: async (): Promise<ActiveAssignment[]> => {
		const assignments = await assignmentsApi.getMyAssignments()
		const withTasks: ActiveAssignment[] = []

		for (const assignment of assignments) {
			try {
				const task = await tasksApi.getById(assignment.task_id)
				withTasks.push({ assignment, task })
			} catch (err) {
				if (isAccessDenied(err)) continue
				if (axios.isAxiosError(err) && err.response?.status === 500) continue
				throw err
			}
		}

		return withTasks
	}
}
