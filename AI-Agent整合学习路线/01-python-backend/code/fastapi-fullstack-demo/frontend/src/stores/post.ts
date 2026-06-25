import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api from '@/utils/api';
import { ElMessage } from 'element-plus';
import type {
  Post,
  PostSimple,
  Tag,
  TagWithPosts,
  CreatePostData,
  UpdatePostData,
  CreateTagData,
  UpdateTagData
} from '@/types/post';

export type { Post, PostSimple, Tag, TagWithPosts, CreatePostData, UpdatePostData, CreateTagData, UpdateTagData };

export const usePostStore = defineStore('post', () => {
  // State
  const posts = ref<PostSimple[]>([]);
  const currentPost = ref<Post | null>(null);
  const tags = ref<Tag[]>([]);
  const currentTag = ref<TagWithPosts | null>(null);
  const loading = ref(false);
  const total = ref(0);

  // Getters
  const publishedPosts = computed(() =>
    posts.value.filter(post => post.is_published)
  );

  const draftPosts = computed(() =>
    posts.value.filter(post => !post.is_published)
  );

  // Actions - 文章相关
  async function fetchPosts(params?: {
    skip?: number;
    limit?: number;
    is_published?: boolean;
    author_id?: number;
    tag_id?: number;
  }) {
    loading.value = true;
    try {
      const data = await api.get<PostSimple[]>('/posts/', { params });
      posts.value = data;
      return data;
    } catch (error) {
      ElMessage.error('获取文章列表失败');
      throw error;
    } finally {
      loading.value = false;
    }
  }

  async function fetchPost(id: number): Promise<Post> {
    loading.value = true;
    try {
      const data = await api.get<Post>(`/posts/${id}`);
      currentPost.value = data;
      return data;
    } catch (error) {
      ElMessage.error('获取文章详情失败');
      throw error;
    } finally {
      loading.value = false;
    }
  }

  async function createPost(data: CreatePostData, authorId: number) {
    loading.value = true;
    try {
      const result = await api.post(`/posts/?author_id=${authorId}`, data);
      ElMessage.success('文章创建成功');
      return result;
    } catch (error: any) {
      ElMessage.error(error.response?.data?.detail || '创建文章失败');
      throw error;
    } finally {
      loading.value = false;
    }
  }

  async function updatePost(id: number, data: UpdatePostData) {
    loading.value = true;
    try {
      const result = await api.patch(`/posts/${id}`, data);
      ElMessage.success('文章更新成功');
      if (currentPost.value?.id === id) {
        currentPost.value = result;
      }
      return result;
    } catch (error: any) {
      ElMessage.error(error.response?.data?.detail || '更新文章失败');
      throw error;
    } finally {
      loading.value = false;
    }
  }

  async function deletePost(id: number) {
    loading.value = true;
    try {
      await api.delete(`/posts/${id}`);
      ElMessage.success('文章删除成功');
      posts.value = posts.value.filter(post => post.id !== id);
    } catch (error: any) {
      ElMessage.error(error.response?.data?.detail || '删除文章失败');
      throw error;
    } finally {
      loading.value = false;
    }
  }

  async function publishPost(id: number) {
    loading.value = true;
    try {
      const result = await api.post(`/posts/${id}/publish`);
      ElMessage.success('文章发布成功');
      if (currentPost.value?.id === id) {
        currentPost.value = result;
      }
      return result;
    } catch (error: any) {
      ElMessage.error(error.response?.data?.detail || '发布文章失败');
      throw error;
    } finally {
      loading.value = false;
    }
  }

  async function unpublishPost(id: number) {
    loading.value = true;
    try {
      const result = await api.post(`/posts/${id}/unpublish`);
      ElMessage.success('文章已取消发布');
      if (currentPost.value?.id === id) {
        currentPost.value = result;
      }
      return result;
    } catch (error: any) {
      ElMessage.error(error.response?.data?.detail || '取消发布失败');
      throw error;
    } finally {
      loading.value = false;
    }
  }

  // Actions - 标签相关
  async function fetchTags(params?: { skip?: number; limit?: number }) {
    loading.value = true;
    try {
      const data = await api.get<Tag[]>('/posts/tags/', { params });
      tags.value = data;
      return data;
    } catch (error) {
      ElMessage.error('获取标签列表失败');
      throw error;
    } finally {
      loading.value = false;
    }
  }

  async function fetchTag(id: number): Promise<TagWithPosts> {
    loading.value = true;
    try {
      const data = await api.get<TagWithPosts>(`/posts/tags/${id}`);
      currentTag.value = data;
      return data;
    } catch (error) {
      ElMessage.error('获取标签详情失败');
      throw error;
    } finally {
      loading.value = false;
    }
  }

  async function createTag(data: CreateTagData) {
    loading.value = true;
    try {
      const result = await api.post<Tag>('/posts/tags/', data);
      ElMessage.success('标签创建成功');
      tags.value.push(result);
      return result;
    } catch (error: any) {
      ElMessage.error(error.response?.data?.detail || '创建标签失败');
      throw error;
    } finally {
      loading.value = false;
    }
  }

  async function updateTag(id: number, data: UpdateTagData) {
    loading.value = true;
    try {
      const result = await api.patch<Tag>(`/posts/tags/${id}`, data);
      ElMessage.success('标签更新成功');
      const index = tags.value.findIndex(tag => tag.id === id);
      if (index !== -1) {
        tags.value[index] = result;
      }
      return result;
    } catch (error: any) {
      ElMessage.error(error.response?.data?.detail || '更新标签失败');
      throw error;
    } finally {
      loading.value = false;
    }
  }

  async function deleteTag(id: number) {
    loading.value = true;
    try {
      await api.delete(`/posts/tags/${id}`);
      ElMessage.success('标签删除成功');
      tags.value = tags.value.filter(tag => tag.id !== id);
    } catch (error: any) {
      ElMessage.error(error.response?.data?.detail || '删除标签失败');
      throw error;
    } finally {
      loading.value = false;
    }
  }

  // Actions - 文章标签管理
  async function addTagToPost(postId: number, tagId: number) {
    loading.value = true;
    try {
      const result = await api.post(`/posts/${postId}/tags/${tagId}`);
      ElMessage.success('标签添加成功');
      if (currentPost.value?.id === postId) {
        currentPost.value = result;
      }
      return result;
    } catch (error: any) {
      ElMessage.error(error.response?.data?.detail || '添加标签失败');
      throw error;
    } finally {
      loading.value = false;
    }
  }

  async function removeTagFromPost(postId: number, tagId: number) {
    loading.value = true;
    try {
      const result = await api.delete(`/posts/${postId}/tags/${tagId}`);
      ElMessage.success('标签移除成功');
      if (currentPost.value?.id === postId) {
        currentPost.value = result;
      }
      return result;
    } catch (error: any) {
      ElMessage.error(error.response?.data?.detail || '移除标签失败');
      throw error;
    } finally {
      loading.value = false;
    }
  }

  return {
    // State
    posts,
    currentPost,
    tags,
    currentTag,
    loading,
    total,
    // Getters
    publishedPosts,
    draftPosts,
    // Actions - 文章
    fetchPosts,
    fetchPost,
    createPost,
    updatePost,
    deletePost,
    publishPost,
    unpublishPost,
    // Actions - 标签
    fetchTags,
    fetchTag,
    createTag,
    updateTag,
    deleteTag,
    // Actions - 文章标签
    addTagToPost,
    removeTagFromPost
  };
});
