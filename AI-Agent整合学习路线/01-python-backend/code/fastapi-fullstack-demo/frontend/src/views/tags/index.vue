<template>
  <div class="tags-container">
    <div class="tags-container__header">
      <h2>标签管理</h2>
      <el-button type="primary" @click="handleOpenCreate">
        <el-icon><Plus /></el-icon>
        新建标签
      </el-button>
    </div>

    <el-card v-loading="postStore.loading" shadow="never">
      <el-empty v-if="postStore.tags.length === 0" description="暂无标签" />

      <div v-else class="tags-container__list">
        <el-card
          v-for="tag in postStore.tags"
          :key="tag.id"
          class="tags-container__card"
          shadow="hover"
          @click="handleViewTag(tag.id)"
        >
          <div class="tags-container__tag-header">
            <el-tag size="large" effect="dark">{{ tag.name }}</el-tag>
            <div class="tag-actions" @click.stop>
              <el-button type="primary" link size="small" @click="handleEdit(tag)">
                编辑
              </el-button>
              <el-button type="danger" link size="small" @click="handleDelete(tag.id)">
                删除
              </el-button>
            </div>
          </div>
          <p class="tags-container__description">{{ tag.description || '暂无描述' }}</p>
          <div class="tags-container__meta">
            <el-icon><Clock /></el-icon>
            {{ formatDate(tag.created_at) }}
          </div>
        </el-card>
      </div>
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑标签' : '新建标签'"
      width="500px"
      destroy-on-close
    >
      <el-form
        ref="formRef"
        :model="tagForm"
        label-width="80px"
        :rules="formRules"
      >
        <el-form-item label="名称" prop="name">
          <el-input v-model="tagForm.name" placeholder="请输入标签名称" />
        </el-form-item>

        <el-form-item label="描述">
          <el-input
            v-model="tagForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入标签描述（可选）"
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
      title="标签详情"
      width="700px"
      destroy-on-close
    >
      <div v-if="postStore.currentTag" class="tag-detail">
        <div class="tag-detail__header">
          <el-tag size="large" effect="dark">{{ postStore.currentTag.name }}</el-tag>
          <p class="tag-detail__description">{{ postStore.currentTag.description || '暂无描述' }}</p>
        </div>

        <el-divider />

        <h4>关联文章</h4>
        <div v-if="postStore.currentTag.posts?.length" class="tag-detail__posts">
          <div
            v-for="post in postStore.currentTag.posts"
            :key="post.id"
            class="tag-detail__post-item"
          >
            <h5>{{ post.title }}</h5>
            <p>{{ post.summary || '暂无摘要' }}</p>
            <div class="post-meta">
              <el-tag v-if="post.is_published" type="success" size="small">
                已发布
              </el-tag>
              <el-tag v-else type="info" size="small">草稿</el-tag>
              <span>
                <el-icon><View /></el-icon>
                {{ post.view_count }} 阅读
              </span>
            </div>
          </div>
        </div>
        <el-empty v-else description="暂无关联文章" />
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts" name="TagsView">
import { ref, reactive, onMounted } from 'vue';
import { ElMessageBox, type FormInstance, type FormRules } from 'element-plus';
import { Plus, Clock, View } from '@element-plus/icons-vue';
import { usePostStore, type CreateTagData, type UpdateTagData, type Tag } from '@/stores/post';

const postStore = usePostStore();

const dialogVisible = ref(false);
const detailVisible = ref(false);
const isEdit = ref(false);
const isSubmitting = ref(false);
const formRef = ref<FormInstance>();

const tagForm = reactive<CreateTagData & { id?: number }>({
  name: '',
  description: ''
});

const formRules: FormRules = {
  name: [
    { required: true, message: '请输入标签名称', trigger: 'blur' },
    { min: 1, max: 50, message: '标签名称长度在 1-50 个字符', trigger: 'blur' }
  ]
};

function formatDate(dateStr: string): string {
  const date = new Date(dateStr);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
}

async function handleViewTag(id: number): Promise<void> {
  await postStore.fetchTag(id);
  detailVisible.value = true;
}

function handleOpenCreate(): void {
  isEdit.value = false;
  resetForm();
  dialogVisible.value = true;
}

function handleEdit(tag: Tag): void {
  isEdit.value = true;
  tagForm.id = tag.id;
  tagForm.name = tag.name;
  tagForm.description = tag.description || '';
  dialogVisible.value = true;
}

async function handleSubmit(): Promise<void> {
  const valid = await formRef.value?.validate().catch(() => false);
  if (!valid) return;

  isSubmitting.value = true;
  try {
    if (isEdit.value && tagForm.id) {
      const updateData: UpdateTagData = {
        name: tagForm.name,
        description: tagForm.description || undefined
      };
      await postStore.updateTag(tagForm.id, updateData);
    } else {
      const createData: CreateTagData = {
        name: tagForm.name,
        description: tagForm.description || undefined
      };
      await postStore.createTag(createData);
    }
    dialogVisible.value = false;
    resetForm();
  } finally {
    isSubmitting.value = false;
  }
}

function resetForm(): void {
  tagForm.id = undefined;
  tagForm.name = '';
  tagForm.description = '';
}

async function handleDelete(id: number): Promise<void> {
  try {
    await ElMessageBox.confirm('确定要删除这个标签吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    });
    await postStore.deleteTag(id);
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error);
    }
  }
}

onMounted(() => {
  postStore.fetchTags();
});
</script>

<style scoped lang="less">
.tags-container {
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

  &__list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 16px;
  }

  &__card {
    cursor: pointer;
    transition: all 0.3s;

    &:hover {
      transform: translateY(-2px);
    }
  }

  &__tag-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }

  &__description {
    color: #606266;
    margin: 0 0 12px 0;
    font-size: 14px;
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  &__meta {
    color: #909399;
    font-size: 13px;
    display: flex;
    align-items: center;
    gap: 4px;
  }
}

.tag-detail {
  &__header {
    margin-bottom: 16px;
  }

  &__description {
    color: #606266;
    margin: 12px 0 0 0;
  }

  &__posts {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  &__post-item {
    padding: 16px;
    border: 1px solid #ebeef5;
    border-radius: 8px;

    h5 {
      margin: 0 0 8px 0;
      font-size: 16px;
      color: #303133;
    }

    p {
      color: #606266;
      font-size: 14px;
      margin: 0 0 12px 0;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
  }

  &__meta {
    display: flex;
    gap: 16px;
    align-items: center;
    color: #909399;
    font-size: 13px;

    span {
      display: flex;
      align-items: center;
      gap: 4px;
    }
  }
}
</style>
