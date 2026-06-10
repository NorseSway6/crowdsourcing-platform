import type { ActiveAssignment } from '@/services/assignment.service'

export const DEMO_ASSIGNMENTS: ActiveAssignment[] = [
	{
		assignment: {
			expires_at: null,
			assignment_id: 1,
			task_id: 1,
			user_id: 'demo-user',
			pool_id: 1,
			annotation: {},
			status: 'IN_PROGRESS',
			started_at: new Date().toISOString(),
			completed_at: null
		},
		task: {
			task_id: 1,
			pool_id: 1,
			dataset_id: 1,
			image_url:
				'https://res.cloudinary.com/unix-center/image/upload/c_limit,dpr_3.0,f_auto,fl_progressive,g_center,h_580,q_75,w_906/ctjvjtjfxqavguj60uss.jpg',
			created_at: new Date().toISOString(),
			status: 'AVAILABLE'
		}
	},
	{
		assignment: {
			expires_at: null,
			assignment_id: 2,
			task_id: 2,
			user_id: 'demo-user',
			pool_id: 1,
			annotation: {},
			status: 'IN_PROGRESS',
			started_at: new Date().toISOString(),
			completed_at: null
		},
		task: {
			task_id: 2,
			pool_id: 1,
			dataset_id: 1,
			image_url:
				'https://res.cloudinary.com/unix-center/image/upload/c_limit,dpr_3.0,f_auto,fl_progressive,g_center,h_580,q_75,w_906/ctjvjtjfxqavguj60uss.jpg',
			created_at: new Date().toISOString(),
			status: 'AVAILABLE'
		}
	},
	{
		assignment: {
			assignment_id: 3,
			expires_at: null,
			task_id: 3,
			user_id: 'demo-user',
			pool_id: 1,
			annotation: {},
			status: 'PENDING',
			started_at: new Date().toISOString(),
			completed_at: new Date().toISOString()
		},
		task: {
			task_id: 3,
			pool_id: 1,
			dataset_id: 1,
			image_url:
				'https://res.cloudinary.com/unix-center/image/upload/c_limit,dpr_3.0,f_auto,fl_progressive,g_center,h_580,q_75,w_906/ctjvjtjfxqavguj60uss.jpg',
			created_at: new Date().toISOString(),
			status: 'COMPLETED'
		}
	},
	{
		assignment: {
			expires_at: null,
			assignment_id: 4,
			task_id: 4,
			user_id: 'demo-user',
			pool_id: 1,
			annotation: {},
			status: 'APPROVED',
			started_at: new Date().toISOString(),
			completed_at: new Date().toISOString()
		},
		task: {
			task_id: 4,
			pool_id: 1,
			dataset_id: 1,
			image_url:
				'https://res.cloudinary.com/unix-center/image/upload/c_limit,dpr_3.0,f_auto,fl_progressive,g_center,h_580,q_75,w_906/ctjvjtjfxqavguj60uss.jpg',
			created_at: new Date().toISOString(),
			status: 'COMPLETED'
		}
	}
]
