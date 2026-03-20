<template>
  <div class="users-container">
    <div class="toolbar">
      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon>
        新增用户
      </el-button>
      <el-button @click="fetchData">
        <el-icon><Refresh /></el-icon>
        刷新
      </el-button>
    </div>
    
    <el-table :data="userStore.users" v-loading="userStore.loading" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="username" label="用户名" width="150" />
      <el-table-column prop="email" label="邮箱" width="200" />
      <el-table-column prop="full_name" label="全名" width="150" />
      <el-table-column prop="is_active" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'danger'">
            {{ row.is_active ? '激活' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
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
      :title="isEdit ? '编辑用户' : '新增用户'"
      width="500px"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="全名" prop="full_name">
          <el-input v-model="form.full_name" placeholder="请输入全名" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!isEdit">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" />
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
import { useUserStore, type User } from '@/stores/user'

const userStore = useUserStore()

const dialogVisible = ref(false)
const submitLoading = ref(false)
const isEdit = ref(false)
const formRef = ref<FormInstance>()
const currentId = ref<number | null>(null)

const form = reactive({
  username: '',
  email: '',
  full_name: '',
  password: ''
})

const rules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 位', trigger: 'blur' }
  ]
}

onMounted(() => {
  fetchData()
})

async function fetchData() {
  try {
    await userStore.fetchUsers()
  } catch (error) {
    ElMessage.error('获取用户列表失败')
  }
}

function handleAdd() {
  isEdit.value = false
  Object.assign(form, { username: '', email: '', full_name: '', password: '' })
  currentId.value = null
  dialogVisible.value = true
}

function handleEdit(row: User) {
  isEdit.value = true
  Object.assign(form, {
    username: row.username,
    email: row.email,
    full_name: row.full_name || '',
    password: ''
  })
  currentId.value = row.id
  dialogVisible.value = true
}

async function handleDelete(row: User) {
  try {
    await ElMessageBox.confirm('确定要删除该用户吗？', '提示', {
      type: 'warning'
    })
    await userStore.deleteUser(row.id)
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
          await userStore.updateUser(currentId.value, form)
          ElMessage.success('更新成功')
        } else {
          await userStore.createUser(form)
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
.users-container {
  padding: 20px;
}

.toolbar {
  margin-bottom: 20px;
}
</style>
