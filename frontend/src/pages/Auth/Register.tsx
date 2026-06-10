import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { Button, Field, Input, Select } from '@/components/ui'

import { useAuth } from '@/hooks/useAuth'

import type { UserRole } from '@/api/auth'

import styles from './Login.module.scss'

export const RegisterPage = () => {
	const { register } = useAuth()
	const navigate = useNavigate()
	const [email, setEmail] = useState('')
	const [password, setPassword] = useState('')
	const [firstName, setFirstName] = useState('')
	const [lastName, setLastName] = useState('')
	const [role, setRole] = useState<UserRole>('STUDENT')
	const [error, setError] = useState<string | null>(null)
	const [loading, setLoading] = useState(false)

	const handleSubmit = async () => {
		if (!email || !password || !firstName || !lastName) return
		setLoading(true)
		setError(null)
		try {
			await register({ email, password, role, firstName, lastName })
			navigate(role === 'CUSTOMER' ? '/customer/create' : '/tasks')
		} catch {
			setError('Ошибка при регистрации')
		} finally {
			setLoading(false)
		}
	}

	return (
		<div className={styles.page}>
			<div className={styles.card}>
				<div className={styles.title}>Регистрация</div>
				<div className={styles.subtitle}>Создайте аккаунт</div>

				<div className={styles.form}>
					{error && <div className={styles.error}>{error}</div>}

					<Field label='Имя'>
						<Input
							placeholder='Иван'
							value={firstName}
							onChange={e => setFirstName(e.target.value)}
						/>
					</Field>

					<Field label='Фамилия'>
						<Input
							placeholder='Иванов'
							value={lastName}
							onChange={e => setLastName(e.target.value)}
						/>
					</Field>

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
							placeholder='Минимум 8 символов'
							value={password}
							onChange={e => setPassword(e.target.value)}
						/>
					</Field>

					<Field label='Роль'>
						<Select
							value={role}
							onChange={v => setRole(v as UserRole)}
							options={[
								{ value: 'STUDENT', label: 'Студент' },
								{ value: 'CUSTOMER', label: 'Заказчик' }
							]}
						/>
					</Field>

					<Button full onClick={handleSubmit} disabled={loading}>
						{loading ? 'Регистрируем...' : 'Зарегистрироваться'}
					</Button>
				</div>

				<div className={styles.footer}>
					Уже есть аккаунт? <Link to='/login'>Войти</Link>
				</div>
			</div>
		</div>
	)
}
