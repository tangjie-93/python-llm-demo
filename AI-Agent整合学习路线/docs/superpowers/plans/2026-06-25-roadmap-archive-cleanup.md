# Roadmap Archive Cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Clean `00-roadmap/docs/archive` so archived materials are grouped and named clearly without deleting historical content.

**Architecture:** Keep the archive root as an index and two grouped subdirectories. Preserve source-map content at the archive root because it is useful for traceability.

**Tech Stack:** Markdown files and filesystem moves.

---

### Task 1: Restructure archive files

**Files:**
- Create: `00-roadmap/docs/archive/README.md`
- Create: `00-roadmap/docs/archive/legacy/`
- Create: `00-roadmap/docs/archive/detailed-version/`
- Move/Rename: files currently in `00-roadmap/docs/archive/`

- [ ] **Step 1: Create grouping directories**

Run: `mkdir -p 00-roadmap/docs/archive/legacy 00-roadmap/docs/archive/detailed-version`

- [ ] **Step 2: Rename source map**

Move `00-roadmap/docs/archive/99-来源映射.md` to `00-roadmap/docs/archive/source-map.md`.

- [ ] **Step 3: Move legacy files**

Move:
- `AI-Agent原README.md` to `legacy/ai-agent-original-readme.md`
- `阶段学习包说明.md` to `legacy/phase-package-notes.md`

- [ ] **Step 4: Move detailed-version files**

Move:
- `细化版README.md` to `detailed-version/README.md`
- `细化版-00-总览与学习节奏.md` to `detailed-version/00-overview-and-study-rhythm.md`
- `细化版-08-学习资源索引.md` to `detailed-version/08-learning-resources.md`
- `细化版-09-术语表.md` to `detailed-version/09-glossary.md`

- [ ] **Step 5: Add archive README**

Create `00-roadmap/docs/archive/README.md` with links to `source-map.md`, `legacy/`, and `detailed-version/`.

- [ ] **Step 6: Verify**

Run:
- `find 00-roadmap/docs/archive -maxdepth 1 -mindepth 1 -print | sort`
- `find 00-roadmap/docs/archive -type f -name '*.md' -print | sort`

Expected:
- Archive root contains only `README.md`, `source-map.md`, `legacy`, and `detailed-version`.
- Total Markdown files under archive remains 8 after adding the new archive README.
