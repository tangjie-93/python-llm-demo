---
name: "vue-template-standards"
description: "定义Vue组件Template部分的编写规范，包括模板缩进、属性顺序、组件标签和插槽使用。当编写或审查Vue组件的Template部分时触发此技能。"
trigger:
  - "*.vue"
  - "创建Vue组件"
  - "审查Vue组件"
  - "Vue组件规范"
  - "vue-component"
  - ".vue文件"
  - "Template规范"
  - "模板编写"
---

# Vue Template 编写规范

## 一、模板缩进

- 使用 4 个空格缩进
- 保持层级清晰

## 二、模板拆分规范

- 如果在 template 标签里的 HTML 标签超过 50 行，需要将该 Vue 组件根据功能拆分为多个 Vue 组件
- 在当前目录下创建 `components` 文件夹，将创建的 Vue 组件放在 components 文件夹下
- 确保组件之间的引用关系清晰，避免循环依赖
- 详细目录结构规范参考 vue-component-structure 技能

## 三、属性顺序

元素属性按照以下顺序排列：

1. 指令（v-if, v-for, v-model 等）
2. 自定义指令（v-custom）
3. 原生属性（id, class, style 等）
4. 事件绑定（@click, @change 等）
5. 其他属性

```vue
<!-- 正确示例 -->
<a-button
    v-if="isVisible"
    v-permission="'order:edit'"
    id="submit-btn"
    class="primary-btn"
    :class="{ active: isActive }"
    type="primary"
    :loading="isLoading"
    :disabled="isDisabled"
    @click="handleSubmit"
    @mouseenter="handleMouseEnter"
>
    提交
</a-button>
```

## 四、组件标签

- 自闭合组件：`<MyComponent />`
- 有插槽的组件：`<MyComponent></MyComponent>`

## 五、插槽使用

```vue
<!-- 默认插槽 -->
<BaseTable :data="list">
    <template #default="{ row }">
        <span>{{ row.name }}</span>
    </template>
</BaseTable>

<!-- 具名插槽 -->
<BaseModal v-model:visible="visible">
    <template #title>
        <span>自定义标题</span>
    </template>
    <template #footer>
        <a-button @click="handleCancel">取消</a-button>
        <a-button type="primary" @click="handleConfirm">确定</a-button>
    </template>
</BaseModal>
```
