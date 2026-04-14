import axios, { AxiosError, AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import { ElMessage } from 'element-plus';

export interface ApiResponse<T = any> {
  success: boolean
  message: string
  data?: T
  error?: string
  details?: any
}

export interface ApiError {
  success: false
  message: string
  error?: string
  details?: any
  data?: any
}

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
});

api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    // 自动解包响应数据
    if (response.data && 'data' in response.data) {
      response.data = response.data.data;
    }
    return response;
  },
  (error: AxiosError<ApiError>) => {
    const responseData = error.response?.data;
    if (error.response?.status === 401) {
       // 登录失败，显示具体错误信息
      const errorMessage = responseData?.message || responseData?.error || '用户名或密码不正确';
      // 检查是否是登录接口的错误
      if (error.config?.url?.includes('/auth/login')) {
        ElMessage.error({
          message: errorMessage,
          duration: 5000 // 5秒
        });
      } else {
        // 其他 401 错误，视为登录过期
        localStorage.removeItem('token');
        window.location.href = '/login';
        ElMessage.error({
          message: '登录已过期，请重新登录',
          duration: 5000 // 5秒
        });
      }
      return Promise.reject(error);
    }
    return Promise.reject(error);
  }
);

export default api;

export function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    return error.response?.data?.message || error.message;
  }
  if (error instanceof Error) {
    return error.message;
  }
  return '未知错误';
}

export function getErrorDetails(error: unknown): any {
  if (axios.isAxiosError(error)) {
    return error.response?.data?.details;
  }
  return null;
}
