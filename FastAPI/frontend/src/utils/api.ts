import { ApiError } from '@/types/auth';
import axios, { AxiosError, AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import { ElMessage } from 'element-plus';

const axiosInstance = axios.create({
  baseURL: '/api',
  timeout: 10000
});

axiosInstance.interceptors.request.use(
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

axiosInstance.interceptors.response.use(
  (response: AxiosResponse) => {
    // 如果响应中有 success 字段且为 false，则抛出错误
    if (response.data && 'success' in response.data && !response.data.success) {
      throw new Error(response.data.message || response.data.error || '请求失败');
    }
    // 返回实际的 data 数据
    return response.data.data;
  },
  (error: AxiosError<ApiError>) => {
    const responseData = error.response?.data;
    let errorMessage = responseData?.message || responseData?.error || responseData?.detail || '请求失败';
    if (error.response?.status === 401) {
      // 检查是否是登录接口的错误
      if (!error.config?.url?.includes('/auth/login')) {
        ElMessage.error({
          message: '登录已过期，请重新登录',
          duration: 5000 // 5 秒
        });
        // 其他 401 错误，视为登录过期
        localStorage.removeItem('token');
        window.location.href = '/login';
      }
      return Promise.reject(errorMessage);
    }
    return Promise.reject(errorMessage);
  }
);

// 包装 axios 方法，返回正确的类型
const api = {
  get: <T = any>(url: string, config?: any): Promise<T> => axiosInstance.get(url, config),
  post: <T = any>(url: string, data?: any, config?: any): Promise<T> => axiosInstance.post(url, data, config),
  put: <T = any>(url: string, data?: any, config?: any): Promise<T> => axiosInstance.put(url, data, config),
  patch: <T = any>(url: string, data?: any, config?: any): Promise<T> => axiosInstance.patch(url, data, config),
  delete: <T = any>(url: string, config?: any): Promise<T> => axiosInstance.delete(url, config),
};

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

