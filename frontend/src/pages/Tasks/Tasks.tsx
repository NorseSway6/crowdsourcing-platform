import { FilterPanel } from '@/components/FilterPanel'
import { SortSelect } from '@/components/SortSelect'
import { TaskCard } from '@/components/TaskCard'

import styles from './Tasks.module.scss'
import { useAssignment, useTaskFilters } from '@/hooks'

export const TasksPage = () => {
	const { current, loading, error } = useAssignment()

	const tasks = current ? [current.task] : []
	const { filtered, sort, setSort } = useTaskFilters(tasks)

	return (
		<div className={styles.page}>
			<h1 className={styles.pageTitle}>Задания</h1>

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
						<div className={styles.empty}>Нет доступных заданий</div>
					)}
					{filtered.map(task => (
						<TaskCard
							key={task.task_id}
							task={task}
						/>
					))}
				</div>

				<FilterPanel />
			</div>
		</div>
	)
}
