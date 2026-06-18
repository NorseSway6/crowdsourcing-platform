import type { ReactNode } from 'react'

import styles from './Field.module.scss'

interface Props {
	label: string
	children: ReactNode
}

export const Field = ({ label, children }: Props) => {
	return (
		<div className={styles.field}>
			<label className={styles.label}>{label}</label>
			{children}
		</div>
	)
}
