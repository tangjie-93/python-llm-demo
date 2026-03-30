---
name: "git-commit-standards"
description: "强制执行Git提交信息格式、分支命名和代码审查规范。当提交代码、创建分支或进行代码审查时触发此技能。"
trigger:
  - "git commit"
  - "git branch"
  - "git push"
  - "git pull"
  - "代码提交"
  - "分支命名"
  - "提交规范"
  - "代码审查"
  - ".gitignore"
  - "git config"
---

# Git提交规范

## 一、Commit Message 格式规范

### 1.1 基本格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 1.2 Type 类型

| 类型 | 说明 |
|------|------|
| feat | 新功能（feature） |
| fix | 修复 bug |
| docs | 文档变更 |
| style | 代码格式（不影响代码运行的变动） |
| refactor | 重构（既不是新增功能，也不是修改bug的代码变动） |
| perf | 性能优化 |
| test | 增加测试 |
| chore | 构建过程或辅助工具的变动 |
| revert | 回退某个提交 |

### 1.3 Scope 范围

- 可选，表示影响的范围
- 例如：`user`, `order`, `api`, `component`
- 如果没有特定范围，可以省略

### 1.4 Subject 主题

- 简短描述，不超过 50 个字符
- 使用动词开头：`add`, `fix`, `update`, `remove`
- 使用现在时：`change` 而不是 `changed` 或 `changes`
- 首字母小写
- 结尾不加句号

### 1.5 Body 正文

- 详细描述本次提交
- 说明为什么做这个修改
- 可以分成多行
- 每行不超过 72 个字符

### 1.6 Footer 页脚

- 关联 Issue：`Closes #123`
- 破坏性变更：`BREAKING CHANGE: xxx`
- 引用其他 Commit：`See also: abc123`

### 1.7 完整示例

```
feat(user): add user profile page

- Add user profile component
- Implement profile editing functionality
- Add validation for profile fields

Closes #456
```

```
fix(auth): resolve login token expiration issue

- Update token refresh logic
- Add proper error handling for expired tokens
- Improve login state management

BREAKING CHANGE: Token refresh endpoint URL changed
```

## 二、分支命名规范

### 2.1 分支类型前缀

| 前缀 | 说明 | 示例 |
|------|------|------|
| feature/ | 功能分支 | `feature/user-profile` |
| bugfix/ | 修复分支 | `bugfix/login-error` |
| hotfix/ | 紧急修复 | `hotfix/critical-bug` |
| release/ | 发布分支 | `release/v1.0.0` |
| refactor/ | 重构分支 | `refactor/api-layer` |
| docs/ | 文档分支 | `docs/update-readme` |
| test/ | 测试分支 | `test/add-e2e-tests` |
| chore/ | 杂项分支 | `chore/update-deps` |

### 2.2 分支命名规则

- 使用小写字母和连字符
- 使用有意义的描述性名称
- 避免使用特殊字符
- 避免使用数字开头

### 2.3 分支命名示例

```bash
# 好
feature/user-profile-page
bugfix/login-token-expiration
hotfix/critical-database-issue

# 不好
feature/userProfilePage
bugfix/LoginTokenExpiration
hotfix/fix123
```

## 三、分支工作流

### 3.1 Git Flow 工作流

```
main (生产环境)
  └── develop (开发环境)
        ├── feature/user-profile (功能分支)
        ├── feature/payment-gateway
        └── release/v1.0.0 (发布分支)
              └── hotfix/critical-bug (紧急修复)
```

### 3.2 创建功能分支

```bash
# 从 develop 分支创建功能分支
git checkout develop
git pull origin develop
git checkout -b feature/user-profile

# 开发完成后合并回 develop
git checkout develop
git merge --no-ff feature/user-profile
git push origin develop

# 删除本地和远程功能分支
git branch -d feature/user-profile
git push origin --delete feature/user-profile
```

### 3.3 创建修复分支

```bash
# 从 develop 分支创建修复分支
git checkout develop
git pull origin develop
git checkout -b bugfix/login-error

# 修复完成后合并回 develop
git checkout develop
git merge --no-ff bugfix/login-error
git push origin develop
```

### 3.4 创建紧急修复分支

```bash
# 从 main 分支创建紧急修复分支
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug

# 修复完成后合并到 main 和 develop
git checkout main
git merge --no-ff hotfix/critical-bug
git tag -a v1.0.1 -m "Hotfix v1.0.1"

git checkout develop
git merge --no-ff hotfix/critical-bug

git push origin main develop --tags
```

## 四、Commit 最佳实践

### 4.1 原子提交

```bash
# 不好：一次提交包含多个功能
git add .
git commit -m "update user module"

# 好：拆分多个小的提交
git add user-profile.vue
git commit -m "feat(user): add user profile component"

git add user-service.ts
git commit -m "feat(user): add user API service"

git add user-validation.ts
git commit -m "feat(user): add user validation logic"
```

### 4.2 提交前检查清单

- [ ] 代码已经过自测
- [ ] 代码已经过格式化（Prettier）
- [ ] 代码已经过 lint 检查（ESLint）
- [ ] 没有调试代码（console.log、debugger 等）
- [ ] 没有注释掉的代码
- [ ] 所有测试通过
- [ ] 提交信息符合规范
- [ ] 没有遗留的临时文件

### 4.3 提交信息示例

#### 新增功能

```
feat(auth): add Google OAuth login

- Add Google OAuth button component
- Implement OAuth callback handling
- Add user profile sync on login

Closes #123
```

#### 修复 Bug

```
fix(checkout): resolve payment timeout issue

- Increase payment request timeout from 10s to 30s
- Add retry logic for payment requests
- Improve error message display

Closes #456
```

#### 文档更新

```
docs(readme): update installation guide

- Add Docker installation instructions
- Update environment variables documentation
- Add troubleshooting section
```

#### 重构

```
refactor(api): restructure API service layer

- Split api.ts into multiple service files
- Improve error handling consistency
- Add TypeScript type definitions
```

#### 性能优化

```
perf(list): optimize large list rendering

- Implement virtual scrolling for large lists
- Add debouncing for search input
- Reduce unnecessary re-renders
```

#### 测试

```
test(user): add unit tests for user service

- Add test cases for user CRUD operations
- Add test cases for user validation
- Add test coverage report
```

## 五、代码审查检查清单

### 5.1 功能检查

- [ ] 新功能是否按需求实现？
- [ ] 边界条件是否处理？
- [ ] 错误处理是否完善？
- [ ] 用户体验是否良好？

### 5.2 代码质量检查

- [ ] 代码是否符合编码规范？
- [ ] 变量命名是否有意义？
- [ ] 函数是否单一职责？
- [ ] 是否有重复代码可以抽取？
- [ ] 是否有可以优化的代码？

### 5.3 类型安全检查

- [ ] 是否避免使用 `any` 类型？
- [ ] TypeScript 类型定义是否完整？
- [ ] 是否有类型安全检查？

### 5.4 性能检查

- [ ] 是否有不必要的重新渲染？
- [ ] 是否有内存泄漏风险？
- [ ] 大数据量是否有优化？
- [ ] API 请求是否有缓存？

### 5.5 安全检查

- [ ] 是否有 XSS 风险？
- [ ] 用户输入是否有验证？
- [ ] 敏感信息是否加密存储？
- [ ] 是否有认证授权检查？

### 5.6 测试检查

- [ ] 是否有单元测试？
- [ ] 测试覆盖率是否足够？
- [ ] 测试用例是否覆盖主要场景？
- [ ] 所有测试是否通过？

### 5.7 文档检查

- [ ] 代码注释是否清晰？
- [ ] 函数/组件是否有文档？
- [ ] API 接口是否有文档？
- [ ] README 是否更新？

## 六、Tag 命名规范

### 6.1 版本号格式

```
v<major>.<minor>.<patch>
```

- `major`：主版本号，不兼容的 API 修改
- `minor`：次版本号，向下兼容的功能性新增
- `patch`：修订号，向下兼容的问题修正

### 6.2 Tag 示例

```bash
# 创建 Tag
git tag -a v1.0.0 -m "Release v1.0.0"

# 推送 Tag
git push origin v1.0.0

# 推送所有 Tags
git push origin --tags

# 删除 Tag
git tag -d v1.0.0
git push origin --delete v1.0.0
```

## 七、Git 配置建议

### 7.1 全局配置

```bash
# 设置用户信息
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 设置默认分支名
git config --global init.defaultBranch main

# 设置默认编辑器
git config --global core.editor "vim"
```

### 7.2 项目配置

```bash
# 创建 .gitignore 文件
node_modules/
dist/
build/
.env.local
.env.*.local
.idea/
.vscode/
*.swp
*.swo

# 创建 .gitattributes 文件（处理换行符）
* text=auto
*.js text
*.ts text
*.vue text
```

### 7.3 常用 Git 别名

```bash
# 添加常用 Git 别名
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'
```

## 八、问题处理

### 8.1 撤销本地提交

```bash
# 撤销最后一次提交（保留更改）
git reset --soft HEAD~1

# 撤销最后一次提交（丢弃更改）
git reset --hard HEAD~1
```

### 8.2 修改最后一次提交

```bash
# 修改提交信息
git commit --amend

# 添加新文件到最后一次提交
git add forgotten-file
git commit --amend --no-edit
```

### 8.3 暂存当前工作

```bash
# 暂存当前工作
git stash

# 查看暂存列表
git stash list

# 应用最近的暂存
git stash pop

# 应用指定的暂存
git stash apply stash@{1}

# 删除指定的暂存
git stash drop stash@{1}
```

### 8.4 回退到某个提交

```bash
# 查看提交历史
git log --oneline --graph

# 创建新分支回退
git checkout -b revert-branch abc123

# 回退到某个提交（不保留更改）
git reset --hard abc123
```

### 8.5 处理合并冲突

```bash
# 合并时发生冲突
git merge feature-branch

# 手动编辑冲突文件后
git add conflicted-file
git commit

# 或者取消合并
git merge --abort
```

## 九、团队协作规范

### 9.1 分支保护

- `main` 分支：保护，只能通过 PR 合并
- `develop` 分支：保护，只能通过 PR 合并
- 功能分支：可以直接 push

### 9.2 Pull Request 流程

1. 创建功能分支
2. 开发并提交代码
3. 推送到远程仓库
4. 创建 Pull Request
5. 代码审查
6. 修改问题
7. 合并到目标分支
8. 删除分支

### 9.3 PR 标题和描述

**标题格式：**
```
<type>: <subject>
```

**描述模板：**
```markdown
## 描述
简要描述这个 PR 做了什么

## 相关 Issue
Closes #123

## 变更类型
- [ ] 新功能
- [ ] Bug 修复
- [ ] 文档更新
- [ ] 代码重构
- [ ] 性能优化
- [ ] 其他

## 测试
- [ ] 单元测试通过
- [ ] 手动测试完成
- [ ] 没有引入新的问题

## 截图
（如果是 UI 变更，添加截图）
```
