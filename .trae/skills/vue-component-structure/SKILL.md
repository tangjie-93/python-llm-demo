***
name: "vue-component-structure"
description: "定义Vue组件的基本规范，包括文件命名、组件命名、组件结构顺序和目录结构。当创建或审查Vue单文件组件时触发此技能。"
trigger:

- "*.vue"
- "创建Vue组件"
- "审查Vue组件"
- "Vue组件规范"
- "vue-component"
- ".vue文件"
- "组件命名"
- "组件结构"
- "文件命名"
- "目录结构"

***

# Vue 组件基本规范

## 一、文件命名规范

### 1. 组件文件命名规则
- **组件文件使用大驼峰命名法（PascalCase）**，例如 `VimEditorView.vue`、`ClipboardAlternative.vue`
- **文件名应该清晰表达组件功能**

### 2. 不同类型组件的命名约定

#### 通用基础组件
- 以 `Base` 开头，例如 `BaseTable.vue`、`BaseForm.vue`
- 用于项目中通用的基础组件

#### 业务组件
- 以模块名称开头，例如 `OrderList.vue`、`FactorySelect.vue`
- 体现业务功能的组件

#### 页面组件
- 以 `Page` 结尾，例如 `UserProfilePage.vue`、`DashboardPage.vue`
- 用于页面级别的组件

#### 布局组件
- 以 `Layout` 开头，例如 `LayoutHeader.vue`、`LayoutSidebar.vue`
- 用于页面布局的组件

### 3. 入口文件命名
- 组件目录下的入口文件统一为 `index.vue`
- 便于导入时使用目录路径

## 二、组件命名规范

### 1. 组件名命名规则
- **组件名使用小驼峰命名法（camelCase）**
- **组件名应该由多个单词组成**，避免与 HTML 原生标签冲突
- **组件 `name` 属性与文件名保持一致**

```vue
<script setup lang="ts" name="vimEditorView">
```

### 2. 命名约定

#### 基础组件命名
- 以 `Base` 开头，例如 `BaseButton`、`BaseInput`
- 用于项目中通用的基础组件

#### 业务组件命名
- 以模块名称开头，例如 `OrderList`、`FactorySelect`
- 体现业务功能的组件

#### 布局组件命名
- 以 `Layout` 开头，例如 `LayoutHeader`、`LayoutSidebar`
- 用于页面布局的组件

#### 高阶组件命名
- 以 `With` 开头，例如 `WithLoading`、`WithAuth`
- 用于增强组件功能的 HOC

### 3. 命名最佳实践

#### 语义化命名
- 组件名应该清晰表达其功能
- 避免使用过于抽象或简化的名称

#### 避免命名冲突
- 确保组件名不与 HTML 原生标签冲突
- 避免与第三方库的组件名重复

#### 一致性原则
- 同一项目中的组件命名风格保持一致
- 遵循团队约定的命名规范

## 三、组件结构顺序

每个 `.vue` 文件按照以下顺序组织代码：

```vue
<template>
    <!-- 模板内容 -->
</template>

<script setup lang="ts">
// 脚本逻辑
</script>

<style scoped lang="less">
/* 样式内容 */
</style>
```

## 四、目录结构规范

### 1. 组件目录结构
```
组件目录/
├── index.vue           # 组件入口文件
├── components/         # 组件依赖的子组件（可选）
└── hooks/              # 组件专用的自定义 Hooks（可选）
```

### 2. 目录命名规范
- **目录名使用小驼峰命名法（camelCase）**
- 目录名应该与组件功能相关

### 3. 文件组织原则

#### 单一职责原则
- 每个文件只负责一个明确的功能
- 避免在一个文件中包含过多不相关的逻辑

#### 模块化组织
- 相关文件组织在同一目录下
- 通过目录结构体现组件间的层级关系

#### 可维护性原则
- 文件结构应该便于理解和维护
- 新成员能够快速理解项目结构

## 五、结构顺序的重要性

### 1. 可读性
- 统一的代码组织顺序提高可读性
- 便于快速定位不同部分的代码

### 2. 维护性
- 标准化的结构便于团队协作
- 减少代码审查时的认知负担

### 3. 一致性
- 确保项目中所有组件结构一致
- 便于自动化工具处理

## 六、命名错误示例

### ❌ 文件命名错误示例
```
// 文件命名不规范
userform.vue           // 应该使用大驼峰
base_button.vue        // 应该使用大驼峰

// 目录结构混乱
components/
  ├── user/           // 目录名应该小驼峰
  │   ├── form.vue    // 文件名不规范
  │   └── list.vue    // 文件名不规范
  └── utils/          // 工具目录不应该放在components下
```

### ✅ 文件命名正确示例
```
// 规范的文件命名
UserForm.vue
BaseButton.vue
OrderList.vue

// 规范的目录结构
components/
  ├── user/
  │   ├── UserForm.vue
  │   └── UserList.vue
  ├── base/
  │   ├── BaseButton.vue
  │   └── BaseInput.vue
  └── layout/
      ├── LayoutHeader.vue
      └── LayoutSidebar.vue
```

### ❌ 组件命名错误示例
```vue
<!-- 单单词组件名，容易与HTML标签冲突 -->
<script setup lang="ts" name="button">

<!-- 使用大驼峰作为组件名 -->
<script setup lang="ts" name="Button">

<!-- 组件名与文件名不一致 -->
<!-- 文件：UserForm.vue -->
<script setup lang="ts" name="form">
```

### ✅ 组件命名正确示例
```vue
<!-- 多单词小驼峰命名 -->
<script setup lang="ts" name="userForm">

<!-- 基础组件 -->
<script setup lang="ts" name="baseButton">

<!-- 业务组件 -->
<script setup lang="ts" name="orderList">
```

## 七、相关技能参考

- **Script 编写规范**：参考 `vue-component-script` 技能
- **Template 编写规范**：参考 `vue-template-standards` 技能
- **Style 编写规范**：参考 `vue-component-style` 技能
- **项目目录结构**：参考 `vue-project-structure` 技能
