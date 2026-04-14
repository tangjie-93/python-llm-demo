***

name: "vue-component-script"
description: "定义Vue组件Script部分的编写规范，包括Props定义、Emits定义、代码组织顺序、代码长度限制和注释规范。当编写或审查Vue组件的Script部分时触发此技能。"
trigger:

- "\*.vue"
- "创建Vue组件"
- "审查Vue组件"
- "Vue组件规范"
- "vue-component"
- ".vue文件"
- "Script规范"
- "Props定义"
- "Emits定义"
- "代码组织"
- "注释规范"

***

# Vue Script 编写规范

## 一、组件拆分原则

- **单一职责**：一个组件只负责一个功能
- **复用性**：可复用的逻辑抽离为 Hook 或组件
- **可维护性**：组件代码行数控制在 300 行以内

## 二、代码长度限制

- **单个组件**：不超过 300 行
- **单个函数**：不超过 50 行
- **超过限制**：考虑拆分为子组件或提取为 Hook

## 三、Props 定义

- 使用 `defineProps` 结合 TypeScript 泛型定义
- 必要的属性必须显式声明
- 默认值使用 `withDefaults` 定义

```ts
// 正确示例
const props = defineProps<{
    editModalVisible: boolean;
    serialNumber: string;
    disabled?: boolean; // 可选属性
}>();

// 带默认值的写法
const props = withDefaults(
    defineProps<{
        editModalVisible: boolean;
        serialNumber: string;
        disabled?: boolean;
    }>(),
    {
        disabled: false
    }
);
```

## 四、Emits 定义

- 使用 `defineEmits` 结合 TypeScript 泛型定义
- 事件名使用小驼峰命名法
- 遵循 Vue 双向绑定规范，`update:propName` 格式

```ts
// 正确示例
const emit = defineEmits<{
    saveEdit: [serialNumber: string]; // 事件名: [参数1类型, 参数2类型, ...]
    cancelEdit: [];
    'update:editModalVisible': [visible: boolean]; // 双向绑定事件
}>();

// 调用示例
emit('saveEdit', props.serialNumber);
emit('update:editModalVisible', false);
```

## 五、代码组织顺序

```ts
<script setup lang="ts">
// 1. 组件名定义（如果使用选项式API需要）
// defineOptions({ name: 'ComponentName' })

// 2. 类型导入
import type { PropType } from 'vue';
import type { OrderItem } from '@/types/order';

// 3. 依赖导入
import { ref, computed, watch, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import { useOrderHook } from './hooks/useOrderHook';

// 4. Props 定义
const props = defineProps<{
    data: OrderItem;
    loading?: boolean;
}>();

// 5. Emits 定义
const emit = defineEmits<{
    submit: [data: OrderItem];
    'update:loading': [value: boolean];
}>();

// 6. 响应式状态定义
const localData = ref<OrderItem>({} as OrderItem);
const isSubmitting = ref(false);

// 7. 计算属性
const isValid = computed(() => {
    return localData.value.id && localData.value.name;
});

// 8. 方法定义
const handleSubmit = async () => {
    if (!isValid.value) return;
    isSubmitting.value = true;
    try {
        emit('submit', localData.value);
    } finally {
        isSubmitting.value = false;
    }
};

// 9. 生命周期钩子
onMounted(() => {
    localData.value = { ...props.data };
});

// 10. Watch 监听
watch(() => props.data, (newVal) => {
    localData.value = { ...newVal };
}, { deep: true });
</script>
```

## 六、注释规范

### 6.1 Props 和 Emits 注释

每个 Props 和 Emits 都应该有明确的用途说明：

```ts
const props = defineProps<{
    /** 是否显示编辑模态框 */
    editModalVisible: boolean;
    /** 序列号 */
    serialNumber: string;
    /** 是否禁用 */
    disabled?: boolean;
}>();

const emit = defineEmits<{
    /** 保存编辑操作 */
    saveEdit: [serialNumber: string];
    /** 取消编辑操作 */
    cancelEdit: [];
    /** 更新编辑模态框显示状态 */
    'update:editModalVisible': [visible: boolean];
}>();
```

### 6.2 函数/方法注释

```ts
/**
 * 函数功能描述
 * @param param1 参数1说明
 * @param param2 参数2说明
 * @returns 返回值说明
 */
function doSomething(param1: string, param2: number): boolean {
    // ...
}
```

### 6.3 行内注释

- 复杂逻辑必须添加注释
- 使用 `//` 进行单行注释
- 注释解释"为什么"而不是"是什么"

