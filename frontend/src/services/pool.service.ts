import { datasetsApi } from '@/api/datasets'
import type { PoolOut } from '@/api/pools'
import { poolsApi } from '@/api/pools'

export interface CreatePoolParams {
	ownerId: string
	datasetName: string
	files: File[]
	overlap: number
	points: number
	limit: number
	skills: string[]
}

export const poolService = {
	findEligiblePool: async (userSkills: string[]): Promise<PoolOut | null> => {
		const pools = await poolsApi.getAll()

		const eligible = pools.filter(p => {
			if (p.skills.length === 0) return true
			return p.skills.some(s => userSkills.includes(s))
		})

		if (eligible.length === 0) return null

		return eligible.sort((a, b) => b.overlap - a.overlap)[0]
	},

	create: async (params: CreatePoolParams) => {
		const dataset = await datasetsApi.create(params.ownerId, {
			name: params.datasetName,
			domain: 'general'
		})

		await datasetsApi.upload(dataset.dataset_id, params.files)

		const pool = await poolsApi.create({
			points: params.points,
			skills: params.skills,
			overlap: params.overlap,
			dataset_id: dataset.dataset_id,
			limit: params.limit
		})

		return { dataset, pool }
	}
}
