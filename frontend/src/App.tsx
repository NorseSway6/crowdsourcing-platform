import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'

import { MainLayout } from './layouts'
import { CustomerLayout } from './layouts/CustomerLayout'
import {
	InProgressPage,
	LabelingPage,
	NotFoundPage,
	ReviewPage,
	TasksPage
} from './pages'
import {
	CreateProjectPage,
	CustomerAnalyticsPage,
	CustomerReviewPage,
	ProjectsPage
} from './pages/customer'
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
				<Route path='/customer' element={<CustomerLayout />}>
					<Route index element={<Navigate to='/customer/create' replace />} />
					<Route path='create' element={<CreateProjectPage />} />
					<Route path='projects' element={<ProjectsPage />} />
					<Route path='analytics' element={<CustomerAnalyticsPage />} />
					<Route path='review' element={<CustomerReviewPage />} />
				</Route>
				<Route path='/labeling' element={<LabelingPage />} />
				<Route path='*' element={<NotFoundPage />} />
			</Routes>
		</BrowserRouter>
	)
}

export default App
