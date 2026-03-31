<template>
  <div class="layout-container">
    <!-- 头部 -->
    <header class="layout-header">
      <div class="header-left">
        <h1>FastAPI Demo</h1>
      </div>
      <div class="header-right">
        <span v-if="authStore.userInfo">{{ authStore.userInfo.username }}</span>
        <el-button
          v-if="authStore.isLoggedIn"
          type="primary"
          plain
          @click="handleLogout"
        >
          退出登录
        </el-button>
      </div>
    </header>

    <!-- 内容区域 -->
    <main class="layout-content">
      <!-- 左侧菜单 -->
      <aside class="layout-sidebar">
        <el-menu
          :default-active="activeMenu"
          class="sidebar-menu"
          @select="handleMenuSelect"
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
            <span>项目管理</span>
          </el-menu-item>
        </el-menu>
      </aside>

      <!-- 右侧内容 -->
      <section class="layout-main">
        <router-view v-slot="{ Component }">
          <transition
            name="slide-fade"
            mode="out-in"
          >
            <component :is="Component" />
          </transition>
        </router-view>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { House, User, Goods } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';

const router = useRouter();
const authStore = useAuthStore();

// 计算当前激活的菜单
const activeMenu = computed(() => {
  return router.currentRoute.value.path;
});

// 处理菜单选择
function handleMenuSelect(key: string) {
  router.push(key);
}

// 处理退出登录
function handleLogout() {
  ElMessage.success({
    message: '退出成功',
    duration: 500 // 1.5秒
  });
  // 延迟跳转，让用户看到成功提示
  setTimeout(() => {
    authStore.logout();
    router.push('/login');
  }, 500);
}
</script>

<style scoped>
.layout-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.layout-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
  background-color: #409EFF;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-left h1 {
  font-size: 20px;
  font-weight: bold;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.layout-content {
  display: flex;
  flex: 1;
  background-color: #f5f7fa;
}

.layout-sidebar {
  width: 200px;
  background-color: white;
  border-right: 1px solid #e4e7ed;
  box-shadow: 2px 0 6px rgba(0, 21, 41, 0.05);
}

.sidebar-menu {
  border-right: none;
  height: 100%;
}

.layout-main {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

</style>