<template>
    <aside class="app-sidebar">
        <el-menu
            :default-active="activeMenu"
            class="app-sidebar__menu"
            @select="handleMenuSelect"
        >
            <el-menu-item index="/admin/home">
                <el-icon><House /></el-icon>
                <span>首页</span>
            </el-menu-item>
            <el-menu-item index="/admin/users">
                <el-icon><User /></el-icon>
                <span>用户管理</span>
            </el-menu-item>
            <el-menu-item index="/admin/items">
                <el-icon><Goods /></el-icon>
                <span>项目管理</span>
            </el-menu-item>
            <el-menu-item index="/admin/posts">
                <el-icon><Document /></el-icon>
                <span>博客文章</span>
            </el-menu-item>
            <el-menu-item index="/admin/tags">
                <el-icon><CollectionTag /></el-icon>
                <span>标签管理</span>
            </el-menu-item>
        </el-menu>
    </aside>
</template>

<script setup lang="ts" name="AppSidebar">
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { House, User, Goods, Document, CollectionTag } from '@element-plus/icons-vue';

const router = useRouter();

/**
 * 计算当前激活的菜单项
 * 根据当前路由路径确定高亮的菜单
 */
const activeMenu = computed(() => {
    return router.currentRoute.value.path;
});

/**
 * 处理菜单选择
 * @param key - 选中的菜单项索引（路由路径）
 */
function handleMenuSelect(key: string) {
    router.push(key);
}
</script>

<style scoped lang="less">
.app-sidebar {
    width: 200px;
    background-color: white;
    border-right: 1px solid #e4e7ed;
    box-shadow: 2px 0 6px rgba(0, 21, 41, 0.05);

    &__menu {
        border-right: none;
        height: 100%;
    }
}
</style>
