# Level 2-3 | 第 7 周：项目实战 — 智能代码审查 CLI

> 🔍 **关卡名**：代码审查官 · AI CR 工具
> 📅 **时间**：第 7 周 | ⏱️ **学时**：~20h

## 本周学习目标

- [ ] 完成阶段二实战项目 `ai-code-review`
- [ ] 掌握 System Prompt 在专业场景中的设计
- [ ] 能处理 Git diff 分析和结构化输出

## 每日学习安排

### 周一（4h）· 项目设计 + System Prompt

- [ ] 设计：代码审查 CLI 的整体架构
- [ ] 设计：System Prompt 模板（安全/性能/可维护性三个维度）
- [ ] 实践：编写审查规则配置

### 周二（4h）· 文件分析核心逻辑

- [ ] 实现：文件路径 → 读取代码 → AI 分析 → 结构化报告
- [ ] 实现：问题等级分类（Critical / Warning / Info）
- [ ] 实现：修复建议生成

### 周三（4h）· Git Diff 模式

- [ ] 学习：`gitpython` 库处理 Git diff
- [ ] 实现：`ai-review diff` 子命令
- [ ] 实现：只审查变更代码，不审未修改部分

### 周四（4h）· CLI 美化 + 输出格式化

- [ ] 学习：`rich` 库美化终端输出
- [ ] 实现：Markdown 格式审查报告输出
- [ ] 实现：彩色终端输出（问题等级用不同颜色）
- [ ] 实现：报告保存到文件

### 周五（4h）· 测试 + 文档

- [ ] 编写测试：不同语言文件的审查测试
- [ ] 编写 README：安装、配置、使用说明
- [ ] 对照验收标准自检

## 知识点清单

- [ ] System Prompt 工程化设计
- [ ] 代码审查维度设计（安全/性能/可维护性/代码风格）
- [ ] `gitpython` Git 操作
- [ ] `rich` 终端美化库
- [ ] 结构化报告输出（Markdown）
- [ ] CLI 子命令设计（`check` / `diff` / `config`）

## 本周产出

- ✅ **`ai-code-review`** 完整可用的 CLI 工具
- ✅ 支持 `check`（文件审查）和 `diff`（变更审查）两种模式
- ✅ Markdown 格式审查报告
- ✅ README 文档

## 通关标志

- [ ] `ai-review check app/main.py` 可分析指定文件
- [ ] `ai-review diff` 可分析当前 Git 变更
- [ ] 输出报告包含问题等级（Critical/Warning/Info）
- [ ] 提供具体的修复建议
- [ ] 支持通过环境变量配置模型和 API 端点
- [ ] README 包含安装和使用说明

## 资源链接

| 资源 | 链接 |
|------|------|
| rich 文档 | https://rich.readthedocs.io/ |
| gitpython 文档 | https://gitpython.readthedocs.io/ |
| click 文档 | https://click.palletsprojects.com/ |

## 前端技能衔接提示

- 代码审查经验 → System Prompt 设计更精准（你比后端更懂前端代码）
- CLI 工具设计 = ESLint/Prettier 的命令行体验设计
- Git diff 分析 = PR code review 的自动化版本
