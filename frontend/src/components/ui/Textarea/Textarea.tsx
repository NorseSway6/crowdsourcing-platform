import type { TextareaHTMLAttributes } from 'react'

import styles from './Textarea.module.scss'

type Props = TextareaHTMLAttributes<HTMLTextAreaElement>

export const Textarea = (props: Props) => {
	return <textarea className={styles.textarea} {...props} />
}
