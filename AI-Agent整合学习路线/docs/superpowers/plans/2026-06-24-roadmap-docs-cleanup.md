# 路线图文档清理计划

## 目标

让 `00-roadmap/docs` 目录直观整洁，只保留一条编号主线。

## 目标根结构

- `README.md`
- `00-总览与学习节奏.md`
- `01-24周阶段学习计划.md`
- `02-核心知识点地图.md`
- `03-项目实战与作品集.md`
- `04-评测Tracing安全MCP与部署.md`
- `05-学习资源索引.md`
- `06-术语表.md`
- `archive/`

## 任务

1. 创建 `00-roadmap/docs/archive/` 目录。
2. 将非主线 Markdown 文件移入 `archive/`：
   - `99-来源映射.md`
   - `阶段学习包说明.md`
   - `细化版-00-总览与学习节奏.md`
   - `细化版-08-学习资源索引.md`
   - `细化版-09-术语表.md`
   - `细化版README.md`
   - `AI-Agent原README.md`
3. 添加 `00-roadmap/docs/README.md` 作为根入口文件。
4. 验证根目录仅包含目标结构中的文件。
5. 验证 `archive/` 中包含所有预期的历史文件。

## 备注

- 不要修改不相关的工作区变更，如 `../.obsidian/workspace.json`。
- 不要删除历史 Markdown 文件；将其归档以便追溯。
