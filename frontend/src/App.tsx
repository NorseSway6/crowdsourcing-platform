import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'

import { PrivateRoute } from './components/PrivateRoute'
import { PublicRoute } from './components/PublicRoute'
import { MainLayout } from './layouts'
import { CustomerLayout } from './layouts/CustomerLayout'
import {
	InProgressPage,
	LabelingPage,
	LoginPage,
	NotFoundPage,
	RegisterPage,
	ReviewPage,
	TasksPage,
	VerificationPage
} from './pages'
import {
	CreateProjectPage,
	CustomerAnalyticsPage,
	CustomerReviewPage,
	ProjectDetailPage,
	ProjectsPage
} from './pages/customer'
import { ProfilePage } from './pages/Profile/Profile'
import './styles/global.scss'

export default function App() {
	return (
		<BrowserRouter>
			<Routes>
				<Route
					path='/login'
					element={
						<PublicRoute>
							<LoginPage />
						</PublicRoute>
					}
				/>
				<Route
					path='/register'
					element={
						<PublicRoute>
							<RegisterPage />
						</PublicRoute>
					}
				/>

				<Route
					path='/'
					element={
						<PrivateRoute role='STUDENT'>
							<MainLayout />
						</PrivateRoute>
					}
				>
					<Route index element={<Navigate to='/tasks' replace />} />
					<Route path='tasks' element={<TasksPage />} />
					<Route path='in-progress' element={<InProgressPage />} />
					<Route path='review' element={<ReviewPage />} />
					<Route path='profile' element={<ProfilePage />} />
				</Route>

				<Route
					path='/customer'
					element={
						<PrivateRoute role='CUSTOMER'>
							<CustomerLayout />
						</PrivateRoute>
					}
				>
					<Route index element={<Navigate to='/customer/create' replace />} />
					<Route path='create' element={<CreateProjectPage />} />
					<Route path='projects' element={<ProjectsPage />} />
					<Route path='projects/:id' element={<ProjectDetailPage />} />
					<Route path='analytics' element={<CustomerAnalyticsPage />} />
					<Route path='review' element={<CustomerReviewPage />} />
					<Route path='profile' element={<ProfilePage />} />
				</Route>

				<Route
					path='/labeling'
					element={
						<PrivateRoute role='STUDENT'>
							<LabelingPage />
						</PrivateRoute>
					}
				/>

				<Route
					path='/verification'
					element={
						<PrivateRoute role='STUDENT'>
							<VerificationPage />
						</PrivateRoute>
					}
				/>

				<Route path='*' element={<NotFoundPage />} />
			</Routes>
		</BrowserRouter>
	)
}
