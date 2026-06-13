import { CheckCircle, Plus, Upload, X } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'

import { datasetsApi, type CategoryOut } from '@/api/datasets'
import {
	Accordion,
	Button,
	Field,
	Input,
	Select,
	Textarea
} from '@/components/ui'

import { useCreatePipeline } from '@/hooks/useCreatePipeline'

import styles from './CreateProject.module.scss'

export const CreateProjectPage = () => {
	const [name, setName] = useState('')
	const [description, setDescription] = useState('')
	const [instruction, setInstruction] = useState('')
	const [markupType, setMarkupType] = useState('bbox')
	const [files, setFiles] = useState<File[]>([])
	const [points, setPoints] = useState('10')
	const [tasksLimit, setTasksLimit] = useState('10')
	const [timeLimit, setTimeLimit] = useState('600')
	const [institution, setInstitution] = useState('')
	const [dragover, setDragover] = useState(false)
	const [availableCategories, setAvailableCategories] = useState<CategoryOut[]>(
		[]
	)
	const [selectedCategories, setSelectedCategories] = useState<string[]>([])
	const [newCategory, setNewCategory] = useState('')
	const [categoryError, setCategoryError] = useState<string | null>(null)
	const fileInputRef = useRef<HTMLInputElement>(null)

	const { loading, error, success, create } = useCreatePipeline()

	useEffect(() => {
		datasetsApi
			.getCategories()
			.then(setAvailableCategories)
			.catch(() => {})
	}, [])

	const handleFiles = (incoming: FileList | null) => {
		if (!incoming) return
		const arr = Array.from(incoming).filter(f =>
			['image/jpeg', 'image/png', 'image/webp'].includes(f.type)
		)
		setFiles(prev => [...prev, ...arr])
	}

	const toggleCategory = (categoryName: string) => {
		setCategoryError(null)
		setSelectedCategories(prev =>
			prev.includes(categoryName)
				? prev.filter(c => c !== categoryName)
				: [...prev, categoryName]
		)
	}

	const handleAddCategory = async () => {
		const trimmed = newCategory.trim()
		if (!trimmed) return

		setCategoryError(null)
		try {
			const created = await datasetsApi.createCategory(trimmed)
			setAvailableCategories(prev => {
				if (prev.some(c => c.name === created.name)) return prev
				return [...prev, created]
			})
			setSelectedCategories(prev =>
				prev.includes(created.name) ? prev : [...prev, created.name]
			)
			setNewCategory('')
		} catch {
			setCategoryError('Не удалось создать категорию')
		}
	}

	const handleCreate = async () => {
		if (files.length === 0 || !name.trim()) return
		if (selectedCategories.length === 0) {
			setCategoryError('Выберите хотя бы одну категорию объектов')
			return
		}

		await create({
			name,
			files,
			categories: selectedCategories,
			points: Number(points),
			tasksLimit: Number(tasksLimit),
			timeLimit: Number(timeLimit),
			institution: institution || undefined
		})
	}

	const canCreate =
		!loading && files.length > 0 && name.trim() && selectedCategories.length > 0

	return (
		<div className={styles.page}>
			<h1 className={styles.pageTitle}>Создать проект</h1>

			<div className={styles.sections}>
				<Accordion
					title='Общая информация'
					subtitle='Укажите название и описание'
					defaultOpen
				>
					<Field label='Название проекта'>
						<Input
							placeholder='Например: Разметка медицинских снимков'
							value={name}
							onChange={e => setName(e.target.value)}
						/>
					</Field>
					<Field label='Описание'>
						<Textarea
							placeholder='Опишите цель проекта'
							value={description}
							onChange={e => setDescription(e.target.value)}
						/>
					</Field>
					<Field label='Институт (необязательно)'>
						<Input
							placeholder='Например: МГТУ'
							value={institution}
							onChange={e => setInstitution(e.target.value)}
						/>
					</Field>
				</Accordion>

				<Accordion
					title='Интерфейс задания'
					subtitle='Настройте внешний вид заданий у исполнителей'
				>
					<Field label='Тип разметки'>
						<Select
							value={markupType}
							onChange={setMarkupType}
							options={[
								{ value: 'bbox', label: 'Bounding Box' },
								{ value: 'polygon', label: 'Полигон' },
								{ value: 'point', label: 'Точка' }
							]}
						/>
					</Field>

					<Field label='Категории объектов'>
						<div className={styles.categoriesBlock}>
							{availableCategories.length > 0 ? (
								<div className={styles.categoryList}>
									{availableCategories.map(cat => (
										<button
											key={cat.id}
											type='button'
											className={`${styles.categoryChip} ${
												selectedCategories.includes(cat.name)
													? styles.categoryChipActive
													: ''
											}`}
											onClick={() => toggleCategory(cat.name)}
										>
											{cat.name}
										</button>
									))}
								</div>
							) : (
								<p className={styles.categoryHint}>
									Категорий пока нет — создайте первую ниже
								</p>
							)}

							<div className={styles.categoryAdd}>
								<Input
									placeholder='Новая категория, например: автомобиль'
									value={newCategory}
									onChange={e => setNewCategory(e.target.value)}
									onKeyDown={e => {
										if (e.key === 'Enter') {
											e.preventDefault()
											handleAddCategory()
										}
									}}
								/>
								<Button
									variant='secondary'
									onClick={handleAddCategory}
									disabled={!newCategory.trim()}
								>
									<Plus size={14} />
								</Button>
							</div>

							{categoryError && (
								<div className={styles.categoryError}>{categoryError}</div>
							)}
						</div>
					</Field>
				</Accordion>

				<Accordion
					title='Инструкция для исполнителей'
					subtitle='Введите инструкцию, которую увидят исполнители'
				>
					<Field label='Инструкция'>
						<Textarea
							placeholder='Опишите как правильно выполнять задание...'
							value={instruction}
							onChange={e => setInstruction(e.target.value)}
						/>
					</Field>
				</Accordion>

				<div className={styles.poolSection}>
					<div className={styles.poolSectionTitle}>Загрузите данные</div>
					<div className={styles.poolSectionSubtitle}>
						Картинки будут автоматически распределены по пулам разметки и
						верификации
					</div>

					{success ? (
						<div className={styles.poolSuccess}>
							<CheckCircle size={18} />
							Проект создан — {files.length} задач загружено
						</div>
					) : (
						<div className={styles.poolForm}>
							<div
								className={`${styles.dropzone} ${dragover ? styles.dragover : ''}`}
								onClick={() => fileInputRef.current?.click()}
								onDragOver={e => {
									e.preventDefault()
									setDragover(true)
								}}
								onDragLeave={() => setDragover(false)}
								onDrop={e => {
									e.preventDefault()
									setDragover(false)
									handleFiles(e.dataTransfer.files)
								}}
							>
								<Upload size={28} strokeWidth={1.5} />
								<span>Перетащите картинки или нажмите для выбора</span>
								<span style={{ fontSize: 11 }}>JPG, PNG, WEBP</span>
								<input
									ref={fileInputRef}
									type='file'
									multiple
									accept='image/jpeg,image/png,image/webp'
									onChange={e => handleFiles(e.target.files)}
								/>
							</div>

							{files.length > 0 && (
								<div className={styles.fileList}>
									{files.map((f, i) => (
										<div key={i} className={styles.fileChip}>
											<span>{f.name}</span>
											<button
												className={styles.fileChipRemove}
												onClick={() =>
													setFiles(prev => prev.filter((_, idx) => idx !== i))
												}
											>
												<X size={12} />
											</button>
										</div>
									))}
								</div>
							)}

							<div className={styles.poolRow}>
								<Field label='Очки за задание'>
									<Input
										type='number'
										value={points}
										onChange={e => setPoints(e.target.value)}
										placeholder='10'
									/>
								</Field>
								<Field label='Лимит задач на студента'>
									<Input
										type='number'
										value={tasksLimit}
										onChange={e => setTasksLimit(e.target.value)}
										placeholder='10'
									/>
								</Field>
								<Field label='Время на задачу (сек)'>
									<Input
										type='number'
										value={timeLimit}
										onChange={e => setTimeLimit(e.target.value)}
										placeholder='600'
									/>
								</Field>
							</div>

							{error && (
								<div style={{ color: '#e53935', fontSize: 13 }}>{error}</div>
							)}

							<div style={{ display: 'flex', gap: 10 }}>
								<Button onClick={handleCreate} disabled={!canCreate}>
									{loading
										? 'Создаём...'
										: `Создать проект (${files.length} файлов)`}
								</Button>
								<Button variant='secondary' onClick={() => setFiles([])}>
									Очистить
								</Button>
							</div>
						</div>
					)}
				</div>
			</div>
		</div>
	)
}
