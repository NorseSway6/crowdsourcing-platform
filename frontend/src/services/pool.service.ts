import { type PoolOut, poolsApi } from '@/api/pools'

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
	}
}
