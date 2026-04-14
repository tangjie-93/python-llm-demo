<template>
  <div class="posts-container">
    <div class="posts-container__header">
      <h2>博客文章</h2>
      <el-button type="primary" @click="handleOpenCreate">
        <el-icon><Plus /></el-icon>
        写文章
      </el-button>
    </div>

    <el-card class="posts-container__filter" shadow="never">
      <el-form :inline="true" :model="filterForm">
        <el-form-item label="状态">
          <el-select
            v-model="filterForm.is_published"
            placeholder="全部状态"
            clearable
          >
            <el-option label="已发布" :value="true" />
            <el-option label="草稿" :value="false" />
          </el-select>
        </el-form-item>
        <el-form-item label="标签">
          <el-select
            v-model="filterForm.tag_id"
            placeholder="全部标签"
            clearable
          >
            <el-option
              v-for="tag in postStore.tags"
              :key="tag.id"
              :label="tag.name"
              :value="tag.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleFilter">筛选</el-button>
          <el-button @click="handleResetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card v-loading="postStore.loading" shadow="never">
      <el-empty v-if="postStore.posts.length === 0" description="暂无文章" />

      <div v-else class="posts-container__list">
        <div
          v-for="post in postStore.posts"
          :key="post.id"
          class="posts-container__item"
          @click="handleViewPost(post.id)"
        >
          <div class="posts-container__post-header">
            <h3 class="posts-container__title">{{ post.title }}</h3>
            <el-tag v-if="post.is_published" type="success" size="small">
              已发布
            </el-tag>
            <el-tag v-else type="info" size="small">草稿</el-tag>
          </div>

          <p class="posts-container__summary">{{ post.summary || '暂无摘要' }}</p>

          <div class="posts-container__meta">
            <span class="posts-container__meta-item">
              <el-icon><View /></el-icon>
              {{ post.view_count }} 阅读
            </span>
            <span class="meta-item">
              <el-icon><Clock /></el-icon>
              {{ formatDate(post.created_at) }}
            </span>
            <span class="meta-item">
              <el-icon><User /></el-icon>
              作者 ID: {{ post.author_id }}
            </span>
          </div>

          <div class="posts-container__actions">
            <el-button
              v-if="!post.is_published"
              type="success"
              size="small"
              @click.stop="handlePublish(post.id)"
            >
              发布
            </el-button>
            <el-button
              v-else
              type="warning"
              size="small"
              @click.stop="handleUnpublish(post.id)"
            >
              取消发布
            </el-button>
            <el-button
              type="primary"
              size="small"
              @click.stop="handleEdit(post)"
            >
              编辑
            </el-button>
            <el-button
              type="danger"
              size="small"
              @click.stop="handleDelete(post.id)"
            >
              删除
            </el-button>
          </div>
        </div>
      </div>

      <div class="posts-container__pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.limit"
          :total="pagination.total"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑文章' : '写文章'"
      width="800px"
      destroy-on-close
    >
      <el-form
        ref="formRef"
        :model="postForm"
        label-width="80px"
        :rules="formRules"
      >
        <el-form-item label="标题" prop="title">
          <el-input v-model="postForm.title" placeholder="请输入文章标题" />
        </el-form-item>

        <el-form-item label="摘要">
          <el-input
            v-model="postForm.summary"
            type="textarea"
            :rows="2"
            placeholder="请输入文章摘要（可选）"
          />
        </el-form-item>

        <el-form-item label="内容" prop="content">
          <el-input
            v-model="postForm.content"
            type="textarea"
            :rows="10"
            placeholder="请输入文章内容"
          />
        </el-form-item>

        <el-form-item label="标签">
          <el-select
            v-model="postForm.tag_ids"
            multiple
            placeholder="选择标签"
            style="width: 100%"
          >
            <el-option
              v-for="tag in postStore.tags"
              :key="tag.id"
              :label="tag.name"
              :value="tag.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="状态">
          <el-switch
            v-model="postForm.is_published"
            active-text="立即发布"
            inactive-text="保存为草稿"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="isSubmitting">
          {{ isEdit ? '保存' : '创建' }}
        </el-button>
      </template>
    </el-dialog>

    <el-dialog
      v-model="detailVisible"
      title="文章详情"
      width="800px"
      destroy-on-close
    >
      <div v-if="postStore.currentPost" class="post-detail">
        <h2>{{ postStore.currentPost.title }}</h2>
        <div class="post-detail__meta">
          <el-tag v-if="postStore.currentPost.is_published" type="success">
            已发布
          </el-tag>
          <el-tag v-else type="info">草稿</el-tag>
          <span>
            <el-icon><View /></el-icon>
            {{ postStore.currentPost.view_count }} 阅读
          </span>
          <span>
            <el-icon><Clock /></el-icon>
            {{ formatDate(postStore.currentPost.created_at) }}
          </span>
          <span v-if="postStore.currentPost.author">
            <el-icon><User /></el-icon>
            {{ postStore.currentPost.author.username }}
          </span>
        </div>

        <div class="post-detail__tags" v-if="postStore.currentPost.tags?.length">
          <el-tag
            v-for="tag in postStore.currentPost.tags"
            :key="tag.id"
            size="small"
            class="tag-item"
          >
            {{ tag.name }}
          </el-tag>
        </div>

        <el-divider />

        <div class="post-detail__content">{{ postStore.currentPost.content }}</div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts" name="PostsView">
import { ref, reactive, onMounted } from 'vue';
import { ElMessageBox, type FormInstance, type FormRules } from 'element-plus';
import { Plus, View, Clock, User } from '@element-plus/icons-vue';
import { usePostStore, type CreatePostData, type UpdatePostData, type PostSimple, type Tag } from '@/stores/post';
import { useAuthStore } from '@/stores/auth';
import type { PostFilterParams } from '@/types/post';

const postStore = usePostStore();
const authStore = useAuthStore();

const filterForm = reactive<PostFilterParams & { is_published?: boolean | undefined; tag_id?: number | undefined }>({
  is_published: undefined,
  tag_id: undefined
});

const pagination = reactive({
  page: 1,
  limit: 10,
  total: 0
});

const dialogVisible = ref(false);
const detailVisible = ref(false);
const isEdit = ref(false);
const isSubmitting = ref(false);
const formRef = ref<FormInstance>();

const postForm = reactive<CreatePostData & { id?: number }>({
  title: '',
  content: '',
  summary: '',
  is_published: false,
  tag_ids: []
});

const formRules: FormRules = {
  title: [
    { required: true, message: '请输入标题', trigger: 'blur' },
    { min: 1, max: 200, message: '标题长度在 1-200 个字符', trigger: 'blur' }
  ],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }]
};

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

async function loadPosts(): Promise<void> {
  const skip = (pagination.page - 1) * pagination.limit;
  await postStore.fetchPosts({
    skip,
    limit: pagination.limit,
    is_published: filterForm.is_published,
    tag_id: filterForm.tag_id
  });
}

function handleFilter(): void {
  pagination.page = 1;
  loadPosts();
}

function handleResetFilter(): void {
  filterForm.is_published = undefined;
  filterForm.tag_id = undefined;
  pagination.page = 1;
  loadPosts();
}

function handleSizeChange(size: number): void {
  pagination.limit = size;
  loadPosts();
}

function handlePageChange(page: number): void {
  pagination.page = page;
  loadPosts();
}

async function handleViewPost(id: number): Promise<void> {
  await postStore.fetchPost(id);
  detailVisible.value = true;
}

function handleOpenCreate(): void {
  isEdit.value = false;
  resetForm();
  dialogVisible.value = true;
}

async function handleEdit(post: PostSimple): Promise<void> {
  isEdit.value = true;
  const fullPost = await postStore.fetchPost(post.id);
  postForm.id = fullPost.id;
  postForm.title = fullPost.title;
  postForm.content = fullPost.content || '';
  postForm.summary = fullPost.summary || '';
  postForm.is_published = fullPost.is_published;
  postForm.tag_ids = fullPost.tags?.map((t: Tag) => t.id) || [];
  dialogVisible.value = true;
}

async function handleSubmit(): Promise<void> {
  const valid = await formRef.value?.validate().catch(() => false);
  if (!valid) return;

  isSubmitting.value = true;
  try {
    if (isEdit.value && postForm.id) {
      const updateData: UpdatePostData = {
        title: postForm.title,
        content: postForm.content,
        summary: postForm.summary || undefined,
        is_published: postForm.is_published,
        tag_ids: postForm.tag_ids
      };
      await postStore.updatePost(postForm.id, updateData);
    } else {
      const createData: CreatePostData = {
        title: postForm.title,
        content: postForm.content,
        summary: postForm.summary || undefined,
        is_published: postForm.is_published,
        tag_ids: postForm.tag_ids
      };
      const authorId = authStore.userInfo?.id || 1;
      await postStore.createPost(createData, authorId);
    }
    dialogVisible.value = false;
    resetForm();
    loadPosts();
  } finally {
    isSubmitting.value = false;
  }
}

function resetForm(): void {
  postForm.id = undefined;
  postForm.title = '';
  postForm.content = '';
  postForm.summary = '';
  postForm.is_published = false;
  postForm.tag_ids = [];
}

async function handlePublish(id: number): Promise<void> {
  try {
    await postStore.publishPost(id);
    loadPosts();
  } catch {
    // error handled in store
  }
}

async function handleUnpublish(id: number): Promise<void> {
  try {
    await postStore.unpublishPost(id);
    loadPosts();
  } catch {
    // error handled in store
  }
}

async function handleDelete(id: number): Promise<void> {
  try {
    await ElMessageBox.confirm('确定要删除这篇文章吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    });
    await postStore.deletePost(id);
    loadPosts();
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error);
    }
  }
}

onMounted(() => {
  loadPosts();
  postStore.fetchTags();
});
</script>

<style scoped lang="less">
.posts-container {
  padding: 20px;

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    h2 {
      margin: 0;
      color: #303133;
    }
  }

  &__filter {
    margin-bottom: 20px;
  }

  &__list {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  &__item {
    padding: 20px;
    border: 1px solid #ebeef5;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s;

    &:hover {
      box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
      border-color: #409eff;
    }
  }

  &__post-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
  }

  &__title {
    margin: 0;
    font-size: 18px;
    color: #303133;
    flex: 1;
  }

  &__summary {
    color: #606266;
    margin: 0 0 12px 0;
    line-height: 1.6;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  &__meta {
    display: flex;
    gap: 20px;
    color: #909399;
    font-size: 14px;
    margin-bottom: 12px;

    &-item {
      display: flex;
      align-items: center;
      gap: 4px;
    }
  }

  &__actions {
    display: flex;
    gap: 8px;
  }

  &__pagination {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
}

.post-detail {
  h2 {
    margin: 0 0 16px 0;
    color: #303133;
  }

  &__meta {
    display: flex;
    gap: 20px;
    color: #909399;
    font-size: 14px;
    margin-bottom: 16px;

    span {
      display: flex;
      align-items: center;
      gap: 4px;
    }
  }

  &__tags {
    margin-bottom: 16px;

    .tag-item {
      margin-right: 8px;
    }
  }

  &__content {
    line-height: 1.8;
    color: #606266;
    white-space: pre-wrap;
  }
}
</style>
