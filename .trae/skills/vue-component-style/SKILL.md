---
name: "vue-component-style"
description: "定义Vue组件Style部分的编写规范，包括样式作用域、CSS命名规范、Less嵌套语法规范和样式变量。当编写或审查Vue组件的Style部分时触发此技能。"
trigger:
  - "*.vue"
  - "创建Vue组件"
  - "审查Vue组件"
  - "Vue组件规范"
  - "vue-component"
  - ".vue文件"
  - "Style规范"
  - "样式编写"
  - "Less规范"
---

# Vue Style 编写规范

## 一、样式作用域

- 组件样式使用 `scoped` 属性
- 全局样式在 `src/style/` 目录下定义

```vue
<style scoped lang="less">
.component-name {
    // 组件根元素使用组件名作为类名
    padding: 16px;

    &__header {
        // BEM 命名规范
        margin-bottom: 12px;
    }

    &__content {
        // 样式内容
    }
}
</style>
```

## 二、CSS 命名规范

- 使用 BEM（Block Element Modifier）命名规范
- 类名使用小写字母和连字符

```less
// Block
.user-card { }

// Element
.user-card__avatar { }
.user-card__name { }

// Modifier
.user-card--active { }
.user-card--disabled { }
```

## 三、Less 嵌套语法规范 ⭐⭐⭐⭐

**重要性**：Less 嵌套是 Vue 组件样式的核心规范，必须严格遵守

**要求**：
- **必须使用嵌套语法**组织样式，禁止平铺 CSS
- 父元素选择器使用 `&` 符号
- 伪类选择器使用 `&:hover`、`&:active` 等格式
- 媒体查询使用 `@media` 嵌套
- BEM 元素使用 `&__element` 格式
- BEM 修饰符使用 `&--modifier` 格式

**触发条件**：
- 样式文件出现平铺结构（无嵌套）
- 伪类、伪元素未使用嵌套语法
- 媒体查询未嵌套在父元素内

**✅ 正确示例**：
```less
.component {
    padding: 16px;
    background: #fff;

    &__header {
        display: flex;
        justify-content: space-between;

        &--compact {
            padding: 8px;
        }
    }

    &__content {
        margin-top: 12px;

        &:hover {
            background: #f5f5f5;
        }
    }

    &__footer {
        display: flex;
        justify-content: flex-end;

        &-button {
            margin-left: 8px;
        }
    }

    @media (max-width: 768px) {
        padding: 12px;

        &__header {
            flex-direction: column;
        }
    }

    &:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }
}
```

**❌ 错误示例**：
```less
/* 平铺结构 - 错误 */
.component {
    padding: 16px;
}

.component__header {
    display: flex;
}

.component__header--compact {
    padding: 8px;
}

.component__content:hover {
    background: #f5f5f5;
}

@media (max-width: 768px) {
    .component {
        padding: 12px;
    }
}
```

## 四、样式变量

- 使用 Less 变量定义颜色和尺寸
- 变量定义在 `src/style/variables.less`

```less
@import '@/style/variables.less';

.component {
    color: @primary-color;
    font-size: @font-size-base;
}
```
