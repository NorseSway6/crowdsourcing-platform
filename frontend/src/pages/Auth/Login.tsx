import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { Button, Field, Input } from '@/components/ui'

import { useAuth } from '@/hooks/useAuth'

import styles from './Login.module.scss'

export const LoginPage = () => {
	const { login } = useAuth()
	const navigate = useNavigate()
	const [email, setEmail] = useState('')
	const [password, setPassword] = useState('')
	const [error, setError] = useState<string | null>(null)
	const [loading, setLoading] = useState(false)

	const handleSubmit = async () => {
		if (!email || !password) return
		setLoading(true)
		setError(null)
		try {
			await login(email, password)
			navigate('/tasks')
		} catch {
			setError('Неверный email или пароль')
		} finally {
			setLoading(false)
		}
	}

	return (
		<div className={styles.page}>
			<div className={styles.card}>
				<div className={styles.title}>Вход</div>
				<div className={styles.subtitle}>Войдите в свой аккаунт</div>

				<div className={styles.form}>
					{error && <div className={styles.error}>{error}</div>}

					<Field label='Email'>
						<Input
							type='email'
							placeholder='ivan@example.com'
							value={email}
							onChange={e => setEmail(e.target.value)}
						/>
					</Field>

					<Field label='Пароль'>
						<Input
							type='password'
							placeholder='Введите пароль'
							value={password}
							onChange={e => setPassword(e.target.value)}
						/>
					</Field>

					<Button full onClick={handleSubmit} disabled={loading}>
						{loading ? 'Входим...' : 'Войти'}
					</Button>
				</div>

				<div className={styles.footer}>
					Нет аккаунта? <Link to='/register'>Зарегистрироваться</Link>
				</div>
			</div>
		</div>
	)
}
