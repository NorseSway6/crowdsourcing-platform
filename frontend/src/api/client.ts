import axios from 'axios'

export const apiClient = axios.create({
	baseURL: 'http://localhost:8000/api',
	headers: { 'Content-Type': 'application/json' },
	withCredentials: true
})

const getToken = () =>
	document.cookie
		.split('; ')
		.find(r => r.startsWith('access_token='))
		?.split('=')[1]

const setTokens = (access: string, refresh: string) => {
	document.cookie = `access_token=${access}; path=/; SameSite=Strict`
	document.cookie = `refresh_token=${refresh}; path=/; SameSite=Strict`
}

const clearTokens = () => {
	document.cookie = 'access_token=; path=/; max-age=0'
	document.cookie = 'refresh_token=; path=/; max-age=0'
}

export { clearTokens, getToken, setTokens }

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
				const refresh = document.cookie
					.split('; ')
					.find(r => r.startsWith('refresh_token='))
					?.split('=')[1]
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
