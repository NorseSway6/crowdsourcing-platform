import { FilterPanel } from '@/components/FilterPanel'
import { SortSelect } from '@/components/SortSelect'
import { TaskCard } from '@/components/TaskCard'

import styles from '../Tasks/Tasks.module.scss'

import { useMyAssignments, useTaskFilters } from '@/hooks'

export const ReviewPage = () => {
	const { items, loading, error } = useMyAssignments('PENDING')
	const { items: approvedItems } = useMyAssignments('APPROVED')

	const pendingTasks = items.map(i => i.task)
	const approvedTasks = approvedItems.map(i => i.task)
	const allTasks = [...pendingTasks, ...approvedTasks]

	const { filtered, sort, setSort } = useTaskFilters(allTasks)

	const getVariant = (taskId: number) => {
		if (approvedTasks.some(t => t.task_id === taskId)) {
			return 'approved' as const
		}
		return 'pending' as const
	}

	return (
		<div className={styles.page}>
			<h1 className={styles.pageTitle}>На проверке</h1>

			<div className={styles.toolbar}>
				<SortSelect
					value={sort}
					onChange={setSort}
				/>
			</div>

			<div className={styles.body}>
				<div className={styles.list}>
					{loading && <div className={styles.empty}>Загрузка...</div>}
					{error && <div className={styles.empty}>{error}</div>}
					{!loading && !error && filtered.length === 0 && (
						<div className={styles.empty}>Нет заданий на проверке</div>
					)}
					{filtered.map(task => (
						<TaskCard
							key={task.task_id}
							task={task}
							variant={getVariant(task.task_id)}
						/>
					))}
				</div>

				<FilterPanel />
			</div>
		</div>
	)
}
