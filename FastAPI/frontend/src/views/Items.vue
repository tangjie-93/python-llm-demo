<template>
  <div class="items-container">
    <div class="toolbar">
      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon>
        新增物品
      </el-button>
      <el-button @click="fetchData">
        <el-icon><Refresh /></el-icon>
        刷新
      </el-button>
    </div>
    
    <el-table :data="itemStore.items" v-loading="itemStore.loading" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="title" label="名称" width="200" />
      <el-table-column prop="description" label="描述" min-width="200" />
      <el-table-column prop="price" label="价格" width="120">
        <template #default="{ row }">
          ¥{{ row.price.toFixed(2) }}
        </template>
      </el-table-column>
      <el-table-column prop="tax" label="税费" width="120">
        <template #default="{ row }">
          {{ row.tax ? `¥${row.tax.toFixed(2)}` : '-' }}
        </template>
      </el-table-column>
      <el-table-column prop="owner_id" label="所有者ID" width="100" />
      <el-table-column label="操作" fixed="right" width="200">
        <template #default="{ row }">
          <el-button type="primary" size="small" @click="handleEdit(row)">
            编辑
          </el-button>
          <el-button type="danger" size="small" @click="handleDelete(row)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑物品' : '新增物品'"
      width="500px"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="名称" prop="title">
          <el-input v-model="form.title" placeholder="请输入物品名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入物品描述"
          />
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input-number
            v-model="form.price"
            :min="0"
            :precision="2"
            placeholder="请输入价格"
          />
        </el-form-item>
        <el-form-item label="税费" prop="tax">
          <el-input-number
            v-model="form.tax"
            :min="0"
            :precision="2"
            placeholder="请输入税费（可选）"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, FormInstance, FormRules } from 'element-plus'
import { Plus, Refresh } from '@element-plus/icons-vue'
import { useItemStore, type Item } from '@/stores/item'
import { useAuthStore } from '@/stores/auth'

const itemStore = useItemStore()
const authStore = useAuthStore()

const dialogVisible = ref(false)
const submitLoading = ref(false)
const isEdit = ref(false)
const formRef = ref<FormInstance>()
const currentId = ref<number | null>(null)

const form = reactive({
  title: '',
  description: '',
  price: 0,
  tax: undefined as number | undefined,
  owner_id: 0
})

const rules: FormRules = {
  title: [
    { required: true, message: '请输入物品名称', trigger: 'blur' }
  ],
  price: [
    { required: true, message: '请输入价格', trigger: 'blur' },
    { type: 'number', min: 0.01, message: '价格必须大于 0', trigger: 'blur' }
  ]
}

onMounted(() => {
  fetchData()
})

async function fetchData() {
  try {
    await itemStore.fetchItems()
  } catch (error) {
    ElMessage.error('获取物品列表失败')
  }
}

function handleAdd() {
  isEdit.value = false
  Object.assign(form, {
    title: '',
    description: '',
    price: 0,
    tax: undefined,
    owner_id: authStore.userInfo?.id || 0
  })
  currentId.value = null
  dialogVisible.value = true
}

function handleEdit(row: Item) {
  isEdit.value = true
  Object.assign(form, {
    title: row.title,
    description: row.description || '',
    price: row.price,
    tax: row.tax,
    owner_id: row.owner_id
  })
  currentId.value = row.id
  dialogVisible.value = true
}

async function handleDelete(row: Item) {
  try {
    await ElMessageBox.confirm('确定要删除该物品吗？', '提示', {
      type: 'warning'
    })
    await itemStore.deleteItem(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

async function handleSubmit() {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitLoading.value = true
      try {
        if (isEdit.value && currentId.value) {
          await itemStore.updateItem(currentId.value, form)
          ElMessage.success('更新成功')
        } else {
          await itemStore.createItem(form)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        fetchData()
      } catch (error: any) {
        ElMessage.error(error.response?.data?.detail || '操作失败')
      } finally {
        submitLoading.value = false
      }
    }
  })
}
</script>

<style scoped>
.items-container {
  padding: 20px;
}

.toolbar {
  margin-bottom: 20px;
}
</style>
