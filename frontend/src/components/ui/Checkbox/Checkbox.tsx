import styles from './Checkbox.module.scss'

interface Props {
	label: string
	count?: number
	checked: boolean
	onChange: (checked: boolean) => void
}

export const Checkbox = ({ label, count, checked, onChange }: Props) => (
	<label className={styles.item}>
		<input
			type='checkbox'
			className={styles.checkbox}
			checked={checked}
			onChange={e => onChange(e.target.checked)}
		/>
		<span className={styles.label}>{label}</span>
		{count !== undefined && <span className={styles.count}>{count}</span>}
	</label>
)
