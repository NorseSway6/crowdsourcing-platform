import { FilterPanel } from '@/components/FilterPanel'
import { PageLoader } from '@/components/PageLoader'
import { SortSelect } from '@/components/SortSelect'
import { TaskCard } from '@/components/TaskCard'

import styles from './Tasks.module.scss'
import { useAssignment, useTaskFilters } from '@/hooks'

export const TasksPage = () => {
	const { current, loading, error } = useAssignment()

	const tasks = current ? [current.task] : []
	const {
		filtered,
		sort,
		setSort,
		poolOptions,
		selectedPools,
		togglePool,
		resetFilters,
		hasActiveFilters
	} = useTaskFilters(tasks)

	return (
		<div className={styles.page}>
			<h1 className={styles.pageTitle}>Задания</h1>

			<div className={styles.toolbar}>
				<SortSelect value={sort} onChange={setSort} />
			</div>

			<div className={styles.body}>
				<div className={styles.list}>
					{loading && <PageLoader />}
					{!loading && error && <div className={styles.empty}>{error}</div>}
					{!loading && !error && filtered.length === 0 && (
						<div className={styles.empty}>Нет доступных заданий</div>
					)}
					{filtered.map(task => (
						<TaskCard key={task.task_id} task={task} />
					))}
				</div>

				<FilterPanel
					poolOptions={poolOptions}
					selectedPools={selectedPools}
					onTogglePool={togglePool}
					onReset={resetFilters}
					hasActiveFilters={hasActiveFilters}
				/>
			</div>
		</div>
	)
}
