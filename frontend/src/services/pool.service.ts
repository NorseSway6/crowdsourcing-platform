import type { PoolOut } from '@/api/pools'
import { poolsApi } from '@/api/pools'

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
