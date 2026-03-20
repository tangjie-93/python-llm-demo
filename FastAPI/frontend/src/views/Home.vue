<template>
  <div class="home-container">
    <el-container>
      <el-header>
        <div class="header-content">
          <h2>FastAPI 后台管理系统</h2>
          <div class="user-info">
            <span>欢迎，{{ authStore.userInfo?.username }}</span>
            <el-button type="danger" size="small" @click="handleLogout">
              退出
            </el-button>
          </div>
        </div>
      </el-header>
      
      <el-container>
        <el-aside width="200px">
          <el-menu
            :default-active="activeMenu"
            router
            class="el-menu-vertical"
          >
            <el-menu-item index="/home">
              <el-icon><House /></el-icon>
              <span>首页</span>
            </el-menu-item>
            <el-menu-item index="/users">
              <el-icon><User /></el-icon>
              <span>用户管理</span>
            </el-menu-item>
            <el-menu-item index="/items">
              <el-icon><Goods /></el-icon>
              <span>物品管理</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { House, User, Goods } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const activeMenu = computed(() => route.path)

onMounted(() => {
  authStore.fetchUserInfo()
})

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.home-container {
  min-height: 100vh;
}

.el-header {
  background-color: #409eff;
  color: white;
  line-height: 60px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h2 {
  margin: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.el-aside {
  background-color: #fff;
  border-right: 1px solid #e6e6e6;
}

.el-menu-vertical {
  border-right: none;
}

.el-main {
  background-color: #f5f7fa;
}
</style>
