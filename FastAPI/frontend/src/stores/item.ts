import { defineStore } from 'pinia'
import { ref } from 'vue'
import api, { getErrorMessage } from '@/utils/api'

export interface Item {
  id: number
  title: string
  description?: string
  price: number
  tax?: number
  owner_id: number
}

export const useItemStore = defineStore('item', () => {
  const items = ref<Item[]>([])
  const currentItem = ref<Item | null>(null)
  const loading = ref(false)

  async function fetchItems(skip = 0, limit = 100) {
    loading.value = true
    try {
      const response = await api.get<Item[]>('/items', {
        params: { skip, limit }
      })
      items.value = response.data
    } catch (error) {
      console.error('获取物品列表失败:', getErrorMessage(error))
      throw error
    } finally {
      loading.value = false
    }
  }

  async function getItem(id: number) {
    loading.value = true
    try {
      const response = await api.get<Item>(`/items/${id}`)
      currentItem.value = response.data
      return response.data
    } catch (error) {
      console.error('获取物品失败:', getErrorMessage(error))
      throw error
    } finally {
      loading.value = false
    }
  }

  async function createItem(itemData: Partial<Item>) {
    try {
      const response = await api.post<Item>('/items', itemData)
      items.value.push(response.data)
      return response.data
    } catch (error) {
      console.error('创建物品失败:', getErrorMessage(error))
      throw error
    }
  }

  async function updateItem(id: number, itemData: Partial<Item>) {
    try {
      const response = await api.put<Item>(`/items/${id}`, itemData)
      const index = items.value.findIndex(i => i.id === id)
      if (index !== -1) {
        items.value[index] = response.data
      }
      return response.data
    } catch (error) {
      console.error('更新物品失败:', getErrorMessage(error))
      throw error
    }
  }

  async function deleteItem(id: number) {
    try {
      await api.delete(`/items/${id}`)
      items.value = items.value.filter(i => i.id !== id)
    } catch (error) {
      console.error('删除物品失败:', getErrorMessage(error))
      throw error
    }
  }

  return {
    items,
    currentItem,
    loading,
    fetchItems,
    getItem,
    createItem,
    updateItem,
    deleteItem
  }
})
