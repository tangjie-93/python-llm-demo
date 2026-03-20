import { defineStore } from 'pinia'
import { ref } from 'vue'
import api, { getErrorMessage } from '@/utils/api'

export interface User {
  id: number
  username: string
  email: string
  full_name?: string
  is_active: boolean
}

export const useUserStore = defineStore('user', () => {
  const users = ref<User[]>([])
  const currentUser = ref<User | null>(null)
  const loading = ref(false)

  async function fetchUsers() {
    loading.value = true
    try {
      const response = await api.get<User[]>('/users')
      users.value = response.data
    } catch (error) {
      console.error('获取用户列表失败:', getErrorMessage(error))
      throw error
    } finally {
      loading.value = false
    }
  }

  async function getUser(id: number) {
    loading.value = true
    try {
      const response = await api.get<User>(`/users/${id}`)
      currentUser.value = response.data
      return response.data
    } catch (error) {
      console.error('获取用户失败:', getErrorMessage(error))
      throw error
    } finally {
      loading.value = false
    }
  }

  async function createUser(userData: Partial<User>) {
    try {
      const response = await api.post<User>('/users', userData)
      users.value.push(response.data)
      return response.data
    } catch (error) {
      console.error('创建用户失败:', getErrorMessage(error))
      throw error
    }
  }

  async function updateUser(id: number, userData: Partial<User>) {
    try {
      const response = await api.put<User>(`/users/${id}`, userData)
      const index = users.value.findIndex(u => u.id === id)
      if (index !== -1) {
        users.value[index] = response.data
      }
      return response.data
    } catch (error) {
      console.error('更新用户失败:', getErrorMessage(error))
      throw error
    }
  }

  async function deleteUser(id: number) {
    try {
      await api.delete(`/users/${id}`)
      users.value = users.value.filter(u => u.id !== id)
    } catch (error) {
      console.error('删除用户失败:', getErrorMessage(error))
      throw error
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
  }
})
