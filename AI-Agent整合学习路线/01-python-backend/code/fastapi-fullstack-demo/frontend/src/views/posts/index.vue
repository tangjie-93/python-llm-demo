<template>
  <div class="posts-page">
    <!-- 工具栏 -->
    <div class="posts-page__toolbar">
      <BaseFilterForm
        v-model="filterForm"
        @filter="handleFilter"
        @reset="handleResetFilter"
      >
        <template #default>
          <el-form-item label="状态" style="width: 150px;">
            <el-select
              v-model="filterForm.is_published"
              placeholder="全部状态"
              clearable
              style="width: 100%;"
            >
              <el-option label="已发布" :value="true" />
              <el-option label="草稿" :value="false" />
            </el-select>
          </el-form-item>
          <el-form-item label="标签" style="width: 150px;">
            <el-select
              v-model="filterForm.tag_id"
              placeholder="全部标签"
              clearable
              style="width: 100%;"
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
            <el-button type="primary" @click="handleOpenCreate">
              <el-icon><Plus /></el-icon>
              写文章
            </el-button>
          </el-form-item>
        </template>
      </BaseFilterForm>
    </div>

    <div class="posts-page__table">
      <BaseTable
        :data="postStore.posts"
        :loading="postStore.loading"
        :border="true"
        height="100%"
      >
        <el-table-column
          prop="title"
          label="标题"
          min-width="200"
        >
          <template #default="{ row }">
            <div class="post-title" @click="handleViewPost(row.id)">
              {{ row.title }}
            </div>
          </template>
        </el-table-column>
        <el-table-column
          prop="is_published"
          label="状态"
          width="100"
        >
          <template #default="{ row }">
            <el-tag :type="row.is_published ? 'success' : 'info'" size="small">
              {{ row.is_published ? '已发布' : '草稿' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="view_count"
          label="阅读"
          width="80"
        >
          <template #default="{ row }">
            <span class="meta-info">
              <el-icon><View /></el-icon>
              {{ row.view_count }}
            </span>
          </template>
        </el-table-column>
        <el-table-column
          label="作者"
          width="120"
        >
          <template #default="{ row }">
            <span class="meta-info">
              <el-icon><User /></el-icon>
              ID: {{ row.author_id }}
            </span>
          </template>
        </el-table-column>
        <el-table-column
          label="创建时间"
          width="180"
        >
          <template #default="{ row }">
            <span class="meta-info">
              <el-icon><Clock /></el-icon>
              {{ formatDate(row.created_at) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column
          label="操作"
          fixed="right"
          width="280"
        >
          <template #default="{ row }">
            <el-button
              v-if="!row.is_published"
              type="success"
              size="small"
              plain
              @click.stop="handlePublish(row.id)"
            >
              发布
            </el-button>
            <el-button
              v-else
              type="warning"
              size="small"
              plain
              @click.stop="handleUnpublish(row.id)"
            >
              取消发布
            </el-button>
            <el-button
              type="primary"
              size="small"
              plain
              @click.stop="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              type="danger"
              size="small"
              plain
              @click.stop="handleDelete(row.id)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </BaseTable>

      <div class="posts-page__pagination">
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
    </div>

    <BaseFormDialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑文章' : '写文章'"
      :form-data="postForm"
      :rules="formRules"
      :submit-loading="isSubmitting"
      width="800px"
      @submit="handleFormSubmit"
    >
      <template #default="{ form }">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入文章标题" />
        </el-form-item>

        <el-form-item label="摘要">
          <el-input
            v-model="form.summary"
            type="textarea"
            :rows="2"
            placeholder="请输入文章摘要（可选）"
          />
        </el-form-item>

        <el-form-item label="内容" prop="content">
          <el-input
            v-model="form.content"
            type="textarea"
            :rows="10"
            placeholder="请输入文章内容"
          />
        </el-form-item>

        <el-form-item label="标签">
          <el-select
            v-model="form.tag_ids"
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
            v-model="form.is_published"
            active-text="立即发布"
            inactive-text="保存为草稿"
          />
        </el-form-item>
      </template>
    </BaseFormDialog>

    <PostDetailDialog
      v-model="detailVisible"
      :post="postStore.currentPost"
    />
  </div>
</template>

<script setup lang="ts" name="PostsView">
import { ref, reactive, onMounted } from 'vue';
import { ElMessageBox, type FormInstance, type FormRules } from 'element-plus';
import { Plus, View, Clock, User } from '@element-plus/icons-vue';
import { usePostStore, type CreatePostData, type UpdatePostData, type PostSimple, type Tag } from '@/stores/post';
import { useAuthStore } from '@/stores/auth';
import type { PostFilterParams } from '@/types/post';
import { BaseFormDialog, BaseFilterForm, BaseTable } from '@/components/common';
import PostDetailDialog from './components/postDetailDialog.vue';

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

async function handleFormSubmit(formRef: FormInstance | undefined): Promise<void> {
  if (!formRef) return;

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
.posts-page {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 20px;

  &__toolbar {
    margin-bottom: 16px;
  }

  &__table {
    flex: 1;
    display: flex;
    flex-direction: column;
    background-color: white;
    border-radius: 8px;
    padding: 16px;
  }

  &__pagination {
    margin-top: 16px;
    display: flex;
    justify-content: flex-end;
  }
}

.post-title {
  color: #409eff;
  cursor: pointer;
  font-weight: 500;
  
  &:hover {
    text-decoration: underline;
  }
}

.meta-info {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #909399;
  font-size: 13px;
  
  .el-icon {
    color: #c0c4cc;
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
