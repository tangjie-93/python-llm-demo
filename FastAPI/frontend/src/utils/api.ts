import axios, { AxiosError, AxiosResponse, InternalAxiosRequestConfig } from 'axios'
import { ElMessage } from 'element-plus'

export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  error?: string
  message?: string
  details?: any
  traceback?: string
  status_code?: number
}

export interface ApiError {
  success: false
  error: string
  message: string
  details?: any
  traceback?: string
  status_code?: number
}

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error: AxiosError) => {
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    return response
  },
  (error: AxiosError<ApiError>) => {
    const responseData = error.response?.data

    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
      ElMessage.error('登录已过期，请重新登录')
      return Promise.reject(error)
    }

    const errorMessage = responseData?.message || responseData?.error || '请求失败'
    const errorDetails = responseData?.details
    const traceback = responseData?.traceback

    console.error('=== API Error ===')
    console.error('Status:', error.response?.status)
    console.error('Error:', errorMessage)
    if (errorDetails) {
      console.error('Details:', errorDetails)
    }
    if (traceback) {
      console.error('Traceback:', traceback)
    }
    console.error('================')

    ElMessage.error(errorMessage)

    return Promise.reject(error)
  }
)

export default api

export function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    return error.response?.data?.message || error.message
  }
  if (error instanceof Error) {
    return error.message
  }
  return '未知错误'
}

export function getErrorDetails(error: unknown): any {
  if (axios.isAxiosError(error)) {
    return error.response?.data?.details
  }
  return null
}
