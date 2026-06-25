<template>
  <el-config-provider>
    <router-view v-slot="{ Component, route }">
      <component :is="Component" :key="route.path" />
    </router-view>
  </el-config-provider>
</template>

<script setup lang="ts" name="App">
import { ElConfigProvider } from 'element-plus';
</script>

<style scoped lang="less">
#app {
  min-height: 100vh;
  background-color: #f5f7fa;
}
</style>
