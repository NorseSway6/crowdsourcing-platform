import { Bot, MoveLeft, MoveRight } from 'lucide-react'

import type { Tool } from '@/types/canvas'

import { toolButtons } from './Toolbar.data'
import styles from './Toolbar.module.scss'

interface Props {
	tool: Tool
	onToolChange: (tool: Tool) => void
	onUndo: () => void
	onRedo: () => void
	canUndo: boolean
	canRedo: boolean
}

export const Toolbar = ({
	tool,
	onToolChange,
	onUndo,
	onRedo,
	canUndo,
	canRedo
}: Props) => {
	return (
		<div className={styles.toolbar}>
			{toolButtons.slice(0, 3).map(item => {
				const Icon = item.icon

				return (
					<button
						key={item.tool}
						title={item.title}
						className={`${styles.btn} ${tool === item.tool ? styles.active : ''}`}
						onClick={() => onToolChange(item.tool)}
					>
						<Icon size={24} />
					</button>
				)
			})}

			<div className={styles.divider} />

			<button
				className={styles.btn}
				title='Умная разметка'
				disabled
			>
				<Bot size={24} />
			</button>

			{toolButtons.slice(3).map(item => {
				const Icon = item.icon

				return (
					<button
						key={item.tool}
						title={item.title}
						className={`${styles.btn} ${tool === item.tool ? styles.active : ''}`}
						onClick={() => onToolChange(item.tool)}
					>
						<Icon size={24} />
					</button>
				)
			})}

			<div className={styles.divider} />

			<button
				className={styles.btn}
				title='Отменить'
				onClick={onUndo}
				disabled={!canUndo}
			>
				<MoveLeft size={24} />
			</button>

			<button
				className={styles.btn}
				title='Повторить'
				onClick={onRedo}
				disabled={!canRedo}
			>
				<MoveRight size={24} />
			</button>
		</div>
	)
}
