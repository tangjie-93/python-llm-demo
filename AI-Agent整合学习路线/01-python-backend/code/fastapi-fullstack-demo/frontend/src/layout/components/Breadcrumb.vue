<template>
    <div class="breadcrumb">
        <template v-for="(item, index) in breadcrumbs" :key="item.path">
            <div 
                class="breadcrumb__item"
                :class="{ 'breadcrumb__item--active': index === breadcrumbs.length - 1 }"
                @click="!isLast(index) && navigateTo(item.path)"
            >
                <span 
                    class="breadcrumb__text"
                    :class="{ 'breadcrumb__text--active': index === breadcrumbs.length - 1 }"
                >
                    {{ item.title }}
                </span>
            </div>
            <span 
                v-if="!isLast(index)" 
                class="breadcrumb__separator"
            >
                /
            </span>
        </template>
    </div>
</template>

<script setup lang="ts" name="Breadcrumb">
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';

interface BreadcrumbItem {
    path: string;
    title: string;
}

const route = useRoute();
const router = useRouter();

// 路由名称映射
const routeTitleMap: Record<string, string> = {
    'Home': '首页',
    'Users': '用户管理',
    'Items': '物品管理',
    'Posts': '文章管理',
    'Tags': '标签管理',
    'Login': '登录',
    'Register': '注册'
};

// 计算面包屑列表
const breadcrumbs = computed<BreadcrumbItem[]>(() => {
    const matchedRoutes = route.matched.filter(record => record.name && record.name !== 'Layout');
    
    if (matchedRoutes.length === 0) {
        return [];
    }

    return matchedRoutes.map(record => ({
        path: record.path,
        title: (record.meta.title as string) || routeTitleMap[record.name as string] || record.name as string
    }));
});

// 判断是否是最后一项
const isLast = (index: number): boolean => {
    return index === breadcrumbs.value.length - 1;
};

// 导航到指定路径
const navigateTo = (path: string) => {
    router.push(path);
};
</script>

<style scoped lang="less">
.breadcrumb {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;

    &__item {
        display: flex;
        align-items: center;
        cursor: pointer;
        transition: all 0.2s;
        opacity: 0.8;

        &:hover {
            opacity: 1;
            
            .breadcrumb__text {
                color: white;
                text-decoration: underline;
            }
        }

        &--active {
            cursor: default;
            pointer-events: none;
            opacity: 1;
            font-weight: 500;
        }
    }

    &__text {
        color: rgba(255, 255, 255, 0.9);
        text-decoration: none;
        transition: all 0.2s;

        &--active {
            color: white;
        }
    }

    &__separator {
        color: rgba(255, 255, 255, 0.6);
        margin: 0 4px;
        font-weight: 300;
    }
}
</style>
