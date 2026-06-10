import { useState, useEffect } from 'react'
import type { AssignmentStatus } from '@/api/assignments'
import type { ActiveAssignment } from '@/services/assignment.service'
import { DEMO_ASSIGNMENTS } from '@/mock/demo'

interface UseMyAssignmentsReturn {
  items: ActiveAssignment[]
  loading: boolean
  error: string | null
}

export const useMyAssignments = (filterStatus?: AssignmentStatus): UseMyAssignmentsReturn => {
  const [items, setItems] = useState<ActiveAssignment[]>([])

  useEffect(() => {
    const filtered = filterStatus
      ? DEMO_ASSIGNMENTS.filter(a => a.assignment.status === filterStatus)
      : DEMO_ASSIGNMENTS
    setItems(filtered)
  }, [filterStatus])

  return { items, loading: false, error: null }
}