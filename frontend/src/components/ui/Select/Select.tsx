import styles from './Select.module.scss'

interface Option {
	value: string
	label: string
}

interface Props {
	value: string
	options: Option[]
	onChange: (value: string) => void
}

export const Select = ({ value, options, onChange }: Props) => (
	<select
		className={styles.select}
		value={value}
		onChange={e => onChange(e.target.value)}
	>
		{options.map(opt => (
			<option
				key={opt.value}
				value={opt.value}
			>
				{opt.label}
			</option>
		))}
	</select>
)
