# Change Log 每日变更日志

自动统计 AI-Agent整合学习路线 项目的每日变更情况。

## 快速使用

```bash
cd AI-Agent整合学习路线/change-log

bash generate.sh              # 生成今天的日志
bash generate.sh 2026-06-26   # 生成指定日期
bash generate.sh -w           # 生成本周汇总
bash generate.sh -m           # 生成本月汇总
```

## 生成内容

每个日志文件包含四部分：

| 板块 | 说明 | 自动/手动 |
|------|------|----------|
| **今日工作摘要** | 实际完成的功能、关键决策、测试结果 | 手动编写 |
| **已提交变更** | 当天 commit 按类型分类 + 每次提交涉及的文件 | 自动生成 |
| **未提交变更** | `git diff --stat` 行级变更量 + 新增文件清单 | 自动生成 |
| **变更统计** | commit 数、文件数、新增/删除行数汇总 | 自动生成 |

### 自动生成示意

```markdown
### 已跟踪文件的变更（+添加行 / -删除行）

  backend/app/routers/items.py |  45 ++-
  backend/app/routers/posts.py |  38 ++-
  2 files changed, 83 insertions(+), 22 deletions(-)

### 新增未跟踪文件

  backend/tests/conftest.py
  backend/tests/test_auth.py
```

> 手动摘要部分需要人工补充。自动部分涵盖所有 git 级别的变更信息。

## 文件命名

```
change-log/
├── generate.sh          # 自动生成脚本
├── README.md            # 本说明
├── 2026-06-27.md        # 单日日志
└── 2026-06-23_to_2026-06-27.md  # 周汇总（-w 生成）
```

## git commit 规范

为了让 `generate.sh` 正确分类，commit message 建议遵循以下前缀：

| 前缀 | 分类 | 示例 |
|------|------|------|
| `feat:` | 新功能 | `feat: add BackgroundTasks router` |
| `fix:` | Bug 修复 | `fix: resolve auth refresh bug` |
| `docs:` | 文档 | `docs: update PROJECT_STRUCTURE.md` |
| `refactor:` | 重构 | `refactor: split tag models` |
| `chore:` | 工程配置 | `chore: add alembic config` |
| `test:` | 测试 | `test: add permission control tests` |
| `perf:` | 性能优化 | `perf: optimize db query` |
| `style:` | 代码风格 | `style: format code` |
