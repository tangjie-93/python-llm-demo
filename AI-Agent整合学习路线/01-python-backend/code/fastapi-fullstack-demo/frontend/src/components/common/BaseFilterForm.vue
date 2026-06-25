<template>
  <div class="base-filter-form">
    <el-form :inline="true" :model="modelValue">
      <slot />
      <el-form-item>
        <el-button type="primary" @click="handleFilter">
          <el-icon><Search /></el-icon>
          {{ filterButtonText }}
        </el-button>
        <el-button @click="handleReset">
          <el-icon><RefreshLeft /></el-icon>
          {{ resetButtonText }}
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts" name="BaseFilterForm">
import { Search, RefreshLeft } from '@element-plus/icons-vue';

interface Props {
  modelValue: Record<string, any>;
  filterButtonText?: string;
  resetButtonText?: string;
}

withDefaults(defineProps<Props>(), {
  filterButtonText: '筛选',
  resetButtonText: '重置'
});

const emit = defineEmits<{
  'update:modelValue': [value: Record<string, any>];
  filter: [];
  reset: [];
}>();

function handleFilter() {
  emit('filter');
}

function handleReset() {
  emit('reset');
}
</script>

<style scoped lang="less">
.base-filter-form {
  width: 100%;
}
:deep(.el-form--inline .el-form-item) {
  margin-bottom: 0 !important;
}
</style>
