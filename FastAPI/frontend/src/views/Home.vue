<template>
  <div class="home-container">
    <el-card class="welcome-card">
      <template #header>
        <div class="card-header">
          <span>欢迎访问 FastAPI 后台管理系统</span>
        </div>
      </template>
      <div class="welcome-content">
        <p>您好，{{ authStore.userInfo?.username }}！</p>
        <p>这是系统的首页，您可以通过左侧菜单访问不同的功能模块。</p>
        <div class="stats-container">
          <el-statistic
            title="用户数量"
            :value="userCount"
          />
          <el-statistic
            title="项目数量"
            :value="itemCount"
          />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const userCount = ref(0);
const itemCount = ref(0);

onMounted(() => {
  authStore.fetchUserInfo();
  // 模拟获取统计数据
  userCount.value = 10;
  itemCount.value = 20;
});
</script>

<style scoped>
.home-container {
  padding: 20px;
}

.welcome-card {
  margin-bottom: 20px;
}

.card-header {
  font-size: 18px;
  font-weight: bold;
}

.welcome-content {
  padding: 20px 0;
}

.welcome-content p {
  margin-bottom: 15px;
  font-size: 16px;
}

.stats-container {
  display: flex;
  gap: 20px;
  margin-top: 30px;
}
</style>
