import { useEffect, useState } from 'react'

import { poolsApi } from '@/api/pools'

export const useVerificationAvailable = () => {
	const [available, setAvailable] = useState(false)

	useEffect(() => {
		poolsApi.getAll({ pool_type: 'VERIFICATION' })
			.then(pools => {
				const hasOpen = pools.some(p => p.status === 'OPEN')
				setAvailable(hasOpen)
			})
			.catch(() => setAvailable(false))
	}, [])

	return available
}
