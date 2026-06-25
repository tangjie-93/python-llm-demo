# FastAPI Frontend Project

Vue3 + TypeScript 前端项目，使用 Pinia 状态管理和 Vue Router 路由。

## 技术栈

- **Vue 3** - 渐进式前端框架
- **TypeScript** - JavaScript 超集
- **Pinia** - 状态管理
- **Vue Router** - 路由管理
- **Element Plus** - UI 组件库
- **Axios** - HTTP 客户端
- **Vite** - 构建工具

## 项目结构

```
frontend/
├── src/
│   ├── main.ts              # 入口文件
│   ├── App.vue              # 根组件
│   ├── router/              # 路由配置
│   │   └── index.ts
│   ├── stores/              # Pinia 状态管理
│   │   ├── auth.ts          # 认证状态
│   │   ├── user.ts          # 用户状态
│   │   └── item.ts          # 物品状态
│   ├── views/               # 页面组件
│   │   ├── Login.vue        # 登录页
│   │   ├── Register.vue     # 注册页
│   │   ├── Home.vue         # 首页
│   │   ├── Users.vue        # 用户管理
│   │   └── Items.vue        # 物品管理
│   └── vite-env.d.ts        # Vite 类型定义
├── index.html
├── vite.config.ts           # Vite 配置
├── tsconfig.json            # TypeScript 配置
└── package.json
```

## 快速开始

### 安装依赖

```bash
cd frontend
npm install
```

### 启动开发服务器

```bash
npm run dev
```

### 构建生产版本

```bash
npm run build
```

### 代码检查

```bash
npm run lint
```

## 主要功能

- [x] 用户登录/注册
- [x] JWT 认证
- [x] 用户管理 CRUD
- [x] 物品管理 CRUD
- [x] 响应式布局
- [x] 状态管理
- [x] API 代理配置

## API 代理

开发环境下，Vite 会将 `/api` 请求代理到 `http://localhost:8000`。
