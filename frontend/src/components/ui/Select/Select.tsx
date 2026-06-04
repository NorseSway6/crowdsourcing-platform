import type { SelectHTMLAttributes } from 'react'

import styles from './Select.module.scss'

interface Option<T extends string> {
	value: T
	label: string
}

interface Props<T extends string> extends Omit<
	SelectHTMLAttributes<HTMLSelectElement>,
	'value' | 'onChange'
> {
	value: T
	options: Option<T>[]
	onChange: (value: T) => void
}

export const Select = <T extends string>({
	value,
	options,
	onChange,
	...props
}: Props<T>) => (
	<select
		className={styles.select}
		value={value}
		onChange={e => onChange(e.target.value as T)}
		{...props}
	>
		{options.map(opt => (
			<option key={opt.value} value={opt.value}>
				{opt.label}
			</option>
		))}
	</select>
)
