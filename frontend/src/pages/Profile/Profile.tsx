import axios from 'axios'
import { useEffect, useState } from 'react'

import { skillsApi } from '@/api/skills'
import { usersApi } from '@/api/users'
import { Button, Checkbox, Field, Input } from '@/components/ui'
import { PageLoader } from '@/components/PageLoader'

import { useAuth } from '@/hooks/useAuth'

import styles from './Profile.module.scss'

const getErrorMessage = (err: unknown): string => {
	if (axios.isAxiosError(err)) {
		const detail = err.response?.data?.detail
		if (typeof detail === 'string') return detail
	}
	return 'Не удалось сохранить профиль'
}

export const ProfilePage = () => {
	const { user, refreshUser } = useAuth()
	const isStudent = user?.role === 'STUDENT'

	const [firstName, setFirstName] = useState('')
	const [lastName, setLastName] = useState('')
	const [middleName, setMiddleName] = useState('')
	const [group, setGroup] = useState('')
	const [institution, setInstitution] = useState('')
	const [availableSkills, setAvailableSkills] = useState<string[]>([])
	const [selectedSkills, setSelectedSkills] = useState<Set<string>>(new Set())
	const [loading, setLoading] = useState(true)
	const [saving, setSaving] = useState(false)
	const [error, setError] = useState<string | null>(null)
	const [success, setSuccess] = useState(false)

	useEffect(() => {
		const load = async () => {
			setLoading(true)
			try {
				const skills = await skillsApi.getAll()
				setAvailableSkills(skills)

				if (user?.user_profile) {
					const p = user.user_profile
					setFirstName(p.first_name)
					setLastName(p.last_name)
					setMiddleName(p.middle_name || '')
					setGroup(p.group || '')
					setInstitution(p.institution || '')
					setSelectedSkills(new Set(p.skills || []))
				}
			} finally {
				setLoading(false)
			}
		}
		load()
	}, [user])

	const toggleSkill = (skill: string) => {
		setSelectedSkills(prev => {
			const next = new Set(prev)
			if (next.has(skill)) next.delete(skill)
			else next.add(skill)
			return next
		})
	}

	const handleSave = async () => {
		if (!lastName.trim() || !firstName.trim()) {
			setError('Укажите имя и фамилию')
			return
		}
		if (isStudent && (!group.trim() || !institution.trim())) {
			setError('Укажите группу и институт')
			return
		}

		setSaving(true)
		setError(null)
		setSuccess(false)

		try {
			await usersApi.updateProfile({
				first_name: firstName.trim(),
				last_name: lastName.trim(),
				middle_name: middleName.trim() || undefined,
				group: group.trim() || undefined,
				institution: institution.trim() || undefined,
				skills: [...selectedSkills]
			})
			await refreshUser()
			setSuccess(true)
		} catch (err) {
			setError(getErrorMessage(err))
		} finally {
			setSaving(false)
		}
	}

	if (loading) {
		return (
			<div className={styles.page}>
				<PageLoader fullscreen />
			</div>
		)
	}

	return (
		<div className={styles.page}>
			<h1 className={styles.pageTitle}>Профиль</h1>
			<p className={styles.subtitle}>{user?.email}</p>

			<div className={styles.card}>
				{error && <div className={styles.error}>{error}</div>}
				{success && <div className={styles.success}>Профиль сохранён</div>}

				<div className={styles.form}>
					<Field label='Фамилия'>
						<Input value={lastName} onChange={e => setLastName(e.target.value)} />
					</Field>
					<Field label='Имя'>
						<Input
							value={firstName}
							onChange={e => setFirstName(e.target.value)}
						/>
					</Field>
					<Field label='Отчество'>
						<Input
							value={middleName}
							onChange={e => setMiddleName(e.target.value)}
						/>
					</Field>

					{isStudent ? (
						<>
							<Field label='Группа'>
								<Input value={group} onChange={e => setGroup(e.target.value)} />
							</Field>
							<Field label='Институт'>
								<Input
									value={institution}
									onChange={e => setInstitution(e.target.value)}
								/>
							</Field>
						</>
					) : (
						<Field label='Организация'>
							<Input
								value={institution}
								onChange={e => setInstitution(e.target.value)}
							/>
						</Field>
					)}

					{availableSkills.length > 0 && (
						<Field label='Навыки'>
							<div className={styles.skills}>
								{availableSkills.map(skill => (
									<Checkbox
										key={skill}
										label={skill}
										checked={selectedSkills.has(skill)}
										onChange={() => toggleSkill(skill)}
									/>
								))}
							</div>
						</Field>
					)}

					<Button onClick={handleSave} disabled={saving}>
						{saving ? 'Сохраняем...' : 'Сохранить'}
					</Button>
				</div>
			</div>
		</div>
	)
}
