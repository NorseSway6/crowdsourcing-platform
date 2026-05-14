import { useState } from 'react'

import { Checkbox } from '@/components/ui'

import styles from './FilterPanel.module.scss'
import { CATEGORIES, CLIENTS } from './Filters.data'

export const FilterPanel = () => {
	const [categories, setCategories] = useState(
		CATEGORIES.map(c => ({ ...c, checked: false }))
	)
	const [clients, setClients] = useState(
		CLIENTS.map(c => ({ ...c, checked: false }))
	)

	return (
		<div className={styles.panel}>
			<div className={styles.section}>
				<div className={styles.sectionTitle}>Фильтры</div>
				{categories.map((cat, i) => (
					<Checkbox
						key={cat.label}
						label={cat.label}
						count={cat.count}
						checked={cat.checked}
						onChange={v =>
							setCategories(prev =>
								prev.map((c, idx) => (idx === i ? { ...c, checked: v } : c))
							)
						}
					/>
				))}
			</div>

			<div className={styles.section}>
				<div className={styles.sectionTitle}>Заказчики</div>
				{clients.map((client, i) => (
					<Checkbox
						key={client.label}
						label={client.label}
						count={client.count}
						checked={client.checked}
						onChange={v =>
							setClients(prev =>
								prev.map((c, idx) => (idx === i ? { ...c, checked: v } : c))
							)
						}
					/>
				))}
			</div>
		</div>
	)
}
