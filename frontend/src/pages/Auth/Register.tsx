import axios from 'axios'
import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import type { RegisterData, UserRole } from '@/api/auth'
import { Button, Field, Input, Select } from '@/components/ui'

import { useAuth } from '@/hooks/useAuth'

import styles from './Login.module.scss'

const getRegisterError = (err: unknown): string => {
	if (axios.isAxiosError(err)) {
		const detail = err.response?.data?.detail
		if (typeof detail === 'string') return detail
		if (Array.isArray(detail)) {
			return detail.map((d: { msg?: string }) => d.msg).filter(Boolean).join(', ')
		}
	}
	return 'Ошибка при регистрации'
}

export const RegisterPage = () => {
	const { register } = useAuth()
	const navigate = useNavigate()

	const [email, setEmail] = useState('')
	const [password, setPassword] = useState('')
	const [firstName, setFirstName] = useState('')
	const [lastName, setLastName] = useState('')
	const [middleName, setMiddleName] = useState('')
	const [group, setGroup] = useState('')
	const [institution, setInstitution] = useState('')
	const [role, setRole] = useState<UserRole>('STUDENT')
	const [error, setError] = useState<string | null>(null)
	const [loading, setLoading] = useState(false)

	const isStudent = role === 'STUDENT'

	const validate = (): string | null => {
		if (!firstName.trim() || !lastName.trim()) return 'Укажите имя и фамилию'
		if (!email.trim()) return 'Укажите email'
		if (password.length < 8) return 'Пароль — минимум 8 символов'
		if (isStudent) {
			if (!group.trim()) return 'Укажите группу'
			if (!institution.trim()) return 'Укажите институт'
		}
		return null
	}

	const handleSubmit = async () => {
		const validationError = validate()
		if (validationError) {
			setError(validationError)
			return
		}

		setLoading(true)
		setError(null)

		const data: RegisterData = {
			email: email.trim(),
			password,
			role,
			profile: {
				firstName: firstName.trim(),
				lastName: lastName.trim(),
				middleName: middleName.trim() || undefined,
				group: isStudent ? group.trim() : undefined,
				institution: institution.trim() || undefined
			}
		}

		try {
			await register(data)
			navigate(role === 'CUSTOMER' ? '/customer/create' : '/tasks')
		} catch (err) {
			setError(getRegisterError(err))
		} finally {
			setLoading(false)
		}
	}

	return (
		<div className={styles.page}>
			<div className={`${styles.card} ${styles.cardWide}`}>
				<div className={styles.title}>Регистрация</div>
				<div className={styles.subtitle}>
					{isStudent
						? 'Аккаунт исполнителя — укажите учебные данные'
						: 'Аккаунт заказчика'}
				</div>

				<div className={styles.form}>
					{error && <div className={styles.error}>{error}</div>}

					<Field label='Роль'>
						<Select
							value={role}
							onChange={v => setRole(v as UserRole)}
							options={[
								{ value: 'STUDENT', label: 'Студент (исполнитель)' },
								{ value: 'CUSTOMER', label: 'Заказчик' }
							]}
						/>
					</Field>

					<Field label='Фамилия'>
						<Input
							placeholder='Иванов'
							value={lastName}
							onChange={e => setLastName(e.target.value)}
						/>
					</Field>

					<Field label='Имя'>
						<Input
							placeholder='Иван'
							value={firstName}
							onChange={e => setFirstName(e.target.value)}
						/>
					</Field>

					<Field label='Отчество (необязательно)'>
						<Input
							placeholder='Иванович'
							value={middleName}
							onChange={e => setMiddleName(e.target.value)}
						/>
					</Field>

					{isStudent ? (
						<>
							<Field label='Группа'>
								<Input
									placeholder='ИВТ-101'
									value={group}
									onChange={e => setGroup(e.target.value)}
								/>
							</Field>
							<Field label='Институт'>
								<Input
									placeholder='МГТУ'
									value={institution}
									onChange={e => setInstitution(e.target.value)}
								/>
							</Field>
						</>
					) : (
						<Field label='Организация (необязательно)'>
							<Input
								placeholder='Название компании или вуза'
								value={institution}
								onChange={e => setInstitution(e.target.value)}
							/>
						</Field>
					)}

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
