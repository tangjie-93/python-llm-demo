<template>
    <header class="app-header">
        <div class="app-header__left">
            <h1>FastAPI Demo</h1>
        </div>
        <div class="app-header__right">
            <UserInfo />
        </div>
    </header>
</template>

<script setup lang="ts" name="AppHeader">
import UserInfo from './UserInfo.vue';
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
        h1 {
            font-size: 20px;
            font-weight: bold;
            margin: 0;
        }
    }

    &__right {
        display: flex;
        align-items: center;
        gap: 10px;
    }
}
</style>
