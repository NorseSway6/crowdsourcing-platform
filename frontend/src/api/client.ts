import axios from 'axios'
import Cookies from 'js-cookie'

export const apiClient = axios.create({
	baseURL: 'http://localhost:8000/api',
	headers: { 'Content-Type': 'application/json' },
	withCredentials: true
})

export const getToken = () => Cookies.get('access_token')

export const setTokens = (access: string, refresh: string) => {
	Cookies.set('access_token', access, { path: '/', sameSite: 'strict' })
	Cookies.set('refresh_token', refresh, { path: '/', sameSite: 'strict' })
}

export const clearTokens = () => {
	Cookies.remove('access_token')
	Cookies.remove('refresh_token')
}

apiClient.interceptors.request.use(config => {
	const token = getToken()
	if (token) config.headers.Authorization = `Bearer ${token}`
	return config
})

apiClient.interceptors.response.use(
	res => res,
	async error => {
		const original = error.config
		if (error.response?.status === 401 && !original._retry) {
			original._retry = true
			try {
				const refresh = Cookies.get('refresh_token')
				if (!refresh) throw new Error()
				const { data } = await axios.post(
					'http://localhost:8000/api/auth/update_tokens',
					{ refresh_token: refresh }
				)
				setTokens(data.access_token, data.refresh_token)
				original.headers.Authorization = `Bearer ${data.access_token}`
				return apiClient(original)
			} catch {
				clearTokens()
				window.location.href = '/login'
			}
		}
		return Promise.reject(error)
	}
)
