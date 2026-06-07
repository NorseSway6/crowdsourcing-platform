import { useNavigate } from 'react-router-dom'

import { Button } from '@/components/ui'

import styles from './TaskCard.module.scss'
import type { Task } from '@/types'

interface Props {
	task: Task
	selected?: boolean
	onClick?: (task: Task) => void
	variant?: 'default' | 'in_progress' | 'pending' | 'approved'
}

export const TaskCard = ({
	task,
	selected,
	onClick,
	variant = 'default'
}: Props) => {
	const navigate = useNavigate()

	return (
		<div
			className={`${styles.card} ${selected ? styles.selected : ''}`}
			onClick={() => onClick?.(task)}
		>
			<div className={styles.header}>
				<span className={styles.title}>{`Задание #${task.task_id}`}</span>
				<span className={styles.category}>Категория {task.pool_id}</span>
			</div>

			<div className={styles.desc}>Описание</div>

			{variant === 'default' && (
				<Button
					onClick={e => {
						e.stopPropagation()
						navigate('/labeling')
					}}
				>
					Взять задачу
				</Button>
			)}

			{variant === 'in_progress' && (
				<Button
					variant='secondary'
					full
					onClick={e => {
						e.stopPropagation()
						navigate('/labeling')
					}}
				>
					Вернуться к задаче
				</Button>
			)}

			{variant === 'pending' && (
				<Button
					variant='pending'
					full
				>
					Ожидает проверки
				</Button>
			)}

			{variant === 'approved' && (
				<Button
					variant='success'
					full
				>
					Проверено
				</Button>
			)}
		</div>
	)
}
