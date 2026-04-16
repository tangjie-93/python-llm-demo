<template>
    <div class="user-info">
        <el-dropdown trigger="click" @command="handleCommand">
            <div class="user-info__trigger">
                <div class="user-info__avatar">
                    <el-icon :size="20"><UserFilled /></el-icon>
                </div>
                <span v-if="authStore.userInfo" class="user-info__name">
                    {{ authStore.userInfo.username }}
                </span>
                <el-icon class="user-info__arrow"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
                <el-dropdown-menu>
                    <el-dropdown-item command="logout">
                        <el-icon class="user-info__menu-icon"><SwitchButton /></el-icon>
                        <span>退出登录</span>
                    </el-dropdown-item>
                </el-dropdown-menu>
            </template>
        </el-dropdown>
    </div>
</template>

<script setup lang="ts" name="UserInfo">
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { ElMessage } from 'element-plus';
import { UserFilled, ArrowDown, SwitchButton } from '@element-plus/icons-vue';

const router = useRouter();
const authStore = useAuthStore();

/**
 * 处理下拉菜单命令
 */
function handleCommand(command: string) {
    if (command === 'logout') {
        handleLogout();
    }
}

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
    justify-content: flex-end;
    padding: 0 12px;

    &__trigger {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 16px;
        border-radius: 24px;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        background: transparent;

        &:hover {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(8px);
        }

        &:active {
            transform: scale(0.98);
        }
    }

    &__avatar {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.9);
        color: #409eff;
        transition: all 0.3s ease;

        .user-info__trigger:hover & {
            background: #fff;
            transform: scale(1.05);
        }
    }

    &__name {
        font-size: 15px;
        font-weight: 600;
        color: #fff;
        letter-spacing: 0.3px;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }

    &__arrow {
        font-size: 14px;
        color: rgba(255, 255, 255, 0.8);
        transition: transform 0.3s ease;
        margin-left: 2px;
    }

    &__menu-icon {
        margin-right: 8px;
        font-size: 16px;
        color: #f56c6c;
    }
}

:deep(.el-dropdown-menu__item) {
    padding: 10px 16px;
    font-size: 14px;

    &:hover {
        background-color: #f5f7fa;
    }

    &--divided {
        border-top: 1px solid #ebeef5;
    }
}

:deep(.el-dropdown-menu) {
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    border: 1px solid #ebeef5;
    padding: 8px 0;
}
</style>
