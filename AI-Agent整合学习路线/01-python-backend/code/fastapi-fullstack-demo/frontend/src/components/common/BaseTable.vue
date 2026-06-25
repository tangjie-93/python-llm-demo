<template>
  <div class="base-table-wrapper">
    <el-table
      v-loading="loading"
      :data="data"
      :stripe="stripe"
      :border="border"
      :height="height"
      :max-height="maxHeight"
      class="base-table"
    >
      <slot />
    </el-table>
  </div>
</template>

<script setup lang="ts" name="BaseTable">
interface Props {
  data?: any[];
  loading?: boolean;
  stripe?: boolean;
  border?: boolean;
  height?: number | string;
  maxHeight?: number | string;
}

withDefaults(defineProps<Props>(), {
  data: () => [],
  loading: false,
  stripe: true,
  border: false,
  height: undefined,
  maxHeight: undefined
});
</script>

<style scoped lang="less">
.base-table-wrapper {
  width: 100%;
  height: 100%;
}

.base-table {
  width: 100%;
  display: block;
}

:deep(.el-table) {
  width: 100% !important;
}

:deep(.el-table__inner-wrapper) {
  width: 100%;
}
</style>
