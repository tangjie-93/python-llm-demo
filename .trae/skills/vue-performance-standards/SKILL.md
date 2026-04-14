---
name: "vue-performance-standards"
description: "提供Vue项目性能优化指南，包括构建优化、代码分割和运行时最佳实践。当优化Vue应用性能或配置构建工具时触发此技能。"
---

# 前端性能优化规范

## 一、构建优化（Vite 层面）

### 1. 代码分割与按需打包

项目已配置 `rollupOptions.manualChunks` 实现代码拆分，**更精细化的拆分示例**：

```ts
// vite.config.ts 完整配置示例
manualChunks(id) {
  // 拆分 node_modules 依赖
  if (id.includes('node_modules')) {
    const modulePath = id.toString().split('node_modules/')[1];
    const moduleName = modulePath.split('/')[0];

    // Vue 生态单独打包
    if (['vue', 'vue-router', 'pinia', '@vue'].includes(moduleName)) {
      return 'vue-vendor';
    }

    // Ant Design Vue 单独打包
    if (moduleName === 'ant-design-vue' || moduleName === '@ant-design') {
      return 'antd-vendor';
    }

    // 图表库单独打包
    if (['echarts', '@logicflow'].includes(moduleName)) {
      return 'chart-vendor';
    }

    // 工具库单独打包
    if (['lodash-es', 'dayjs', 'axios'].includes(moduleName)) {
      return 'utils-vendor';
    }

    // 其他第三方依赖打包到 vendors
    return 'vendors';
  }

  // 业务公共代码单独打包
  if (id.includes('src/components/') || id.includes('src/hooks/') || id.includes('src/utils/')) {
    return 'common';
  }
}
```

**拆分效果说明**：

- `vue-vendor.js`：包含 Vue 核心及生态库，版本稳定，缓存命中率高
- `antd-vendor.js`：包含 UI 组件库，独立更新不影响其他依赖
- `chart-vendor.js`：包含大体积图表库，按需加载不影响首屏
- `utils-vendor.js`：包含常用工具库，体积小加载快
- `common.js`：包含业务公共组件和工具，业务复用率高

**规范要求**：

- 第三方依赖按类别拆分，避免单个 chunk 体积超过 2MB
- 大体积第三方库（如 ECharts、LogicFlow 等）单独拆包，配合路由懒加载
- 页面级组件使用路由懒加载，减少首屏加载体积：

```ts
// router 配置示例
const routes = [
    {
        path: '/order',
        name: 'Order',
        component: () => import('@/views/order/index.vue'), // 懒加载
        meta: { title: '订单管理' }
    }
];
```

### 2. 构建产物优化

项目已配置的优化项：

- 生产环境关闭 `sourcemap`，减少构建产物体积
- 静态资源添加 `hash` 后缀，利用浏览器缓存：

```ts
chunkFileNames: 'js/[name]-[hash].js',
entryFileNames: 'js/[name]-[hash].js',
assetFileNames: '[ext]/[name]-[hash].[ext]',
```

**补充规范**：

- 生产环境移除 `console`、`debugger` 等调试代码：

```ts
terserOptions: {
  compress: {
    drop_console: true,
    drop_debugger: true,
  },
}
```

- 控制 chunk 大小警告阈值，避免单个文件过大：

```ts
chunkSizeWarningLimit: 2000; // 建议调整为2MB
```

### 3. 插件优化

- 使用 `@vitejs/plugin-vue` 的 `template.compilerOptions` 优化模板编译
- 图片资源使用 `vite-plugin-imagemin` 进行压缩
- SVG 图标使用 `vite-plugin-svg-icons` 进行雪碧图优化

## 二、运行时优化

### 1. 组件优化

#### 1.1 合理使用 v-show 和 v-if

- `v-if`：条件不成立时不渲染组件，适用于切换频率低的场景
- `v-show`：始终渲染组件，通过 CSS 控制显示，适用于频繁切换的场景

```vue
<!-- 低频切换：使用 v-if -->
<Modal v-if="visible" />

<!-- 高频切换：使用 v-show -->
<TabPane v-show="activeTab === 'detail'" />
```

#### 1.2 使用 keep-alive 缓存组件

```vue
<template>
  <keep-alive :include="cachedViews">
    <component :is="currentComponent" />
  </keep-alive>
</template>
```

#### 1.3 避免不必要的组件重渲染

- 使用 `computed` 缓存计算结果
- 使用 `watch` 时指定 `deep: false`（除非必要）
- 使用 `shallowRef` 替代 `ref` 处理大型对象

#### 1.4 组件级别性能优化

- **使用 `v-once` 渲染静态内容**：对于不会变化的静态内容，使用 `v-once` 避免不必要的重渲染
- **使用 `computed` 缓存计算结果**：对于复杂的计算逻辑，使用计算属性进行缓存
- **大数据列表使用虚拟滚动**：对于大量数据的列表展示，使用虚拟滚动技术
- **懒加载非首屏组件**：对于非首屏显示的组件，使用懒加载技术

### 2. 列表优化

#### 2.1 大数据列表使用虚拟滚动

```vue
<template>
  <RecycleScroller
    class="scroller"
    :items="list"
    :item-size="50"
    key-field="id"
  >
    <template #default="{ item }">
      <div class="list-item">{{ item.name }}</div>
    </template>
  </RecycleScroller>
</template>
```

#### 2.2 列表项使用 key

```vue
<!-- 正确：使用唯一标识作为 key -->
<div v-for="item in list" :key="item.id">{{ item.name }}</div>

<!-- 错误：使用 index 作为 key（除非列表不会变化） -->
<div v-for="(item, index) in list" :key="index">{{ item.name }}</div>
```

### 3. 响应式优化

#### 3.1 避免深层响应式

```ts
// 不推荐：深层响应式影响性能
const state = reactive({
  nested: {
    deep: {
      data: { ... }
    }
  }
});

// 推荐：使用 shallowReactive 或 markRaw
const state = shallowReactive({
  nested: markRaw({
    deep: {
      data: { ... }
    }
  })
});
```

#### 3.2 大数据使用 toRaw

```ts
import { toRaw } from 'vue';

// 提交数据时使用 toRaw 避免不必要的响应式开销
const submitData = toRaw(formData);
```

### 4. 事件优化

#### 4.1 事件委托

```vue
<!-- 不推荐：每个子元素都绑定事件 -->
<div v-for="item in list" :key="item.id">
  <span @click="handleClick(item)">{{ item.name }}</span>
</div>

<!-- 推荐：使用事件委托 -->
<div @click="handleClick">
  <span v-for="item in list" :key="item.id" :data-id="item.id">
    {{ item.name }}
  </span>
</div>
```

#### 4.2 防抖和节流

```ts
import { debounce, throttle } from 'lodash-es';

// 搜索输入防抖
const handleSearch = debounce((value: string) => {
  fetchSearchResults(value);
}, 300);

// 滚动事件节流
const handleScroll = throttle(() => {
  checkScrollPosition();
}, 100);
```

## 三、网络优化

### 1. 请求优化

#### 1.1 请求合并

**方式一：使用 Promise.allSettled（推荐）**

```ts
// 使用 Promise.allSettled 合并并行请求，即使某个请求失败也不会影响其他请求
const results = await Promise.allSettled([
  fetchUserInfo(),
  fetchOrderList(),
  fetchProductList()
]);

// 处理结果
const [userResult, orderResult, productResult] = results;

// 获取成功的数据
const userInfo = userResult.status === 'fulfilled' ? userResult.value : null;
const orderList = orderResult.status === 'fulfilled' ? orderResult.value : [];
const productList = productResult.status === 'fulfilled' ? productResult.value : [];

// 处理错误
results.forEach((result, index) => {
  if (result.status === 'rejected') {
    console.error(`请求 ${index} 失败:`, result.reason);
  }
});
```

**方式二：使用 Promise.all + 错误处理包装**

```ts
// 包装请求，确保单个请求失败不影响其他请求
const safeFetch = async <T>(fetchFn: () => Promise<T>, defaultValue: T): Promise<T> => {
  try {
    return await fetchFn();
  } catch (error) {
    console.error('请求失败:', error);
    return defaultValue;
  }
};

// 并行请求，即使某个失败也能获取其他结果
const [userInfo, orderList, productList] = await Promise.all([
  safeFetch(fetchUserInfo, null),
  safeFetch(fetchOrderList, []),
  safeFetch(fetchProductList, [])
]);
```

**方式三：使用 Promise.all（需要所有请求都成功）**

```ts
// 注意：使用 Promise.all 时，如果任一请求失败，整个 Promise 会 reject
try {
  const [userInfo, orderList, productList] = await Promise.all([
    fetchUserInfo(),
    fetchOrderList(),
    fetchProductList()
  ]);
} catch (error) {
  // 任一请求失败都会进入这里
  console.error('请求失败:', error);
}
```

#### 1.2 请求缓存

项目已提供 `useRequest` Hook 实现，位于 `src/hooks/useRequest.ts`：

```ts
import { useRequest } from '@/hooks/useRequest';

// 使用 useRequest 的缓存功能
const { data, loading, error, run, refresh, cancel } = useRequest(fetchUserInfo, {
  cacheKey: 'user-info',           // 缓存键，设置后启用缓存
  staleTime: 5 * 60 * 1000,       // 缓存有效期，默认5分钟
  immediate: true,                // 是否立即执行请求，默认true
  onSuccess: (data) => {
    console.log('请求成功:', data);
  },
  onError: (error) => {
    console.error('请求失败:', error);
  }
});

// 手动执行请求
const handleFetch = () => {
  run();
};

// 刷新数据（忽略缓存）
const handleRefresh = () => {
  refresh();
};

// 取消请求
const handleCancel = () => {
  cancel();
};
```

**useRequest 功能特性：**
- ✅ 请求状态管理（loading、error、data）
- ✅ 缓存功能（cacheKey + staleTime）
- ✅ 自动请求（immediate）
- ✅ 手动执行（run）
- ✅ 刷新数据（refresh，忽略缓存）
- ✅ 取消请求（cancel）
- ✅ 成功/失败/完成回调
- ✅ TypeScript 类型支持

**清除缓存：**
```ts
import { clearRequestCache, clearAllRequestCache } from '@/hooks/useRequest';

// 清除指定缓存
clearRequestCache('user-info');

// 清除所有缓存
clearAllRequestCache();
```

#### 1.3 请求取消

```ts
import axios from 'axios';

const controller = new AbortController();

axios.get('/api/data', {
  signal: controller.signal
});

// 组件卸载时取消请求
onUnmounted(() => {
  controller.abort();
});
```

### 2. 资源优化

#### 2.1 图片懒加载

```vue
<img v-lazy="imageUrl" :alt="imageName" />
```

#### 2.2 图片格式优化

- 使用 WebP 格式替代 PNG/JPG
- 使用 SVG 替代小图标
- 使用响应式图片

```html
<picture>
  <source srcset="image.webp" type="image/webp">
  <source srcset="image.jpg" type="image/jpeg">
  <img src="image.jpg" alt="描述">
</picture>
```

## 四、渲染优化

### 1. 骨架屏

```vue
<template>
  <div v-if="loading" class="skeleton">
    <a-skeleton active :paragraph="{ rows: 6 }" />
  </div>
  <div v-else class="content">
    <!-- 真实内容 -->
  </div>
</template>
```

### 2. 渐进式加载

```vue
<template>
  <div>
    <!-- 优先加载首屏内容 -->
    <CriticalContent />

    <!-- 延迟加载非关键内容 -->
    <LazyComponent>
      <NonCriticalContent />
    </LazyComponent>
  </div>
</template>
```

### 3. SSR/SSG

- 首屏关键内容使用 SSR（服务端渲染）
- 静态页面使用 SSG（静态站点生成）
- 使用 Nuxt.js 或 Vite-SSG 实现

## 五、性能监控

### 1. 性能指标

- **FCP**（First Contentful Paint）：首次内容绘制
- **LCP**（Largest Contentful Paint）：最大内容绘制
- **FID**（First Input Delay）：首次输入延迟
- **CLS**（Cumulative Layout Shift）：累积布局偏移

### 2. 性能测试工具

- Lighthouse：Chrome 开发者工具
- WebPageTest：在线性能测试
- Vue DevTools：Vue 性能分析

### 3. 性能预算

```json
{
  "budgets": [
    {
      "type": "bundle",
      "name": "app",
      "maximumWarningSize": "500kb",
      "maximumErrorSize": "1mb"
    }
  ]
}
```
