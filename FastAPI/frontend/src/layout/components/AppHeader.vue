<template>
    <header class="app-header">
        <div class="app-header__left">
            <h1>FastAPI Demo</h1>
            <Breadcrumb v-if="showBreadcrumb" class="app-header__breadcrumb" />
        </div>
        <div class="app-header__right">
            <UserInfo />
        </div>
    </header>
</template>

<script setup lang="ts" name="AppHeader">
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import UserInfo from './UserInfo.vue';
import Breadcrumb from './Breadcrumb.vue';

const route = useRoute();

// 判断是否显示面包屑（登录页和注册页不显示）
const showBreadcrumb = computed(() => {
    return !['Login', 'Register'].includes(route.name as string);
});
</script>

<style scoped lang="less">
.app-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    height: 60px;
    background-color: #409EFF;
    color: white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

    &__left {
        display: flex;
        gap: 2px;

        h1 {
            font-size: 20px;
            font-weight: bold;
            margin: 0;
            width: 180px;
        }
    }

    &__right {
        display: flex;
        align-items: center;
        gap: 10px;
    }
}
</style>
