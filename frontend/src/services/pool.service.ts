import type { PoolType } from '@/api/pipelines'
import { poolsApi, type PoolOut } from '@/api/pools'

interface FindPoolOptions {
	poolType?: PoolType
	institution?: string
}

export const poolService = {
	findEligiblePool: async (
		userSkills: string[],
		options?: FindPoolOptions
	): Promise<PoolOut | null> => {
		try {
			const pools = await poolsApi.getAll()
			console.log('All pools:', pools)

			const eligible = pools.filter(p => {
				if (p.status !== 'OPEN') return false
				if (options?.poolType && p.pool_type !== options.poolType) return false
				if (p.target_institution) {
					const institution = options?.institution?.trim()
					if (!institution || p.target_institution !== institution) return false
				}
				if (p.skills.length === 0) return true
				return p.skills.some(s => userSkills.includes(s))
			})

			console.log('Eligible pools:', eligible)

			if (eligible.length === 0) return null

			return eligible.sort((a, b) => a.order - b.order)[0]
		} catch (err) {
			console.error('Error finding pool:', err)
			return null
		}
	}
}
