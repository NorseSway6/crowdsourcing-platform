import fs from 'fs'
import path from 'path'

const BASE_URL = 'http://localhost:8000/api'

async function seed() {
	console.log('🌱 Запускаю seeder...')

	// 1. РЕГИСТРАЦИЯ (исправлено под /api/auth/register)
	const userRes = await fetch(`${BASE_URL}/auth/register`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({
			email: `student_${Date.now()}@test.com`,
			role: 'STUDENT',
			password: 'test1234',
			user_profile: {
				first_name: 'Иван',
				last_name: 'Иванов',
				middle_name: 'Иванович',
				group: 'ИВТ-101',
				institution: 'МГТУ',
				skills: []
			}
		}),
	})

	if (!userRes.ok) {
		console.error('❌ Ошибка регистрации:', await userRes.text())
		return
	}

	const regData = await userRes.json()
	const USER_ID = regData.user.user_id
	console.log(`✅ Юзер создан: ${USER_ID}`)

	// 2. СОЗДАНИЕ ДАТАСЕТА
	const datasetRes = await fetch(`${BASE_URL}/datasets/?owner_id=${USER_ID}`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ name: 'Test Dataset', domain: 'general' }),
	})

	if (!datasetRes.ok) {
		console.error('❌ Датасет:', await datasetRes.text())
		return
	}
	const dataset = await datasetRes.json()
	console.log(`✅ Датасет создан: ${dataset.dataset_id}`)

	// 3. ЗАГРУЗКА КАРТИНОК
	const imagesDir = path.join(process.cwd(), 'scripts', 'images')
	if (!fs.existsSync(imagesDir)) {
		console.error('❌ Папка scripts/images/ не найдена')
		return
	}

	const files = fs.readdirSync(imagesDir).filter(f =>
		['.jpg', '.jpeg', '.png', '.webp'].includes(path.extname(f).toLowerCase())
	)

	if (files.length === 0) {
		console.error('❌ Нет картинок в scripts/images/')
		return
	}

	const formData = new FormData()
	for (const file of files) {
		const buffer = fs.readFileSync(path.join(imagesDir, file))
		formData.append('files', new Blob([buffer], { type: 'image/jpeg' }), file)
	}

	const uploadRes = await fetch(`${BASE_URL}/datasets/${dataset.dataset_id}/upload`, {
		method: 'POST',
		body: formData,
	})

	if (!uploadRes.ok) {
		console.error('❌ Upload:', await uploadRes.text())
		return
	}
	const uploadedTasks = await uploadRes.json()
	console.log(`✅ Загружено файлов: ${uploadedTasks.length}`)

	// 4. СОЗДАНИЕ ПАЙПЛАЙНА
	const pipelineRes = await fetch(`${BASE_URL}/pipelines/?owner_id=${USER_ID}`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({
			name: 'Test Pipeline',
			dataset_id: dataset.dataset_id,
			limit: files.length,
			pools: [
				{
					points: 10,
					skills: [],
					pool_type: 'ANNOTATION',
					target_institution: null,
					tasks_limit: 10,
					time_limit: 600,
					order: 1,
				},
				{
					points: 5,
					skills: [],
					pool_type: 'VERIFICATION',
					target_institution: null,
					tasks_limit: 10,
					time_limit: 300,
					order: 2,
				},
			],
		}),
	})

	if (!pipelineRes.ok) {
		console.error('❌ Pipeline:', await pipelineRes.text())
		return
	}

	const pipeline = await pipelineRes.json()
	const annotationPool = pipeline.pools.find(p => p.pool_type === 'ANNOTATION')
	console.log(`✅ Pipeline создан: ${pipeline.pipeline_id}`)
	console.log(`✅ Пул разметки: ${annotationPool.pool_id}`)

	// 5. СОЗДАНИЕ ЗАДАНИЙ (Assignments)
	const tasksRes = await fetch(`${BASE_URL}/tasks/`)
	const allTasks = await tasksRes.json()
	const poolTasks = allTasks.filter(t => t.pool_id === annotationPool.pool_id)
	console.log(`📦 Задач в пуле: ${poolTasks.length}`)

	let created = 0
	for (let i = 0; i < Math.min(poolTasks.length, 4); i++) {
		const assignRes = await fetch(
			`${BASE_URL}/assignments/next?user_id=${USER_ID}&pool_id=${annotationPool.pool_id}`,
			{ method: 'POST' }
		)
		if (!assignRes.ok) {
			console.warn(`⚠️ Assignment ${i + 1} не создан:`, await assignRes.text())
			continue
		}
		const assignment = await assignRes.json()

		// Отправляем демо-разметку для всех кроме первого (чтобы показать флоу проверки)
		if (i > 0) {
			const submitRes = await fetch(
				`${BASE_URL}/assignments/${assignment.assignment_id}?user_id=${USER_ID}`,
				{
					method: 'PATCH',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify({
						annotation: {
							type: 'coco',
							items: [
								{ category_id: 1, bbox: [10, 10, 100, 100], area: 10000, iscrowd: 0, segmentation: [] }
							],
						},
					}),
				}
			)
			if (!submitRes.ok) console.warn(`⚠️ Submit ${i + 1}:`, await submitRes.text())
		}

		created++
		console.log(`✅ Assignment ${assignment.assignment_id} создан (task ${assignment.task_id})`)
	}

	console.log('\n🏁 Готово')
	console.log(`USER_ID = ${USER_ID}`)
	console.log(`PIPELINE_ID = ${pipeline.pipeline_id}`)
	console.log(`P OOL_ID = ${annotationPool.pool_id}`)
	console.log(`DATASET_ID = ${dataset.dataset_id}`)
	console.log(`assignments = ${created}`)
	console.log(`\n📝 Обнови в config/temp.ts:`)
	console.log(`TEMP_USER_ID = '${USER_ID}'`)
	console.log(`TEMP_POOL_ID = ${annotationPool.pool_id}`)
}

seed().catch(console.error)