# uv 包管理迁移指南

## 为什么从 Poetry 迁移到 uv

| 对比 | Poetry | uv |
|------|--------|-----|
| 速度 | 中等 (Python) | 极快 (Rust) |
| 依赖解析 | 较慢，可能卡住 | 快 |
| pip 兼容 | 否 | 是 |
| 内置 Python 版本管理 | 否 | 是 |
| 学习成本 | 中 | 低 |

## 迁移步骤

### 1. 安装 uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或使用 pip
pip install uv
```

### 2. 初始化 uv 项目

```bash
cd backend
uv init --no-readme
```

### 3. 同步依赖

```bash
# 使用本目录下的 pyproject.toml 替换 backend 下的
cp uv-setup/pyproject.toml pyproject.toml
uv sync
```

### 4. 运行项目

```bash
# 直接运行
uv run uvicorn app.main:app --reload

# 或激活虚拟环境后运行
source .venv/bin/activate
uvicorn app.main:app --reload
```

### 5. 运行测试

```bash
uv run pytest tests/ -v
```

### 常用 uv 命令速查

| 命令 | 说明 |
|------|------|
| `uv sync` | 安装/同步依赖 |
| `uv add <包名>` | 添加生产依赖 |
| `uv add --dev <包名>` | 添加开发依赖 |
| `uv remove <包名>` | 移除依赖 |
| `uv run <命令>` | 在虚拟环境中运行命令 |
| `uv lock` | 更新锁文件 |
| `uv tree` | 查看依赖树 |
| `uv python list` | 列出已安装的 Python 版本 |
| `uv python install 3.12` | 安装指定 Python 版本 |

### 前端类比

| uv | npm / pnpm | 说明 |
|----|------------|------|
| `uv init` | `npm init` | 初始化项目 |
| `uv add` | `npm install` / `pnpm add` | 安装依赖 |
| `uv sync` | `npm ci` / `pnpm install` | 按 lock 文件同步 |
| `uv run` | `npx` | 运行命令 |
| `uv.lock` | `package-lock.json` | 锁文件 |
| `.venv/` | `node_modules/` | 依赖目录 |
| `uv python install` | `nvm install` | 版本管理 |
