---
name: "vue-hook-standards"
description: "强制执行Vue Hook编码规范，包括命名约定、类型定义和代码组织。当创建或审查Vue项目中的自定义Hook（useXxx）时触发此技能。"
---

# Vue Hook 编写规范

## 一、基本规范

### 1. 命名规范

- **文件名**：小驼峰命名法（camelCase），以 `use` 开头，例如 `useClipboard.ts`、`useOrderHook.ts`
- **函数名**：与文件名保持一致，同样以 `use` 开头
- **业务 Hook**：名称体现所属模块，例如 `useOrderHook`、`useFactoryHook`

### 2. 存放位置

- **全局通用 Hook**：`src/hooks/` 目录下
- **业务模块专属 Hook**：对应模块的 `hooks/` 目录下，例如 `src/views/order/hooks/`
- **组件专属 Hook**：对应组件目录下的 `hooks/` 目录

## 二、类型定义规范

### 1. 入参类型定义

- Hook 入参统一为 `options` 配置对象
- 入参接口使用 `HookNameOptions` 命名方式
- 所有配置项提供合理的默认值

```ts
// 正确示例
export interface ClipboardOptions {
    autoParse?: boolean;
    trimCells?: boolean;
    autoFocus?: boolean;
    showMessages?: boolean;
}

export function useClipboard(options: ClipboardOptions = {}) {
    const { autoParse = true, trimCells = true, autoFocus = true, showMessages = true } = options;
    // ...
}
```

### 2. 返回值类型定义

- 复杂返回值需要定义返回接口
- 状态与方法分开定义，结构清晰

```ts
// 正确示例
export interface ClipboardData {
    excelData: string[][];
    isLoading: boolean;
    error: string;
    status: {
        focus: boolean;
        permission: boolean;
        https: boolean;
    };
}

export interface ClipboardActions {
    readClipboardData: () => Promise<string[][] | null>;
    clearData: () => void;
    fixFocusIssue: () => void;
}

// 返回值类型
export type UseClipboardReturn = ClipboardData & ClipboardActions;
```

### 3. 内部类型定义

- 内部使用的类型也需要明确定义
- **禁止使用 `any` 类型**

## 三、Hook 内部结构规范

Hook 内部代码按照以下顺序组织：

### 1. 依赖导入

导入顺序遵循项目规范：
1. Vue 核心库
2. 第三方库
3. 项目内部依赖
4. 类型导入

```ts
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { message } from 'ant-design-vue';
import { getOrderList } from '@/service/order';
import type { OrderItem } from '@/types/order';
```

### 2. 接口定义

- 定义 Hook 的入参、返回值等接口类型
- 接口放在函数实现之前

### 3. 函数实现结构

```ts
export function useHookName(options: HookOptions = {}) {
    // ------------------------------
    // 第一步：解构配置参数，设置默认值
    // ------------------------------
    const { param1 = true, param2 = 10 } = options;
    
    // ------------------------------
    // 第二步：定义响应式状态
    // ------------------------------
    const state = ref(initialValue);
    const computedValue = computed(() => { ... });
    
    // ------------------------------
    // 第三步：定义方法
    // ------------------------------
    const method1 = () => { ... };
    const method2 = async () => { ... };
    
    // ------------------------------
    // 第四步：生命周期钩子
    // ------------------------------
    onMounted(() => { ... });
    onUnmounted(() => { ... });
    
    // ------------------------------
    // 第五步：返回暴露的内容
    // ------------------------------
    return {
        // 状态
        state,
        computedValue,
        // 方法
        method1,
        method2
    };
}
```

## 四、代码质量要求

### 1. 单一职责原则

- 每个 Hook 只负责一个明确的功能
- 复杂逻辑拆分为多个小 Hook

### 2. 副作用管理

- 在 `onUnmounted` 中清理副作用
- 取消未完成的异步请求
- 移除事件监听器

### 3. 错误处理

- 异步操作必须包含 try-catch
- 提供错误状态和错误信息

### 4. 可测试性

- 纯逻辑与 UI 分离
- 避免直接操作 DOM（除非必要）

## 五、示例模板

```ts
import { ref, computed, onMounted, onUnmounted } from 'vue';
import type { Ref, ComputedRef } from 'vue';

// 接口定义
export interface UseExampleOptions {
    initialValue?: number;
    enabled?: boolean;
}

export interface UseExampleReturn {
    count: Ref<number>;
    doubleCount: ComputedRef<number>;
    increment: () => void;
    decrement: () => void;
}

// Hook 实现
export function useExample(options: UseExampleOptions = {}): UseExampleReturn {
    const { initialValue = 0, enabled = true } = options;
    
    // 状态定义
    const count = ref(initialValue);
    
    // 计算属性
    const doubleCount = computed(() => count.value * 2);
    
    // 方法定义
    const increment = () => {
        if (enabled) {
            count.value++;
        }
    };
    
    const decrement = () => {
        if (enabled && count.value > 0) {
            count.value--;
        }
    };
    
    // 生命周期
    onMounted(() => {
        console.log('Example hook mounted');
    });
    
    onUnmounted(() => {
        console.log('Example hook unmounted');
    });
    
    // 返回值
    return {
        count,
        doubleCount,
        increment,
        decrement
    };
}
```
