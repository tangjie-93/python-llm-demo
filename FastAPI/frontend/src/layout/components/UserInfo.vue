<template>
    <div class="user-info">
        <span v-if="authStore.userInfo" class="user-info__name">
            {{ authStore.userInfo.username }}
        </span>
        <el-button
            v-if="authStore.isLoggedIn"
            type="primary"
            plain
            @click="handleLogout"
        >
            退出登录
        </el-button>
    </div>
</template>

<script setup lang="ts" name="UserInfo">
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { ElMessage } from 'element-plus';

const router = useRouter();
const authStore = useAuthStore();

/**
 * 处理退出登录
 * 显示成功提示，延迟后执行退出操作并跳转到登录页
 */
function handleLogout() {
    ElMessage.success({
        message: '退出成功',
        duration: 500
    });
    // 延迟跳转，让用户看到成功提示
    setTimeout(() => {
        authStore.logout();
        router.push('/login');
    }, 500);
}
</script>

<style scoped lang="less">
.user-info {
    display: flex;
    align-items: center;
    gap: 10px;

    &__name {
        font-size: 14px;
    }
}
</style>
