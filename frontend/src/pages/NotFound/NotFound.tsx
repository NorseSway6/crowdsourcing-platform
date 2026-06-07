import { useNavigate } from 'react-router-dom'

import styles from './NotFound.module.scss'

export const NotFoundPage = () => {
	const navigate = useNavigate()
	return (
		<div className={styles.page}>
			<div className={styles.code}>404</div>
			<div className={styles.text}>Страница не найдена</div>
			<button className={styles.btn} onClick={() => navigate(-1)}>
				Назад
			</button>
		</div>
	)
}
