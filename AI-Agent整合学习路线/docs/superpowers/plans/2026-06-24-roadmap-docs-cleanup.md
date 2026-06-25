# Roadmap Docs Cleanup Plan

## Goal

Make `00-roadmap/docs` visually clean by keeping one numbered mainline only.

## Target root structure

- `README.md`
- `00-总览与学习节奏.md`
- `01-24周阶段学习计划.md`
- `02-核心知识点地图.md`
- `03-项目实战与作品集.md`
- `04-评测Tracing安全MCP与部署.md`
- `05-学习资源索引.md`
- `06-术语表.md`
- `archive/`

## Tasks

1. Create `00-roadmap/docs/archive/`.
2. Move non-mainline Markdown files into `archive/`:
   - `99-来源映射.md`
   - `阶段学习包说明.md`
   - `细化版-00-总览与学习节奏.md`
   - `细化版-08-学习资源索引.md`
   - `细化版-09-术语表.md`
   - `细化版README.md`
   - `AI-Agent原README.md`
3. Add `00-roadmap/docs/README.md` as the root entry point.
4. Verify the root directory contains only the target structure.
5. Verify all expected historical files exist in `archive/`.

## Notes

- Do not modify unrelated workspace changes such as `../.obsidian/workspace.json`.
- Do not delete historical Markdown files; archive them for traceability.
