const BASE_URL = 'http://localhost:8000/api'
const USER_ID = '5ca80a4b-31f5-42f8-8579-cb4b5cbc74a2'

import fs from 'fs'
import path from 'path'

async function seed() {
	console.log('Запускаю seeder...\n')

	console.log('1. Создаю датасет...')
	const datasetRes = await fetch(`${BASE_URL}/datasets/?owner_id=${USER_ID}`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ name: 'Test Dataset', domain: 'general' }),
	})
	if (!datasetRes.ok) { console.error('Датасет:', await datasetRes.text()); return }
	const dataset = await datasetRes.json()
	console.log(`Датасет: dataset_id=${dataset.dataset_id}\n`)

	console.log('2. Создаю пул...')
	const poolRes = await fetch(`${BASE_URL}/pools/`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ points: 10, skills: [], overlap: 3, dataset_id: dataset.dataset_id, limit: 100 }),
	})
	if (!poolRes.ok) { console.error('Пул:', await poolRes.text()); return }
	const pool = await poolRes.json()
	console.log(`Пул: pool_id=${pool.pool_id}\n`)

	console.log('3. Загружаю изображения...')
	const imagesDir = path.join(process.cwd(), 'scripts', 'images')
	if (!fs.existsSync(imagesDir)) { console.error('Папка scripts/images/ не найдена'); return }

	const files = fs.readdirSync(imagesDir).filter(f =>
		['.jpg', '.jpeg', '.png'].includes(path.extname(f).toLowerCase())
	)
	if (files.length === 0) { console.error('Нет картинок в scripts/images/'); return }

	const formData = new FormData()
	for (const file of files) {
		const filePath = path.join(imagesDir, file)
		const buffer = fs.readFileSync(filePath)
		const blob = new Blob([buffer], { type: 'image/jpeg' })
		formData.append('files', blob, file)
	}

	const uploadRes = await fetch(`${BASE_URL}/datasets/${dataset.dataset_id}/upload`, {
		method: 'POST',
		body: formData,
	})
	if (!uploadRes.ok) { console.error('❌ Upload:', await uploadRes.text()); return }
	const tasks = await uploadRes.json()
	console.log(`Загружено ${tasks.length} задач\n`)

	console.log('4. Создаю assignment...')
	const assignRes = await fetch(
		`${BASE_URL}/assignments/next?user_id=${USER_ID}&pool_id=${pool.pool_id}`,
		{ method: 'POST' }
	)
	if (!assignRes.ok) { console.error('Assignment:', await assignRes.text()); return }
	const assignment = await assignRes.json()
	console.log(`Assignment: assignment_id=${assignment.assignment_id}`)

	console.log('\n Готово!')
	console.log(`POOL_ID = ${pool.pool_id}`)
	console.log(`DATASET_ID = ${dataset.dataset_id}`)
}

seed().catch(console.error)