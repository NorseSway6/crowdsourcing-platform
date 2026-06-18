import styles from './PageLoader.module.scss'

interface Props {
	fullscreen?: boolean
}

export const PageLoader = ({ fullscreen = false }: Props) => (
	<div
		className={`${styles.loader} ${fullscreen ? styles.fullscreen : styles.inline}`}
		role='status'
		aria-label='Загрузка'
	>
		<div className={styles.spinner} />
	</div>
)
