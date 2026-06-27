<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { fetchContentDetail } from '@/api/intelligence';
import type { ContentItem } from '@/types/intelligence';

const route = useRoute();
const item = ref<ContentItem | null>(null);

onMounted(async () => {
  item.value = await fetchContentDetail(String(route.params.id));
});
</script>

<template>
  <article v-if="item" class="detail">
    <p class="category">{{ item.category }}</p>
    <h1>{{ item.title }}</h1>
    <p class="summary">{{ item.summary }}</p>
    <div class="tags">
      <el-tag v-for="tag in item.tags" :key="tag">{{ tag }}</el-tag>
    </div>
    <h2>关键要点</h2>
    <ul>
      <li v-for="point in item.key_points" :key="point">{{ point }}</li>
    </ul>
    <p>{{ item.reason }}</p>
    <a :href="item.url" target="_blank" rel="noreferrer">打开原文</a>
  </article>
</template>

<style scoped>
.detail {
  max-width: 800px;
}

.category {
  color: #2563eb;
  font-weight: 700;
}

.summary {
  color: #374151;
  font-size: 18px;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 16px 0;
}
</style>
