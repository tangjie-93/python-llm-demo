import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api, { getErrorMessage } from '@/utils/api';
import { LoginResponse } from '@/types/auth';

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'));
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
    localStorage.setItem('token', data.access_token);
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

  function logout() {
    token.value = null;
    userInfo.value = null;
    localStorage.removeItem('token');
  }

  return {
    token,
    userInfo,
    isLoggedIn,
    login,
    register,
    fetchUserInfo,
    logout,
    api
  };
});
