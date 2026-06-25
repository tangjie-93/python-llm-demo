import { ApiError } from '@/types/auth';
import axios, { AxiosError, AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import { ElMessage } from 'element-plus';
import { useAuthStore } from '@/stores/auth';

const axiosInstance = axios.create({
  baseURL: '/api',
  timeout: 10000
});

// 标记是否正在刷新 token
let isRefreshing = false;
// 存储 401 请求队列
let requestsQueue: Array<() => void> = [];

// 执行队列中的请求
function executeQueue() {
  requestsQueue.forEach(cb => cb());
  requestsQueue = [];
}

axiosInstance.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const authStore = useAuthStore();
    const token = authStore.token;
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
    // 后端统一返回格式：{success: true, message: "...", data: {...}}
    const responseData = response.data;
    
    // 如果响应中有 success 字段且为 false，则抛出错误
    if (responseData && 'success' in responseData && !responseData.success) {
      throw new Error(responseData.message || '请求失败');
    }
    
    // 返回实际的 data 数据
    return responseData.data;
  },
  async (error: AxiosError<ApiError>) => {
    const responseData = error.response?.data;
    let errorMessage = responseData?.message || '请求失败';
    
    if (error.response?.status === 401) {
      // 检查是否是登录接口的错误 - 登录接口不显示错误提示，由组件自己处理
      if (error.config?.url?.includes('/auth/login')) {
        return Promise.reject(errorMessage);
      }
      
      const authStore = useAuthStore();
      
      // 如果已经在刷新 token，则加入队列
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          requestsQueue.push(() => {
            axiosInstance(error.config!).then(resolve).catch(reject);
          });
        });
      }
      
      // 尝试刷新 token
      if (authStore.token) {
        isRefreshing = true;
        
        try {
          const success = await authStore.refreshTokenFunc();
          
          if (success) {
            // 重新执行队列中的请求
            executeQueue();
            // 重试当前请求
            return axiosInstance(error.config!);
          } else {
            // 刷新失败，跳转登录
            ElMessage.error({
              message: '登录已过期，请重新登录',
              duration: 5000
            });
            window.location.href = '/login';
            return Promise.reject(errorMessage);
          }
        } catch (refreshError) {
          ElMessage.error({
            message: '登录已过期，请重新登录',
            duration: 5000
          });
          window.location.href = '/login';
          return Promise.reject(errorMessage);
        } finally {
          isRefreshing = false;
        }
      } else {
        // 没有 refresh token，直接跳转登录
        ElMessage.error({
          message: '登录已过期，请重新登录',
          duration: 5000
        });
        window.location.href = '/login';
        return Promise.reject(errorMessage);
      }
    }
    
    return Promise.reject(errorMessage);
  }
);

// 包装 axios 方法，返回正确的类型
const api = {
  get: <T = any>(url: string, config?: any): Promise<T> => axiosInstance.get(url, config) as Promise<T>,
  post: <T = any>(url: string, data?: any, config?: any): Promise<T> => axiosInstance.post(url, data, config) as Promise<T>,
  put: <T = any>(url: string, data?: any, config?: any): Promise<T> => axiosInstance.put(url, data, config) as Promise<T>,
  patch: <T = any>(url: string, data?: any, config?: any): Promise<T> => axiosInstance.patch(url, data, config) as Promise<T>,
  delete: <T = any>(url: string, config?: any): Promise<T> => axiosInstance.delete(url, config) as Promise<T>,
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

