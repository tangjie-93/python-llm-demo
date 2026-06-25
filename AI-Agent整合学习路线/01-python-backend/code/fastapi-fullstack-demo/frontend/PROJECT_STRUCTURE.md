# FastAPI Frontend 项目结构与功能梳理

本文档梳理 `frontend/src` 的目录结构、前端分层职责、页面功能、状态管理和与后端 API 的交互方式。

## 项目概览

这是一个基于 Vue 3 的后台管理前端项目，使用 Vite 构建，Element Plus 作为 UI 组件库，Pinia 管理状态，Vue Router 管理路由，Axios 封装后端请求。

当前已实现：

- 登录页
- 注册页
- 登录态路由守卫
- Access Token 本地存储
- Refresh Token 自动刷新流程
- 后台管理布局
- 顶部导航栏
- 左侧菜单
- 面包屑
- 用户下拉菜单与退出登录
- 首页
- 用户管理
- 物品管理
- 博客文章管理
- 标签管理
- 公共表格组件
- 公共表单弹窗组件
- 公共筛选表单组件
- Axios 请求/响应拦截器

## 技术栈

| 类型 | 技术 |
| --- | --- |
| 框架 | Vue 3 |
| 构建工具 | Vite |
| 语言 | TypeScript |
| UI 组件库 | Element Plus |
| 状态管理 | Pinia |
| 路由 | Vue Router |
| HTTP 请求 | Axios |
| 样式 | Less、CSS |
| 图标 | `@element-plus/icons-vue` |

## 目录结构

```text
frontend/src/
  App.vue
  main.ts
  vite-env.d.ts
  router/
    index.ts
  utils/
    api.ts
  stores/
    auth.ts
    user.ts
    item.ts
    post.ts
  types/
    auth.ts
    post.ts
  components/
    common/
      BaseTable.vue
      BaseFormDialog.vue
      BaseFilterForm.vue
      index.ts
  layout/
    index.vue
    components/
      AppHeader.vue
      AppSidebar.vue
      Breadcrumb.vue
      UserInfo.vue
  views/
    auth/
      index.vue
      register.vue
    home/
      index.vue
    users/
      index.vue
    items/
      index.vue
    posts/
      index.vue
      components/
        postDetailDialog.vue
    tags/
      index.vue
  styles/
    animations.css
    index.less
```

## 分层职责

| 层级 | 目录 / 文件 | 职责 |
| --- | --- | --- |
| 应用入口 | `main.ts` | 创建 Vue 应用，注册 Pinia、Router、Element Plus 和图标 |
| 根组件 | `App.vue` | 提供 Element Plus 配置容器和根级 `router-view` |
| 路由层 | `router/index.ts` | 定义页面路由、嵌套路由和登录态守卫 |
| API 层 | `utils/api.ts` | Axios 实例、请求拦截、响应解包、401 自动刷新 |
| 状态层 | `stores/` | Pinia stores，封装认证、用户、物品、文章和标签状态 |
| 类型层 | `types/` | TypeScript 接口类型 |
| 公共组件 | `components/common/` | 表格、弹窗表单、筛选表单等复用组件 |
| 布局层 | `layout/` | 后台管理系统整体框架、顶部栏、侧边栏、面包屑 |
| 页面层 | `views/` | 登录、注册、首页、用户、物品、文章、标签页面 |
| 样式层 | `styles/` | 全局样式和动画 |

## 构建与开发配置

文件：`package.json`

脚本：

```text
pnpm dev      启动 Vite 开发服务
pnpm build    TypeScript 类型检查并构建生产包
pnpm preview  预览构建结果
pnpm lint     ESLint 修复
pnpm format   Prettier 格式化
```

文件：`vite.config.ts`

关键配置：

```text
dev server port: 5173
alias @ -> /src
/api proxy -> http://localhost:8000
```

前端请求 `/api/...` 时，开发环境会通过 Vite proxy 转发到后端 `http://localhost:8000`。

## 应用入口

文件：`src/main.ts`

启动流程：

1. 创建 Vue 应用。
2. 创建 Pinia 实例。
3. 全局注册 Element Plus 图标。
4. 注册 Pinia。
5. 注册 Vue Router。
6. 注册 Element Plus。
7. 挂载到 `#app`。

文件：`src/App.vue`

职责：

- 使用 `el-config-provider` 包裹应用。
- 渲染根级 `router-view`。
- 根据路由 path 设置组件 key，确保路由切换时组件刷新。

## 路由结构

文件：`src/router/index.ts`

路由：

```text
/           redirect -> /login
/login      登录页
/register   注册页

/home       首页，需要登录
/users      用户管理，需要登录
/items      物品管理，需要登录
/posts      博客文章，需要登录
/tags       标签管理，需要登录
```

认证路由统一挂在 `layout/index.vue` 下。

路由守卫逻辑：

1. 如果本地有 token 但没有用户信息，尝试调用 `/auth/me` 获取用户信息。
2. 如果获取用户信息失败，尝试调用 refresh token。
3. 如果目标路由需要登录但没有 token，跳转 `/login`。
4. 否则正常放行。

## API 请求封装

文件：`src/utils/api.ts`

Axios 基础配置：

```text
baseURL: /api
timeout: 10000
```

请求拦截器：

- 从 `authStore.token` 读取 access token。
- 如果 token 存在，则写入请求头：

```text
Authorization: Bearer <token>
```

响应拦截器：

- 后端统一响应格式为：

```json
{
  "success": true,
  "message": "操作成功",
  "data": {}
}
```

- 如果 `success=false`，抛出错误。
- 如果成功，直接返回 `response.data.data`，页面和 store 不需要再手动解包。

401 处理：

- 登录接口的 401 直接返回给组件处理。
- 非登录接口遇到 401 时：
  1. 如果正在刷新 token，请求进入队列。
  2. 如果没有刷新中的请求，调用 `authStore.refreshTokenFunc()`。
  3. 刷新成功后重放队列请求和当前请求。
  4. 刷新失败则提示登录过期并跳转 `/login`。

## 状态管理

### 认证 Store

文件：`src/stores/auth.ts`

状态：

```text
token
userInfo
isLoggedIn
```

动作：

```text
login
register
fetchUserInfo
refreshTokenFunc
logout
```

实现细节：

- Access Token 存在 `localStorage` 的 `access_token`。
- Refresh Token 不存前端，由后端通过 HttpOnly Cookie 管理。
- 登录成功后会立即调用 `/auth/me` 获取当前用户信息。
- 登出时清空本地 token，并调用 `/auth/logout` 尝试清理后端 Cookie。

### 用户 Store

文件：`src/stores/user.ts`

状态：

```text
users
currentUser
loading
```

动作：

```text
fetchUsers
getUser
createUser
updateUser
deleteUser
```

对应后端：

```text
/api/users/
```

### 物品 Store

文件：`src/stores/item.ts`

状态：

```text
items
currentItem
loading
```

动作：

```text
fetchItems
getItem
createItem
updateItem
deleteItem
```

对应后端：

```text
/api/items/
```

### 文章与标签 Store

文件：`src/stores/post.ts`

状态：

```text
posts
currentPost
tags
currentTag
loading
total
```

计算属性：

```text
publishedPosts
draftPosts
```

文章动作：

```text
fetchPosts
fetchPost
createPost
updatePost
deletePost
publishPost
unpublishPost
```

标签动作：

```text
fetchTags
fetchTag
createTag
updateTag
deleteTag
```

文章标签动作：

```text
addTagToPost
removeTagFromPost
```

对应后端：

```text
/api/posts/
/api/posts/tags/
/api/posts/{post_id}/tags/{tag_id}
```

## 布局系统

### 主布局

文件：`src/layout/index.vue`

职责：

- 页面整体采用上下结构。
- 顶部是 `AppHeader`。
- 主体区域左侧是 `AppSidebar`，右侧是页面内容。
- 子页面通过嵌套 `router-view` 渲染。
- 页面切换使用过渡动画。

### 顶部栏

文件：`src/layout/components/AppHeader.vue`

功能：

- 显示系统标题 `FastAPI Demo`。
- 显示面包屑。
- 显示用户信息区域。

### 侧边栏

文件：`src/layout/components/AppSidebar.vue`

菜单：

```text
首页        /home
用户管理    /users
项目管理    /items
博客文章    /posts
标签管理    /tags
```

### 面包屑

文件：`src/layout/components/Breadcrumb.vue`

功能：

- 根据当前路由生成面包屑。
- 支持点击非最后一级跳转。
- 路由名称映射为中文标题。

### 用户信息

文件：`src/layout/components/UserInfo.vue`

功能：

- 显示当前用户名。
- 用户下拉菜单。
- 退出登录并跳转登录页。

## 公共组件

### BaseTable

文件：`src/components/common/BaseTable.vue`

封装 Element Plus `el-table`。

支持：

- `data`
- `loading`
- `stripe`
- `border`
- `height`
- `maxHeight`
- slot 自定义列

### BaseFormDialog

文件：`src/components/common/BaseFormDialog.vue`

封装表单弹窗。

支持：

- `v-model`
- 标题
- 宽度
- 表单数据
- 表单校验规则
- 提交 loading
- 自定义 slot 表单内容
- 提交前自动调用 Element Plus 表单校验

事件：

```text
submit
cancel
update:modelValue
```

### BaseFilterForm

文件：`src/components/common/BaseFilterForm.vue`

封装内联筛选表单。

支持：

- 自定义筛选项 slot
- 筛选按钮
- 重置按钮
- `filter` 事件
- `reset` 事件

## 页面功能

### 登录页

文件：`src/views/auth/index.vue`

功能：

- 用户名输入
- 密码输入
- 表单校验
- 用户名格式校验：4-32 位字母、数字或下划线
- 密码强度校验：至少 8 位，包含小写字母、大写字母和数字
- 调用 `authStore.login`
- 登录成功后跳转 `/home`
- 根据后端错误展示账户锁定、剩余尝试次数等提示
- 跳转注册页

### 注册页

文件：`src/views/auth/register.vue`

功能：

- 用户名输入
- 邮箱输入
- 密码输入
- 确认密码
- 密码强度条
- 密码规则实时提示
- 表单校验
- 调用 `authStore.register`
- 注册成功后跳转 `/login`

### 首页

文件：`src/views/home/index.vue`

功能：

- 展示欢迎语。
- 展示当前用户名。
- 展示用户数量和项目数量统计。

注意：当前用户数量和项目数量是前端模拟值：

```text
userCount = 10
itemCount = 20
```

### 用户管理页

文件：`src/views/users/index.vue`

功能：

- 用户列表表格
- 新增用户
- 编辑用户
- 删除用户
- 刷新列表
- 用户状态标签
- 复用 `BaseTable`
- 复用 `BaseFormDialog`

字段：

```text
id
username
email
full_name
is_active
```

### 物品管理页

文件：`src/views/items/index.vue`

功能：

- 物品列表表格
- 新增物品
- 编辑物品
- 删除物品
- 刷新列表
- 显示价格、税费、所有者
- 新建物品时使用当前登录用户 ID 作为 `owner_id`
- 复用 `BaseTable`
- 复用 `BaseFormDialog`

字段：

```text
id
title
description
price
tax
owner
```

### 博客文章管理页

文件：`src/views/posts/index.vue`

功能：

- 文章列表表格
- 按发布状态筛选
- 按标签筛选
- 写文章
- 编辑文章
- 删除文章
- 发布文章
- 取消发布
- 查看文章详情
- 文章详情弹窗
- 选择多个标签
- 分页组件
- 复用 `BaseFilterForm`
- 复用 `BaseTable`
- 复用 `BaseFormDialog`

字段：

```text
title
is_published
view_count
author_id
created_at
```

创建文章时：

- 使用当前用户 ID 作为 `author_id`。
- 如果当前用户信息缺失，fallback 为 `1`。

### 文章详情弹窗

文件：`src/views/posts/components/postDetailDialog.vue`

功能：

- 展示文章标题
- 展示发布状态
- 展示阅读数
- 展示创建时间
- 展示作者
- 展示标签
- 展示文章正文

### 标签管理页

文件：`src/views/tags/index.vue`

功能：

- 标签卡片列表
- 新建标签
- 编辑标签
- 删除标签
- 查看标签详情
- 展示标签关联文章
- 标签详情弹窗

字段：

```text
id
name
description
created_at
posts
```

## 类型定义

### 认证类型

文件：`src/types/auth.ts`

主要类型：

```text
BaseResponse<T>
LoginResponse
ApiError
```

### 文章与标签类型

文件：`src/types/post.ts`

主要类型：

```text
Post
PostAuthor
PostSimple
Tag
TagWithPosts
CreatePostData
UpdatePostData
CreateTagData
UpdateTagData
PostFilterParams
PaginationParams
```

## 前后端交互关系

```text
页面组件
  -> Pinia Store
    -> utils/api.ts
      -> Axios /api/*
        -> Vite proxy
          -> FastAPI backend http://localhost:8000
```

典型请求流程：

1. 页面调用 store action。
2. store action 调用 `api.get/post/put/patch/delete`。
3. Axios 请求拦截器自动加 Authorization header。
4. 后端返回统一响应。
5. Axios 响应拦截器解包 `data`。
6. store 更新状态。
7. 页面响应式刷新。

## 当前看到的实现风险

### 1. 前端分页总数没有真实接入

文章页有分页组件，维护了：

```text
pagination.total
```

但 `postStore.fetchPosts()` 只接收后端返回的数组，没有设置 total。当前分页 UI 的总数可能不准确。

### 2. 创建文章 fallback authorId 为 1

文章创建时：

```ts
const authorId = authStore.userInfo?.id || 1;
```

如果当前用户信息缺失，会使用 `1` 作为作者 ID。真实项目中更适合强制依赖当前登录用户，或者由后端从 JWT 中识别作者。

### 3. Access Token 存在 localStorage

当前 access token 存在 `localStorage`。实现简单，但存在 XSS 风险。项目已经把 refresh token 放在 HttpOnly Cookie 中，这是更安全的方向。

### 4. 错误处理格式不完全统一

部分页面读取错误时使用：

```ts
error.response?.data?.detail
```

但 `utils/api.ts` 响应拦截器通常已经把错误转换成字符串或 Error。不同页面对错误结构的假设不完全一致。

### 5. 首页统计是模拟数据

首页的用户数量和项目数量当前是固定值：

```text
用户数量 10
项目数量 20
```

还没有接入真实统计接口。

### 6. 用户管理和物品管理缺少筛选/分页

用户页和物品页当前是基础 CRUD 表格。对于数据量较大场景，还需要后端分页、搜索和筛选。

## 总体评价

这个前端项目是一个结构清晰的 Vue 3 后台管理系统样例，已经覆盖从认证、路由守卫、状态管理、API 封装到 CRUD 页面和文章标签管理的完整链路。

它比较适合作为 FastAPI 后端的配套管理端，当前重点不是复杂业务，而是展示一个完整的前后端联调结构：

- 登录注册
- Token 认证
- API 自动鉴权
- 401 自动刷新
- 用户管理
- 物品管理
- 博客文章管理
- 标签管理
- 可复用后台页面组件

如果继续演进，建议优先处理：

1. 接入真实分页 total。
2. 创建文章时去掉 `authorId = 1` fallback。
3. 统一错误处理格式。
4. 首页统计改为真实接口。
5. 给用户和物品列表补筛选、搜索和分页。
6. 评估 access token 的存储策略。
