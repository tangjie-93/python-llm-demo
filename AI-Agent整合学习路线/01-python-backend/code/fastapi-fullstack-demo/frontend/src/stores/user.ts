import { defineStore } from 'pinia';
import { ref } from 'vue';
import api, { getErrorMessage } from '@/utils/api';

export interface User {
  id: number
  username: string
  email: string
  full_name?: string
  is_active: boolean
}

export interface UserCreate extends Partial<User> {
  password: string
}

export const useUserStore = defineStore('user', () => {
  const users = ref<User[]>([]);
  const currentUser = ref<User | null>(null);
  const loading = ref(false);

  async function fetchUsers() {
    loading.value = true;
    try {
      const data = await api.get<User[]>('/users/');
      users.value = data;
    } catch (error) {
      console.error('获取用户列表失败:', getErrorMessage(error));
      throw error;
    } finally {
      loading.value = false;
    }
  }

  async function getUser(id: number) {
    loading.value = true;
    try {
      const data = await api.get<User>(`/users/${id}/`);
      currentUser.value = data;
      return data;
    } catch (error) {
      console.error('获取用户失败:', getErrorMessage(error));
      throw error;
    } finally {
      loading.value = false;
    }
  }

  async function createUser(userData: UserCreate) {
    try {
      const data = await api.post<User>('/users/', userData);
      users.value.push(data);
      return data;
    } catch (error) {
      console.error('创建用户失败:', getErrorMessage(error));
      throw error;
    }
  }

  async function updateUser(id: number, userData: Partial<User>) {
    try {
      const data = await api.put<User>(`/users/${id}/`, userData);
      const index = users.value.findIndex(u => u.id === id);
      if (index !== -1) {
        users.value[index] = data;
      }
      return data;
    } catch (error) {
      console.error('更新用户失败:', getErrorMessage(error));
      throw error;
    }
  }

  async function deleteUser(id: number) {
    try {
      await api.delete(`/users/${id}/`);
      users.value = users.value.filter(u => u.id !== id);
    } catch (error) {
      console.error('删除用户失败:', getErrorMessage(error));
      throw error;
    }
  }

  return {
    users,
    currentUser,
    loading,
    fetchUsers,
    getUser,
    createUser,
    updateUser,
    deleteUser
  };
});
