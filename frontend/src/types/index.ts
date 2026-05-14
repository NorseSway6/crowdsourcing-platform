export interface Task {
	task_id: number
	pool_id: number
	dataset_id: number
	image_url: string
	created_at: string
}

export type AssignmentStatus = 'IN_PROGRESS' | 'PENDING' | 'APPROVED' | 'REJECTED'

export interface Assignment {
	assignment_id: number
	task_id: number
	user_id: string
	annotation: Record<string, unknown>
	status: AssignmentStatus
	started_at: string
	completed_at: string | null
}

export interface FilterOption {
	label: string
	count: number
}

export interface Filters {
	categories: FilterOption[]
	clients: FilterOption[]
}
