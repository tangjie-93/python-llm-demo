# 路线图归档清理实施计划

> **面向 agentic 工作程序：** 必须使用子技能：使用 superpowers:executing-plans 按任务逐项实施本计划。步骤使用复选框（`- [ ]`）语法进行跟踪。

**目标：** 清理 `00-roadmap/docs/archive`，使归档材料分组清晰、命名规范，同时不删除历史内容。

**架构：** 保留归档根目录作为索引，并包含两个分组子目录。将来源映射内容保留在归档根目录，因为它对于追溯很有用。

**技术栈：** Markdown 文件和文件系统移动操作。

---

### 任务 1：重组归档文件

**涉及文件：**
- 创建：`00-roadmap/docs/archive/README.md`
- 创建：`00-roadmap/docs/archive/legacy/`
- 创建：`00-roadmap/docs/archive/detailed-version/`
- 移动/重命名：当前位于 `00-roadmap/docs/archive/` 中的文件

- [ ] **步骤 1：创建分组目录**

执行：`mkdir -p 00-roadmap/docs/archive/legacy 00-roadmap/docs/archive/detailed-version`

- [ ] **步骤 2：重命名来源映射**

将 `00-roadmap/docs/archive/99-来源映射.md` 移动为 `00-roadmap/docs/archive/source-map.md`。

- [ ] **步骤 3：移动旧版文件**

移动：
- `AI-Agent原README.md` → `legacy/ai-agent-original-readme.md`
- `阶段学习包说明.md` → `legacy/phase-package-notes.md`

- [ ] **步骤 4：移动细化版本文件**

移动：
- `细化版README.md` → `detailed-version/README.md`
- `细化版-00-总览与学习节奏.md` → `detailed-version/00-overview-and-study-rhythm.md`
- `细化版-08-学习资源索引.md` → `detailed-version/08-learning-resources.md`
- `细化版-09-术语表.md` → `detailed-version/09-glossary.md`

- [ ] **步骤 5：添加归档 README**

创建 `00-roadmap/docs/archive/README.md`，包含指向 `source-map.md`、`legacy/` 和 `detailed-version/` 的链接。

- [ ] **步骤 6：验证**

执行：
- `find 00-roadmap/docs/archive -maxdepth 1 -mindepth 1 -print | sort`
- `find 00-roadmap/docs/archive -type f -name '*.md' -print | sort`

预期：
- 归档根目录仅包含 `README.md`、`source-map.md`、`legacy` 和 `detailed-version`。
- 添加新归档 README 后，归档下 Markdown 文件总数仍为 8。
