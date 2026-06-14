import { Checkbox } from '@/components/ui'

import type { FilterOption } from '@/hooks/useTaskFilters'

import styles from './FilterPanel.module.scss'

interface Props {
	poolOptions: FilterOption[]
	selectedPools: Set<string>
	onTogglePool: (poolId: string) => void
	onReset?: () => void
	hasActiveFilters?: boolean
}

export const FilterPanel = ({
	poolOptions,
	selectedPools,
	onTogglePool,
	onReset,
	hasActiveFilters
}: Props) => {
	return (
		<div className={styles.panel}>
			<div className={styles.section}>
				<div className={styles.sectionHeader}>
					<div className={styles.sectionTitle}>Фильтры</div>
					{hasActiveFilters && onReset && (
						<button type='button' className={styles.resetBtn} onClick={onReset}>
							Сбросить
						</button>
					)}
				</div>
				{poolOptions.length === 0 ? (
					<p className={styles.emptyHint}>Нет данных для фильтрации</p>
				) : (
					poolOptions.map(option => (
						<Checkbox
							key={option.id}
							label={option.label}
							count={option.count}
							checked={selectedPools.has(option.id)}
							onChange={() => onTogglePool(option.id)}
						/>
					))
				)}
			</div>
		</div>
	)
}
