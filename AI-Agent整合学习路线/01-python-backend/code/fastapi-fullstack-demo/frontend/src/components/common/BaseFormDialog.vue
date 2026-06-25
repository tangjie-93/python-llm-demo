<template>
  <el-dialog
    v-model="dialogVisible"
    :title="title"
    :width="width"
    :close-on-click-modal="false"
    destroy-on-close
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      :label-width="labelWidth"
    >
      <slot :form="formData" />
    </el-form>

    <template #footer>
      <el-button @click="handleCancel">
        {{ cancelText }}
      </el-button>
      <el-button
        type="primary"
        :loading="submitLoading"
        @click="handleSubmit"
      >
        {{ confirmText }}
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts" name="BaseFormDialog">
import { ref, watch } from 'vue';
import type { FormInstance, FormRules } from 'element-plus';

interface Props {
  modelValue: boolean;
  title: string;
  formData: Record<string, any>;
  rules?: FormRules;
  width?: string;
  labelWidth?: string;
  cancelText?: string;
  confirmText?: string;
  submitLoading?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  width: '500px',
  labelWidth: '80px',
  cancelText: '取消',
  confirmText: '确定',
  submitLoading: false,
  rules: () => ({})
});

const emit = defineEmits<{
  'update:modelValue': [value: boolean];
  cancel: [];
  submit: [formRef: FormInstance | undefined];
}>();

const formRef = ref<FormInstance>();

const dialogVisible = ref(props.modelValue);

watch(() => props.modelValue, (val) => {
  dialogVisible.value = val;
});

watch(dialogVisible, (val) => {
  emit('update:modelValue', val);
  if (!val) {
    emit('cancel');
  }
});

function handleCancel() {
  dialogVisible.value = false;
}

async function handleSubmit() {
  if (!formRef.value) return;
  
  try {
    await formRef.value.validate();
    emit('submit', formRef.value);
  } catch (error) {
    console.error('表单验证失败:', error);
  }
}
</script>

<style scoped lang="less">
// 无需额外样式
</style>
