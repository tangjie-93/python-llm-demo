<template>
    <div class="post-detail-dialog">
        <el-dialog
            v-model="dialogVisible"
            title="文章详情"
            width="800px"
            destroy-on-close
        >
            <div v-if="post" class="post-detail-dialog__content">
                <h2 class="post-detail-dialog__title">{{ post.title }}</h2>
                <div class="post-detail-dialog__meta">
                    <el-tag :type="post.is_published ? 'success' : 'info'">
                        {{ post.is_published ? '已发布' : '草稿' }}
                    </el-tag>
                    <span class="post-detail-dialog__meta-item">
                        <el-icon><View /></el-icon>
                        {{ post.view_count }} 阅读
                    </span>
                    <span class="post-detail-dialog__meta-item">
                        <el-icon><Clock /></el-icon>
                        {{ formatDate(post.created_at) }}
                    </span>
                    <span v-if="post.author" class="post-detail-dialog__meta-item">
                        <el-icon><User /></el-icon>
                        {{ post.author.username }}
                    </span>
                </div>

                <div v-if="post.tags?.length" class="post-detail-dialog__tags">
                    <el-tag
                        v-for="tag in post.tags"
                        :key="tag.id"
                        size="small"
                        class="post-detail-dialog__tag-item"
                    >
                        {{ tag.name }}
                    </el-tag>
                </div>

                <el-divider />

                <div class="post-detail-dialog__text">{{ post.content }}</div>
            </div>
        </el-dialog>
    </div>
</template>

<script setup lang="ts" name="PostDetailDialog">
import { computed } from 'vue';
import { View, Clock, User } from '@element-plus/icons-vue';
import type { Post } from '@/stores/post';

interface Props {
    modelValue: boolean;
    post: Post | null;
}

interface Emits {
    (e: 'update:modelValue', value: boolean): void;
}

const props = withDefaults(defineProps<Props>(), {
    post: null
});

const emit = defineEmits<Emits>();

const dialogVisible = computed({
    get: () => props.modelValue,
    set: (value: boolean) => emit('update:modelValue', value)
});

function formatDate(dateStr: string): string {
    const date = new Date(dateStr);
    return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}
</script>

<style scoped lang="less">
.post-detail-dialog {
    &__content {
        padding: 8px 0;
    }

    &__title {
        margin: 0 0 16px 0;
        color: #303133;
        font-size: 20px;
        font-weight: 600;
    }

    &__meta {
        display: flex;
        gap: 16px;
        color: #909399;
        font-size: 13px;
        margin-bottom: 16px;
        align-items: center;
        flex-wrap: wrap;

        &-item {
            display: flex;
            align-items: center;
            gap: 4px;

            .el-icon {
                color: #c0c4cc;
            }
        }
    }

    &__tags {
        margin-bottom: 16px;
        display: flex;
        gap: 8px;
        flex-wrap: wrap;

        &-item {
            cursor: default;
        }
    }

    &__text {
        line-height: 1.8;
        color: #606266;
        white-space: pre-wrap;
        font-size: 14px;
    }
}
</style>
