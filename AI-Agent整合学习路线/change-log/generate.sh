#!/bin/bash
# ============================================================
# 每日变更日志自动生成脚本
# 用法:
#   ./generate.sh                 生成今天的日志
#   ./generate.sh 2026-06-26      生成指定日期的日志
#   ./generate.sh -w              生成本周汇总
#   ./generate.sh -m              生成本月汇总
# ============================================================

set -euo pipefail

# 切换到项目根目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CHANGE_LOG_DIR="$SCRIPT_DIR"
cd "$PROJECT_ROOT"

# ---------- helper functions ----------

get_date() {
    if [ -n "${1:-}" ]; then
        echo "$1"
    else
        date +%Y-%m-%d
    fi
}

get_date_range() {
    local mode="$1"
    local today
    today=$(date +%Y-%m-%d)

    case "$mode" in
        -w)
            local weekday
            weekday=$(date +%u)
            local monday
            monday=$(date -v-$((weekday - 1))d +%Y-%m-%d 2>/dev/null || date -d "$today - $((weekday - 1)) days" +%Y-%m-%d)
            echo "$monday" "$today"
            ;;
        -m)
            local first_day
            first_day=$(date +%Y-%m)-01
            echo "$first_day" "$today"
            ;;
        *)
            local d
            d=$(get_date "${1:-$today}")
            echo "$d" "$d"
            ;;
    esac
}

# 按 commit 前缀分类
classify_commit() {
    local prefix="$1"
    case "$prefix" in
        feat*|Feat*)    echo "新功能" ;;
        fix*|Fix*)      echo "Bug 修复" ;;
        docs*|Docs*)    echo "文档" ;;
        refactor*|Refactor*) echo "重构" ;;
        chore*|Chore*)  echo "工程配置" ;;
        test*|Test*)    echo "测试" ;;
        style*|Style*)  echo "代码风格" ;;
        perf*|Perf*)    echo "性能优化" ;;
        *)              echo "其他" ;;
    esac
}

format_commits_section() {
    local since="$1"
    local until="$2"

    if [ "$since" = "$until" ]; then
        until=$(date -v+1d -jf "%Y-%m-%d" "$since" +%Y-%m-%d 2>/dev/null || date -d "$since + 1 day" +%Y-%m-%d)
    fi

    local commits
    commits=$(git log --since="$since" --until="$until" \
        --pretty=format:"%h|%s|%an" \
        --no-merges 2>/dev/null)

    if [ -z "$commits" ]; then
        echo "_当日无已提交记录_"
        return
    fi

    # 按类别分组输出
    echo "$commits" | while IFS='|' read -r hash msg author; do
        local prefix="${msg%%:*}"
        local category
        category=$(classify_commit "$prefix")
        echo "CATEGORY_SEP|$category|$hash|$msg|$author"
    done | sort -t'|' -k2 | while IFS='|' read -r sep category hash msg author; do
        echo "- **[$category]** \`$hash\` — $msg _($author)_"
    done
}

format_commits_with_files() {
    local since="$1"
    local until="$2"

    if [ "$since" = "$until" ]; then
        until=$(date -v+1d -jf "%Y-%m-%d" "$since" +%Y-%m-%d 2>/dev/null || date -d "$since + 1 day" +%Y-%m-%d)
    fi

    local hashes
    hashes=$(git log --since="$since" --until="$until" --pretty=format:"%h" --no-merges 2>/dev/null)

    if [ -z "$hashes" ]; then
        return
    fi

    echo ""
    echo "### 每次提交涉及的文件"
    echo ""

    for hash in $hashes; do
        local msg
        msg=$(git log -1 --pretty=format:"%s" "$hash")
        local prefix="${msg%%:*}"
        local category
        category=$(classify_commit "$prefix")
        echo "**\`$hash\`** [$category] $msg"
        echo ""
        echo '```text'
        git -c core.quotepath=false diff-tree --no-commit-id --stat -r "$hash" 2>/dev/null | \
            sed 's|AI-Agent整合学习路线/||g'
        echo '```'
        echo ""
    done
}

get_diff_stat() {
    # 直接输出 git diff --stat（含行级变更）
    git -c core.quotepath=false diff --stat 2>/dev/null
}

get_new_files() {
    # 获取未跟踪的新文件
    git -c core.quotepath=false status --porcelain 2>/dev/null | \
        grep '^??' | sed 's/^...//' | sort
}

format_uncommitted_changes() {
    # 1. 已跟踪文件的 diff stat
    local diff_output
    diff_output=$(get_diff_stat)

    if [ -n "$diff_output" ]; then
        echo ""
        echo "### 已跟踪文件的变更（+添加行 / -删除行）"
        echo ""
        echo '```text'
        echo "$diff_output"
        echo '```'
    fi

    # 2. 新增未跟踪文件
    local new_files
    new_files=$(get_new_files)

    if [ -n "$new_files" ]; then
        echo ""
        echo "### 新增未跟踪文件"
        echo ""
        echo '```text'
        echo "$new_files"
        echo '```'
    fi

    if [ -z "$diff_output" ] && [ -z "$new_files" ]; then
        echo "_无未提交变更_"
    fi
}

get_diff_summary() {
    # 汇总：总添加行数、总删除行数、总变更文件数
    local staged unstaged total_added total_deleted total_files

    staged=$(git diff --cached --numstat 2>/dev/null)
    unstaged=$(git diff --numstat 2>/dev/null)

    total_added=$( (
        echo "$staged"; echo "$unstaged"
    ) | awk '{sum += $1} END {print sum}')
    total_deleted=$( (
        echo "$staged"; echo "$unstaged"
    ) | awk '{sum += $2} END {print sum}')
    total_files=$( (
        echo "$staged"; echo "$unstaged"
    ) | grep -c '.' || echo 0)

    echo ""
    echo "| 指标 | 数值 |"
    echo "|------|------|"
    echo "| 代码新增行数 | +${total_added:-0} |"
    echo "| 代码删除行数 | -${total_deleted:-0} |"
    echo "| 涉及文件数 | ${total_files:-0} |"
}

generate_daily_log() {
    local date_str="$1"
    local since="$2"
    local until="$3"
    local output_file="$CHANGE_LOG_DIR/$date_str.md"
    local title_suffix=""

    if [ "$since" != "$until" ]; then
        title_suffix="（$since ~ $until）"
    fi

    # 计算 commit 数量
    if [ "$since" = "$until" ]; then
        local u
        u=$(date -v+1d -jf "%Y-%m-%d" "$since" +%Y-%m-%d 2>/dev/null || date -d "$since + 1 day" +%Y-%m-%d)
    else
        u="$until"
    fi
    local commit_count
    commit_count=$(git log --since="$since" --until="$u" --oneline --no-merges 2>/dev/null | wc -l | tr -d ' ')
    commit_count=${commit_count:-0}

    local uncommit_count
    uncommit_count=$(git status --short 2>/dev/null | wc -l | tr -d ' ')
    uncommit_count=${uncommit_count:-0}

    cat > "$output_file" << EOF
# 变更日志 - $date_str$title_suffix

> 自动生成于 $(date '+%Y-%m-%d %H:%M:%S') | 项目: AI-Agent整合学习路线

---

## 一、已提交变更 ($commit_count 个 commit)

$(format_commits_section "$since" "$until")
$(format_commits_with_files "$since" "$until")

---

## 二、未提交变更 ($uncommit_count 个文件)

$(format_uncommitted_changes)

---

## 三、变更统计

### 提交统计

| 指标 | 数值 |
|------|------|
| Commit 数 | $commit_count |
| 未提交文件数 | $uncommit_count |
$(get_diff_summary)

---

> **手动补充区** — 在此记录自动生成无法覆盖的内容，如：设计决策、遇到的问题、方案取舍、下一步计划。
>
> - 
> - 
EOF

    echo "已生成: $output_file"
}

# ---------- main ----------

MODE=""
DATE_ARG=""

for arg in "$@"; do
    case "$arg" in
        -w|-m) MODE="$arg" ;;
        *) DATE_ARG="$arg" ;;
    esac
done

if [ -n "$MODE" ]; then
    read -r SINCE UNTIL <<< "$(get_date_range "$MODE")"
    LABEL="${SINCE}_to_${UNTIL}"
    generate_daily_log "$LABEL" "$SINCE" "$UNTIL"
else
    TARGET_DATE=$(get_date "$DATE_ARG")
    read -r SINCE UNTIL <<< "$(get_date_range "$TARGET_DATE")"
    generate_daily_log "$TARGET_DATE" "$SINCE" "$UNTIL"
fi

echo "Done."
