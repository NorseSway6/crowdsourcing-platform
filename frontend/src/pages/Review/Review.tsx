import { FilterPanel } from '@/components/FilterPanel'
import { PageLoader } from '@/components/PageLoader'
import { SortSelect } from '@/components/SortSelect'
import { TaskCard } from '@/components/TaskCard'

import styles from '../Tasks/Tasks.module.scss'

import { useMyAssignments, useTaskFilters } from '@/hooks'

export const ReviewPage = () => {
	const { items, loading, error } = useMyAssignments('PENDING')
	const { items: approvedItems, loading: approvedLoading } =
		useMyAssignments('APPROVED')
	const { items: rejectedItems, loading: rejectedLoading } =
		useMyAssignments('REJECTED')

	const pendingTasks = items.map(i => i.task)
	const approvedTasks = approvedItems.map(i => i.task)
	const rejectedTasks = rejectedItems.map(i => i.task)
	const allTasks = [...pendingTasks, ...approvedTasks, ...rejectedTasks]

	const {
		filtered,
		sort,
		setSort,
		poolOptions,
		selectedPools,
		togglePool,
		resetFilters,
		hasActiveFilters
	} = useTaskFilters(allTasks)

	const getVariant = (taskId: number) => {
		if (approvedTasks.some(t => t.task_id === taskId)) {
			return 'approved' as const
		}
		if (rejectedTasks.some(t => t.task_id === taskId)) {
			return 'rejected' as const
		}
		return 'pending' as const
	}

	const isLoading = loading || approvedLoading || rejectedLoading

	return (
		<div className={styles.page}>
			<h1 className={styles.pageTitle}>На проверке</h1>
			<p className={styles.pageSubtitle}>
				Задания проверяются автоматически системой валидации
			</p>

			<div className={styles.toolbar}>
				<SortSelect value={sort} onChange={setSort} />
			</div>

			<div className={styles.body}>
				<div className={styles.list}>
					{isLoading && <PageLoader />}
					{!isLoading && error && <div className={styles.empty}>{error}</div>}
					{!isLoading && !error && filtered.length === 0 && (
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
