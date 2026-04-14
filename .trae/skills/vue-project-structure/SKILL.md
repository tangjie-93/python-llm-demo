---
name: "vue-project-structure"
description: "定义Vue项目目录结构和组织标准。当搭建新Vue项目或重组现有项目结构时触发此技能。"
---

# 项目结构说明

## 整体目录结构

```
mon-mes/
├── .vscode/                  # VSCode 配置文件
├── docker/                   # Docker 相关配置
├── mock/                     # 全局 Mock 数据
├── public/                   # 静态资源文件
├── src/                      # 项目源代码
├── .env.development          # 开发环境配置
├── .eslintrc.cjs             # ESLint 配置
├── .gitattributes            # Git 属性配置
├── .prettierrc.json          # Prettier 代码格式化配置
├── DockerFile                # Docker 构建文件
├── README.md                 # 项目说明文档
├── env.d.ts                  # 环境变量类型定义
├── index.html                # 项目入口 HTML 文件
├── package.json              # 项目依赖和脚本配置
├── pnpm-lock.yaml            # pnpm 依赖锁定文件
├── tsconfig.json             # TypeScript 配置
├── vite.config.ts            # Vite 构建配置
└── vitest.config.ts          # Vitest 测试配置
```

## src 目录结构详解

```
src/
├── assets/                   # 静态资源目录
│   └── icons/                # SVG 图标资源
├── components/               # 公共组件目录
│   ├── GlobalHeader/         # 全局头部组件
│   ├── Menu/                 # 菜单相关组件
│   ├── MultiTab/             # 多标签页组件
│   ├── NProgress/            # 进度条组件
│   ├── SvgIcon/              # SVG 图标组件
├── config/                   # 全局配置目录
│   └── defaultSettings.ts    # 默认配置文件
├── eventBus/                 # 事件总线
├── hooks/                    # 全局自定义 Hooks
│   └── Full.ts               # 全屏操作 Hook
├── layouts/                  # 布局组件
│   ├── BasicLayout.vue       # 基础布局
│   ├── RouteView.vue         # 路由视图
│   └── UserLayout.vue        # 用户布局
├── locales/                  # 国际化配置
│   └── menu/                 # 菜单国际化
├── mock/                     # 业务模块 Mock 数据
│   └── order.ts              # 订单模块 Mock
├── router/                   # 路由配置
│   ├── basicRouter.ts        # 基础路由
│   ├── commonRoutes.ts       # 通用路由
│   ├── exceptionRouter.ts    # 异常页面路由
│   ├── generateAsyncRoutes.ts # 动态路由生成
│   ├── permission.ts         # 权限控制
│   ├── routerGuard.ts        # 路由守卫
├── service/                  # API 接口层
│   ├── user.ts               # 用户相关接口
├── store/                    # 状态管理
├── style/                    # 全局样式
│   ├── global.less           # 全局样式
│   ├── table.less            # 表格样式
├── types/                    # 全局类型定义
│   ├── user.ts               # 用户类型
├── utils/                    # 工具函数
│   ├── http/                 # HTTP 请求工具
│   │   ├── axios.ts          # Axios 封装
│   │   └── request.ts        # 请求封装
│   ├── Storage.ts            # 存储工具
│   ├── domUtil.ts            # DOM 操作工具
│   ├── encrypt.ts            # 加密工具
│   ├── formValidator.ts      # 表单验证工具
│   └── util.ts               # 通用工具函数
├── views/                    # 页面视图
│   ├── user/                 # 用户相关页面
├── App.vue                   # 根组件
├── main.ts                   # 项目入口文件
└── global.d.ts               # 全局类型定义
```

## 目录设计规范

### 1. 组件目录 (components/)

- 所有公共组件放在此目录下
- 每个组件独立成目录，包含组件自身、样式、Hooks 等
- 业务模块内的私有组件放在对应模块的 `components/` 目录下
- 接口层组件放在 `service/` 目录下，与业务模块对应。
- 组件的类型定义放在 `src/types/` 目录下，与业务模块对应。

**组件目录结构**：

```
components/
├── ComponentName/            # 组件目录（大驼峰命名）
│   ├── index.vue             # 组件入口
│   ├── hooks/                # 组件专用 Hooks
│   │   └── useComponent.ts
│   └── components/             # 组件目录（可选）
│   │   ├── SubComponent1.vue
│   │   └── SubComponent2.vue
```

### 2. 页面目录 (views/)

- 每个页面对应一个目录
- 页面私有组件放在页面内的 `components/` 目录
- 页面逻辑封装在 `hooks/` 目录下，保持组件简洁
- 页面相关的类型定义放在 `src/types/` 目录下，与业务模块对应。

**页面目录结构**：

```
views/
├── module-name/              # 模块目录（小写+连字符）
│   ├── index.vue             # 页面入口
│   ├── components/           # 页面私有组件
│   │   ├── SubComponent1.vue
│   │   └── SubComponent2.vue
│   ├── hooks/                # 页面专用 Hooks
│   │   ├── useModuleHook.ts
│   │   └── useDataFetch.ts
```

### 3. 接口层 (service/)

- 按业务模块划分接口文件
- 每个文件对应一个业务模块的 API
- 使用统一的请求封装

**接口层结构**：

```ts
// service/user.ts
import { request } from '@/utils/http/request';
import type { UserInfo, LoginParams } from '@/types/user';

export const userApi = {
    // 登录
    login: (params: LoginParams) =>
        request.post<UserInfo>('/api/user/login', params),

    // 获取用户信息
    getUserInfo: () =>
        request.get<UserInfo>('/api/user/info'),

    // 更新用户信息
    updateUserInfo: (data: Partial<UserInfo>) =>
        request.put<UserInfo>('/api/user/info', data),
};
```

### 4. 类型定义 (types/)

- 全局类型定义放在 `src/types/` 目录
- 页面/组件私有类型放在各自的 `types.ts` 文件
- 类型文件与业务模块对应

**类型定义结构**：

```ts
// types/user.ts
// 实体类型
export interface UserInfo {
    id: string;
    name: string;
    email: string;
    avatar?: string;
}

// API 参数类型
export interface LoginParams {
    username: string;
    password: string;
    captcha?: string;
}

// API 响应类型
export interface LoginResponse {
    token: string;
    userInfo: UserInfo;
}
```

### 5. 工具函数 (utils/)

- 通用工具函数放在 `src/utils/` 目录
- 按功能分类组织文件
- 复杂功能单独成目录

**工具函数结构**：

```
utils/
├── http/                     # HTTP 请求相关
│   ├── axios.ts              # Axios 实例配置
│   └── request.ts            # 请求封装
├── Storage.ts                # 本地存储封装
├── domUtil.ts                # DOM 操作工具
├── encrypt.ts                # 加密解密工具
├── formValidator.ts          # 表单验证工具
└── util.ts                   # 通用工具函数
```

### 6. 路由配置 (router/)

- 路由配置按功能拆分多个文件
- 动态路由生成逻辑单独封装
- 路由守卫集中管理

**路由配置结构**：

```
router/
├── index.ts                  # 路由入口
├── basicRouter.ts            # 基础路由（登录、404等）
├── commonRoutes.ts           # 通用业务路由
├── exceptionRouter.ts        # 异常页面路由
├── generateAsyncRoutes.ts    # 动态路由生成
├── permission.ts             # 权限控制逻辑
└── routerGuard.ts            # 路由守卫
```

### 7. 状态管理 (store/)

- 使用 Pinia 进行状态管理
- 按功能模块拆分 store
- 组合式 API 风格编写

**状态管理结构**：

```ts
// store/modules/user.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { UserInfo } from '@/types/user';

export const useUserStore = defineStore('user', () => {
    // State
    const userInfo = ref<UserInfo | null>(null);
    const token = ref<string>('');

    // Getters
    const isLoggedIn = computed(() => !!token.value);

    // Actions
    const setUserInfo = (info: UserInfo) => {
        userInfo.value = info;
    };

    const logout = () => {
        userInfo.value = null;
        token.value = '';
    };

    return {
        userInfo,
        token,
        isLoggedIn,
        setUserInfo,
        logout
    };
});
```

### 7.1 Token 状态管理规范

- token 状态必须存储在 Pinia store 中
- 禁止在 localStorage/sessionStorage 直接存储 token 原始值，应通过 store 封装
- refreshToken 必须使用 HttpOnly Cookie 存储，由后端管理

**Token Store 规范**：

```ts
// store/modules/auth.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { AuthTokens } from '@/types/auth';

export const useAuthStore = defineStore('auth', () => {
    const accessToken = ref<string>('');
    const refreshToken = ref<string>('');
    const expiresAt = ref<number>(0);

    const isLoggedIn = computed(() => !!accessToken.value);
    const isTokenExpired = computed(() => expiresAt.value > 0 && Date.now() >= expiresAt.value);

    const setTokens = (tokens: AuthTokens) => {
        accessToken.value = tokens.accessToken;
        if (tokens.refreshToken) {
            refreshToken.value = tokens.refreshToken;
        }
        if (tokens.expiresAt) {
            expiresAt.value = tokens.expiresAt;
        }
    };

    const clearTokens = () => {
        accessToken.value = '';
        refreshToken.value = '';
        expiresAt.value = 0;
    };

    return {
        accessToken,
        refreshToken,
        expiresAt,
        isLoggedIn,
        isTokenExpired,
        setTokens,
        clearTokens
    };
});
```

### 7.2 HTTP 请求 Token 附加规范

- 统一在请求拦截器中附加 Token
- 使用 `Bearer` 模式：`Authorization: Bearer <token>`
- Token 为空时不应发起需要认证的请求

**请求拦截器示例**：

```ts
// utils/http/request.ts
import axios from 'axios';
import { useAuthStore } from '@/store/modules/auth';

const request = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    timeout: 10000
});

request.interceptors.request.use((config) => {
    const authStore = useAuthStore();
    if (authStore.accessToken) {
        config.headers.Authorization = `Bearer ${authStore.accessToken}`;
    }
    return config;
});
```

### 7.3 Token 刷新规范

- 401 响应时自动触发 Token 刷新
- 使用请求队列确保刷新请求串行执行，避免多请求竞争
- 刷新失败时跳转登录页并清除本地状态

**Token 刷新流程**：

```ts
// utils/http/token.ts
import axios from 'axios';
import { useAuthStore } from '@/store/modules/auth';
import router from '@/router';

let isRefreshing = false;
let refreshSubscribers: Array<(token: string) => void> = [];

const subscribeTokenRefresh = (callback: (token: string) => void) => {
    refreshSubscribers.push(callback);
};

const onTokenRefreshed = (token: string) => {
    refreshSubscribers.forEach(callback => callback(token));
    refreshSubscribers = [];
};

export const refreshToken = async (): Promise<string> => {
    const authStore = useAuthStore();
    try {
        const response = await axios.post('/api/auth/refresh', {
            refreshToken: authStore.refreshToken
        });
        const { accessToken, expiresAt } = response.data;
        authStore.setTokens({ accessToken, expiresAt });
        onTokenRefreshed(accessToken);
        return accessToken;
    } catch (error) {
        authStore.clearTokens();
        router.push('/login');
        throw error;
    }
};

export const handleTokenError = async (error: any) => {
    if (error.response?.status !== 401) {
        throw error;
    }

    if (isRefreshing) {
        return new Promise((resolve) => {
            subscribeTokenRefresh((token: string) => {
                resolve(token);
            });
        });
    }

    isRefreshing = true;
    try {
        const token = await refreshToken();
        isRefreshing = false;
        return token;
    } catch {
        isRefreshing = false;
        throw error;
    }
};
```

### 7.4 敏感信息处理规范

- refreshToken 必须在 HttpOnly Cookie 中存储
- 禁止在 URL 参数、localStorage 明文、console.log 中暴露 token
- 调试时使用 `JSON.parse(JSON.stringify())` 脱敏后再打印

### 8. 样式文件 (style/)

- 全局样式放在 `src/style/` 目录
- 使用 Less 预处理器
- 变量和混合宏单独文件定义

**样式文件结构**：

```
style/
├── global.less               # 全局样式
├── variables.less            # Less 变量定义
├── mixins.less               # Less 混合宏
├── table.less                # 表格样式
└── animation.less            # 动画样式
```

## 文件命名规范

### 1. 目录命名

- **小写字母**：`components`, `views`, `utils`
- **连字符分隔**：`global-header`, `user-management`
- **业务模块**：复数形式，如 `orders`, `products`

### 2. 文件命名

| 文件类型 | 命名规范 | 示例 |
|---------|---------|------|
| 组件文件 | 小驼峰 | `userCard.vue`, `orderList.vue` |
| Hook 文件 | 小驼峰 + use 前缀 | `useUser.ts`, `useOrderHook.ts` |
| 工具文件 | 小驼峰 | `domUtil.ts`, `storage.ts` |
| 类型文件 | 小驼峰 | `user.ts`, `order.ts` |
| 样式文件 | 小驼峰 | `global.less`, `variables.less` |
| 配置文件 | 小驼峰 | `defaultSettings.ts` |

### 3. 特殊文件

- **入口文件**：统一使用 `index.vue`, `index.ts`
- **类型定义文件**：使用 `types.ts` 或 `[name].types.ts`
- **样式文件**：与组件同名，如 `UserCard.vue` + `UserCard.less`

## 导入路径规范

### 1. 别名配置

```ts
// tsconfig.json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["src/*"],
      "#/*": ["types/*"]
    }
  }
}
```

### 2. 导入顺序

```ts
// 1. Vue 核心库
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';

// 2. 第三方库
import { message } from 'ant-design-vue';
import { cloneDeep } from 'lodash-es';

// 3. 项目内部依赖
import { useUserStore } from '@/store/modules/user';
import { userApi } from '@/service/user';

// 4. 类型导入
import type { UserInfo } from '@/types/user';
```

## 项目初始化检查清单

创建新项目时，确保以下目录和文件已创建：

- [ ] `src/components/` - 公共组件目录
- [ ] `src/views/` - 页面视图目录
- [ ] `src/router/` - 路由配置目录
- [ ] `src/store/` - 状态管理目录
- [ ] `src/service/` - API 接口目录
- [ ] `src/types/` - 类型定义目录
- [ ] `src/utils/` - 工具函数目录
- [ ] `src/hooks/` - 全局 Hooks 目录
- [ ] `src/style/` - 全局样式目录
- [ ] `src/assets/` - 静态资源目录
- [ ] `src/config/` - 配置文件目录
- [ ] `mock/` - Mock 数据目录
