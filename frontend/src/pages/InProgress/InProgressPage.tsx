import { FilterPanel } from '@/components/FilterPanel'
import { SortSelect } from '@/components/SortSelect'
import { TaskCard } from '@/components/TaskCard'

import styles from '../Tasks/Tasks.module.scss'

import { useMyAssignments, useTaskFilters } from '@/hooks'

export const InProgressPage = () => {
	const { items, loading, error } = useMyAssignments('IN_PROGRESS')
	const tasks = items.map(i => i.task)
	const { filtered, sort, setSort } = useTaskFilters(tasks)

	return (
		<div className={styles.page}>
			<h1 className={styles.pageTitle}>В работе</h1>

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
						<div className={styles.empty}>Нет заданий в работе</div>
					)}
					{filtered.map(task => (
						<TaskCard
							key={task.task_id}
							task={task}
							variant='in_progress'
						/>
					))}
				</div>

				<FilterPanel />
			</div>
		</div>
	)
}
