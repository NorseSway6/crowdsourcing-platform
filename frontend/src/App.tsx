import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'

import { MainLayout } from './layouts'
import { InProgressPage, LabelingPage, ReviewPage, TasksPage } from './pages'

import './styles/global.scss'

function App() {
	return (
		<BrowserRouter>
			<Routes>
				<Route path='/' element={<MainLayout />}>
					<Route index element={<Navigate to='/tasks' replace />} />
					<Route path='tasks' element={<TasksPage />} />
					<Route path='in-progress' element={<InProgressPage />} />
					<Route path='review' element={<ReviewPage />} />
				</Route>

				<Route path='/labeling' element={<LabelingPage />} />
			</Routes>
		</BrowserRouter>
	)
}

export default App