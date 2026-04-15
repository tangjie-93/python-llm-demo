import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api, { getErrorMessage } from '@/utils/api';
import { LoginResponse } from '@/types/auth';

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(null);
  const userInfo = ref<{ id: number; username: string; email: string } | null>(null);

  const isLoggedIn = computed(() => !!token.value);

  async function login(username: string, password: string) {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const data = await api.post<LoginResponse>('/auth/login', formData);

    if (!data?.access_token) {
      throw new Error('登录失败');
    }
    token.value = data.access_token;
    // refresh_token 现在存储在 HttpOnly Cookie 中，不需要在前端存储
    await fetchUserInfo();
  }

  async function register(username: string, email: string, password: string) {
    await api.post('/auth/register', { username, email, password });
  }

  async function fetchUserInfo() {
    if (!token.value) return;
    try {
      const data = await api.get('/auth/me');
      userInfo.value = data;
    } catch (error) {
      console.error('获取用户信息失败:', getErrorMessage(error));
    }
  }

  async function refreshTokenFunc() {
    // refresh_token 存储在 HttpOnly Cookie 中，后端会自动读取
    try {
      const data = await api.post('/auth/refresh', {});
      token.value = data.access_token;
      return true;
    } catch (error) {
      console.error('刷新 token 失败:', getErrorMessage(error));
      logout();
      return false;
    }
  }

  function logout() {
    token.value = null;
    userInfo.value = null;
    // 调用后端登出接口清除 Cookie
    api.post('/auth/logout').catch(() => {});
  }

  return {
    token,
    userInfo,
    isLoggedIn,
    login,
    register,
    fetchUserInfo,
    refreshTokenFunc,
    logout,
    api
  };
});
