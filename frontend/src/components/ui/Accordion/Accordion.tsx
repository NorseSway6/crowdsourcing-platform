import { ChevronUp } from 'lucide-react'
import { useState } from 'react'

import styles from './Accordion.module.scss'

interface AccordionProps {
	title: string
	subtitle: string
	children: React.ReactNode
	defaultOpen?: boolean
}

export const Accordion = ({
	title,
	subtitle,
	children,
	defaultOpen = false
}: AccordionProps) => {
	const [open, setOpen] = useState(defaultOpen)

	return (
		<div className={styles.accordion}>
			<div className={styles.accordionHeader} onClick={() => setOpen(o => !o)}>
				<div>
					<div className={styles.accordionTitle}>{title}</div>
					<div className={styles.accordionSubtitle}>{subtitle}</div>
				</div>
				<ChevronUp
					size={20}
					className={`${styles.accordionIcon} ${open ? styles.open : ''}`}
				/>
			</div>

			{open && <div className={styles.accordionBody}>{children}</div>}
		</div>
	)
}
