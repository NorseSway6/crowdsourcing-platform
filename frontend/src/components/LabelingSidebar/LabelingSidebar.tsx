import { Button } from '@/components/ui'

import type { Shape } from '@/types/canvas'

import styles from './LabelingSidebar.module.scss'

interface Props {
	shapes: Shape[]
	onSubmit: () => void
	onSkip: () => void
	submitting: boolean
}

export const LabelingSidebar = ({
	shapes,
	onSubmit,
	onSkip,
	submitting
}: Props) => (
	<div className={styles.sidebar}>
		<Button
			full
			onClick={onSubmit}
			disabled={submitting || shapes.length === 0}
		>
			{submitting ? 'Отправка...' : 'Отправить'}
		</Button>
		<Button
			variant='secondary'
			full
			onClick={onSkip}
			disabled={submitting}
		>
			Пропустить
		</Button>
	</div>
)
