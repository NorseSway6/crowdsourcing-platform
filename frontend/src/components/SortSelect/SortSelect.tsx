import { Select } from '@/components/ui'

import type { SortOption } from '@/hooks'

interface Props {
	value: SortOption
	onChange: (v: SortOption) => void
}

export const SortSelect = ({ value, onChange }: Props) => (
	<Select
		value={value}
		options={[
			{ value: 'newest', label: 'Сначала новые' },
			{ value: 'oldest', label: 'Сначала старые' }
		]}
		onChange={v => onChange(v as SortOption)}
	/>
)
