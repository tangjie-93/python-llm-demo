---
name: "vue-component-communication"
description: "定义Vue组件通信规范，包括Props向下传递、Events向上传递和跨组件通信。当编写或审查Vue组件的通信逻辑时触发此技能。"
trigger:
  - "*.vue"
  - "创建Vue组件"
  - "审查Vue组件"
  - "Vue组件规范"
  - "vue-component"
  - ".vue文件"
  - "组件通信"
  - "Props传递"
  - "Events传递"
---

# Vue 组件通信规范

## 一、Props 向下传递

- 父组件通过 Props 向子组件传递数据
- Props 应该是单向数据流

## 二、Events 向上传递

- 子组件通过 Events 向父组件传递消息
- 复杂状态使用状态管理（Pinia/Vuex）

## 三、跨组件通信

- 兄弟组件通信：通过父组件中转或使用 Event Bus
- 深层嵌套：使用 Provide/Inject
- 全局状态：使用 Pinia
