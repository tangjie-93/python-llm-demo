---
name: "security-standards"
description: "前端安全规范，包括Token管理、XSS防护、CSRF防护、输入验证等安全最佳实践。当处理敏感数据、用户认证或安全相关功能时触发此技能。"
trigger:
  - "token"
  - "security"
  - "auth"
  - "XSS"
  - "CSRF"
  - "安全"
  - "认证"
  - "授权"
  - "密码"
  - "敏感数据"
  - "HTTPS"
  - "CSP"
  - "Content-Security-Policy"
---

# 前端安全规范

## Token 管理

### Token 存储规范

- **Access Token**: 存储在 Pinia store 中（内存）
- **Refresh Token**: 必须使用 HttpOnly Cookie 存储
- **禁止**: 在 localStorage 直接存储 token 原始值
- **禁止**: 在 URL 参数、console.log 中暴露 token

### HTTP 请求安全

- 统一在请求拦截器中附加 Token
- 使用 `Bearer` 模式: `Authorization: Bearer <token>`
- 401 响应时自动触发 Token 刷新

```typescript
// 请求拦截器示例
axios.interceptors.request.use((config) => {
    const token = useUserStore().token;
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});
```

## XSS 防护

### 输入处理

- 对用户输入进行转义和过滤
- 使用框架提供的安全机制（Vue 的模板自动转义）
- 避免使用 `v-html` 渲染用户输入内容

### 输出处理

```typescript
// 使用 DOMPurify 清理 HTML
import DOMPurify from 'dompurify';

const cleanHtml = DOMPurify.sanitize(userInput);
```

## CSRF 防护

- 使用 CSRF Token 验证
- 验证请求来源（Referer/Origin）
- 使用 SameSite Cookie 属性

## 输入验证

- 前端和后端都要进行输入验证
- 使用白名单验证策略
- 对特殊字符进行转义

## 安全头部

```typescript
// 推荐的 CSP 配置
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
```

## 敏感信息处理

- 不在前端代码中硬编码敏感信息
- 不在日志中输出敏感数据
- 使用环境变量管理配置
