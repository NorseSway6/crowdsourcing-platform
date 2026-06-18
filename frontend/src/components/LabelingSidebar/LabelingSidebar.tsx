import { Button, Select } from '@/components/ui'

import type { CategoryOut } from '@/api/datasets'
import type { Shape } from '@/types/canvas'

import styles from './LabelingSidebar.module.scss'

interface Props {
	shapes: Shape[]
	onSubmit: () => void
	onSkip: () => void
	submitting: boolean
	categories: CategoryOut[]
	selectedCategoryId: number
	onCategoryChange: (id: number) => void
}

export const LabelingSidebar = ({
	shapes,
	onSubmit,
	onSkip,
	submitting,
	categories,
	selectedCategoryId,
	onCategoryChange
}: Props) => (
	<div className={styles.sidebar}>
		{categories.length > 0 && (
			<div className={styles.categorySection}>
				<label className={styles.categoryLabel}>Категория</label>
				<Select
					value={String(selectedCategoryId)}
					onChange={val => onCategoryChange(Number(val))}
					options={categories.map(c => ({
						value: String(c.id),
						label: c.name
					}))}
				/>
			</div>
		)}
		<div className={styles.shapesCount}>
			Объектов: {shapes.length}
		</div>
		<Button
			full
			onClick={onSubmit}
			disabled={submitting || shapes.length === 0}
		>
			{submitting ? 'Отправка...' : 'Отправить'}
		</Button>
		<Button variant='secondary' full onClick={onSkip} disabled={submitting}>
			Пропустить
		</Button>
	</div>
)
