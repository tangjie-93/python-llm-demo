# HttpOnly Cookie 存储 Refresh Token 实施报告

## 问题发现

在代码审查中发现，之前的实现**违反了 security-standards 规范**：

### ❌ 之前的实现（错误）
```typescript
// frontend/src/stores/auth.ts
const refreshToken = ref<string | null>(null);

async function login() {
  token.value = data.access_token;
  refreshToken.value = data.refresh_token; // ❌ 存储在内存中
}
```

**问题**：
- Refresh Token 存储在 Pinia store（内存）中
- 虽然不在 localStorage，但仍可被 JavaScript 访问
- 存在 XSS 攻击风险

### ✅ 规范要求
根据 [`security-standards`](file:///Users/james/Desktop/LLM/code/python-llm-demo/.trae/skills/security-standards/SKILL.md)：

> ### Token 存储规范
> - **Access Token**: 存储在 Pinia store 中（内存）
> - **Refresh Token**: 必须使用 HttpOnly Cookie 存储
> - **禁止**: 在 localStorage 直接存储 token 原始值

---

## 实施方案

### 后端实现

#### 1. 登录接口设置 HttpOnly Cookie

```python
@router.post("/login")
async def login(...):
    # ... 验证逻辑 ...
    
    # 创建响应
    response = Response(content=success_response(...)["detail"])
    
    # 设置 HttpOnly Cookie 存储 refresh token
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,      # ✅ JavaScript 无法访问
        samesite="lax",     # ✅ 防止 CSRF 攻击
        secure=False,       # 开发环境 HTTP，生产环境改为 True
        max_age=604800,     # 7 天（秒）
        path="/api/auth/refresh"  # ✅ 只在 refresh 接口发送
    )
    
    return response
```

**安全特性**：
- ✅ `httponly=True`：防止 XSS 攻击，JavaScript 无法读取
- ✅ `samesite="lax"`：防止 CSRF 攻击
- ✅ `secure=False`：开发环境兼容 HTTP（生产环境应改为 True）
- ✅ `path="/api/auth/refresh"`：限制 Cookie 发送范围

#### 2. Refresh 接口从 Cookie 读取

```python
@router.post("/refresh")
async def refresh_access_token(request: Request, ...):
    # ✅ 从 HttpOnly Cookie 读取 refresh token
    refresh_token = request.cookies.get("refresh_token")
    
    if not refresh_token:
        raise HTTPException(401, "未找到刷新令牌")
    
    # ... 验证和刷新逻辑 ...
    
    # 更新 Cookie
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=604800,
        path="/api/auth/refresh"
    )
    
    return response
```

#### 3. 登出接口清除 Cookie

```python
@router.post("/logout")
async def logout(...):
    # 清除数据库中的 refresh token
    current_user.refresh_token = None
    session.commit()
    
    # 创建响应并清除 Cookie
    response = Response(content=success_response(...)["detail"])
    
    # ✅ 删除 refresh_token Cookie
    response.delete_cookie(
        key="refresh_token",
        path="/api/auth/refresh"
    )
    
    return response
```

---

### 前端实现

#### 1. 移除 Refresh Token 存储

```typescript
// frontend/src/stores/auth.ts
export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(null);  // ✅ Access Token 仍在内存
  // ❌ 删除：const refreshToken = ref<string | null>(null);
  
  async function login(username: string, password: string) {
    const data = await api.post('/auth/login', formData);
    
    token.value = data.access_token;
    // ✅ Refresh Token 现在在 HttpOnly Cookie 中，不需要存储
    
    await fetchUserInfo();
  }
  
  async function refreshTokenFunc() {
    // ✅ 后端会自动从 Cookie 读取 refresh token
    const data = await api.post('/auth/refresh', {});
    token.value = data.access_token;
    return true;
  }
  
  function logout() {
    token.value = null;
    userInfo.value = null;
    // ✅ 调用后端接口清除 Cookie
    api.post('/auth/logout').catch(() => {});
  }
});
```

#### 2. API 拦截器自动携带 Cookie

```typescript
// frontend/src/utils/api.ts
const axiosInstance = axios.create({
  baseURL: '/api',
  timeout: 10000,
  withCredentials: true  // ✅ 自动携带 Cookie
});
```

---

## 工作流程

### 登录流程
```
1. 用户输入用户名密码
   ↓
2. 前端发送登录请求
   ↓
3. 后端验证成功
   ↓
4. 后端返回：
   - Access Token（响应体）→ 前端存储在 Pinia
   - Refresh Token（HttpOnly Cookie）→ 浏览器自动存储
   ↓
5. 前端存储 Access Token，Refresh Token 由浏览器管理
```

### Token 刷新流程
```
1. Access Token 过期（15 分钟后）
   ↓
2. API 请求返回 401
   ↓
3. 前端拦截器检测到 401
   ↓
4. 前端调用 /auth/refresh（不传参数）
   ↓
5. 浏览器自动发送 HttpOnly Cookie
   ↓
6. 后端从 Cookie 读取 Refresh Token
   ↓
7. 验证成功，返回新的 Access Token
   ↓
8. 后端更新 Cookie 中的 Refresh Token
   ↓
9. 前端重试原请求
```

### 登出流程
```
1. 用户点击登出
   ↓
2. 前端调用 /auth/logout
   ↓
3. 后端清除数据库中的 Refresh Token
   ↓
4. 后端删除 HttpOnly Cookie
   ↓
5. 前端清除 Access Token
   ↓
6. 跳转登录页
```

---

## 安全性对比

| 存储方式 | 之前（内存） | 现在（HttpOnly Cookie） |
|----------|-------------|------------------------|
| XSS 攻击 | ⚠️ 可被读取 | ✅ 无法读取 |
| CSRF 攻击 | ⚠️ 无防护 | ✅ SameSite 防护 |
| 自动过期 | ❌ 需手动清除 | ✅ 浏览器自动管理 |
| 跨域发送 | ❌ 需手动附加 | ✅ 浏览器自动处理 |
| 符合规范 | ❌ 不符合 | ✅ 完全符合 |

---

## 修改文件清单

### 后端文件
1. [`backend/app/routers/auth.py`](file:///Users/james/Desktop/LLM/code/python-llm-demo/FastAPI/backend/app/routers/auth.py)
   - 登录接口：添加 `set_cookie()` 设置 HttpOnly Cookie
   - Refresh 接口：从 `request.cookies` 读取，添加 `set_cookie()` 更新
   - 登出接口：添加 `delete_cookie()` 清除 Cookie
   - 导入 `Request` 依赖

### 前端文件
1. [`frontend/src/stores/auth.ts`](file:///Users/james/Desktop/LLM/code/python-llm-demo/FastAPI/frontend/src/stores/auth.ts)
   - 移除 `refreshToken` 状态
   - 更新 `login()` 不再存储 refresh token
   - 更新 `refreshTokenFunc()` 从 Cookie 读取
   - 更新 `logout()` 调用后端清除 Cookie

---

## 生产环境配置建议

### Cookie 安全配置
```python
response.set_cookie(
    key="refresh_token",
    value=refresh_token,
    httponly=True,      # ✅ 必须
    samesite="strict",  # ✅ 生产环境使用 strict
    secure=True,        # ✅ 必须（HTTPS）
    max_age=604800,     # 7 天
    path="/api/auth/refresh",
    domain="yourdomain.com"  # 生产环境指定域名
)
```

### CORS 配置
```python
# backend/app/middleware/__init__.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,  # ✅ 必须，允许携带 Cookie
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 测试建议

### 功能测试
1. **登录测试**
   - 检查响应是否设置 Cookie
   - 检查 Cookie 属性（HttpOnly, SameSite）
   - 检查 Access Token 是否正确返回

2. **刷新测试**
   - 等待 Access Token 过期
   - 验证自动刷新是否触发
   - 检查 Cookie 是否自动发送

3. **登出测试**
   - 验证 Cookie 是否被删除
   - 验证数据库 refresh token 是否清除

### 安全测试
1. **XSS 测试**
   ```javascript
   // 尝试读取 Cookie（应该返回空）
   document.cookie  // 不应该包含 refresh_token
   ```

2. **CSRF 测试**
   - 尝试从其他域名发起请求
   - 验证 SameSite 是否生效

---

## 总结

本次修复确保了项目**完全符合 security-standards 规范**：

✅ **Access Token**：存储在 Pinia store（内存）  
✅ **Refresh Token**：存储在 HttpOnly Cookie  
✅ **XSS 防护**：JavaScript 无法访问 Refresh Token  
✅ **CSRF 防护**：使用 SameSite=lax 属性  
✅ **自动管理**：浏览器自动处理 Cookie 过期  

项目现在拥有企业级的 Token 安全管理机制！🎉
