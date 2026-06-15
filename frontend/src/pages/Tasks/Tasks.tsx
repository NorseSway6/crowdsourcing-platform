import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { FilterPanel } from '@/components/FilterPanel'
import { PageLoader } from '@/components/PageLoader'
import { SortSelect } from '@/components/SortSelect'
import { TaskCard } from '@/components/TaskCard'
import { Button } from '@/components/ui'

import styles from './Tasks.module.scss'
import { useAssignment, useMyAssignments, useTaskFilters } from '@/hooks'

export const TasksPage = () => {
	const navigate = useNavigate()
	const { current, loading, error } = useAssignment()
	const { items: inProgressItems } = useMyAssignments('IN_PROGRESS')

	const hasInProgress = inProgressItems.length > 0

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

	useEffect(() => {
		if (hasInProgress && !loading) {
			navigate('/in-progress')
		}
	}, [hasInProgress, loading, navigate])

	return (
		<div className={styles.page}>
			<h1 className={styles.pageTitle}>Задания</h1>

			{hasInProgress && (
				<div className={styles.inProgressBanner}>
					<span>У вас есть задания в работе</span>
					<Button onClick={() => navigate('/in-progress')}>
						Перейти к заданиям
					</Button>
				</div>
			)}

			<div className={styles.toolbar}>
				<SortSelect value={sort} onChange={setSort} />
			</div>

			<div className={styles.body}>
				<div className={styles.list}>
					{loading && <PageLoader />}
					{!loading && error && <div className={styles.empty}>{error}</div>}
					{!loading && !error && filtered.length === 0 && !hasInProgress && (
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
