import styles from './Button.module.scss'

interface Props {
	children: React.ReactNode
	variant?: 'primary' | 'secondary' | 'success' | 'pending'
	full?: boolean
	disabled?: boolean
	onClick?: (e: React.MouseEvent<HTMLButtonElement>) => void
}

export const Button = ({
	children,
	variant = 'primary',
	full = false,
	disabled = false,
	onClick
}: Props) => (
	<button
		className={[styles.btn, styles[variant], full ? styles.full : ''].join(' ')}
		disabled={disabled}
		onClick={onClick}
	>
		{children}
	</button>
)
