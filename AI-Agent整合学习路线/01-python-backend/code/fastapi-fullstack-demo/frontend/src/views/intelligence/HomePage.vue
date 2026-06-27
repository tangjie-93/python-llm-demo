<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { fetchIntelligenceHome } from '@/api/intelligence';
import type { HomeData } from '@/types/intelligence';

const data = ref<HomeData | null>(null);
const loading = ref(false);

onMounted(async () => {
  loading.value = true;
  try {
    data.value = await fetchIntelligenceHome();
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <section class="hero">
    <div>
      <p class="eyebrow">每日更新</p>
      <h1>AI Agent 开发者情报站</h1>
      <p class="subtitle">聚合 Agent、RAG、LLM API、MCP、开源项目和工程实践内容。</p>
    </div>
  </section>

  <el-skeleton v-if="loading" :rows="8" animated />

  <template v-else-if="data">
    <section v-if="data.brief" class="section">
      <h2>{{ data.brief.title }}</h2>
      <p>{{ data.brief.summary }}</p>
    </section>

    <section class="section">
      <h2>主题分类</h2>
      <div class="category-grid">
        <RouterLink v-for="category in data.categories" :key="category" :to="`/categories/${encodeURIComponent(category)}`">
          {{ category }}
        </RouterLink>
      </div>
    </section>

    <section class="section">
      <h2>最新内容</h2>
      <div class="item-list">
        <RouterLink v-for="item in data.latest_items" :key="item.id" class="item" :to="`/contents/${item.id}`">
          <span class="item-category">{{ item.category }}</span>
          <strong>{{ item.title }}</strong>
          <p>{{ item.summary }}</p>
        </RouterLink>
      </div>
    </section>
  </template>
</template>

<style scoped>
.hero {
  padding: 40px 0 28px;
}

.eyebrow {
  color: #2563eb;
  font-weight: 700;
}

h1 {
  margin: 0;
  font-size: 42px;
  line-height: 1.1;
}

.subtitle {
  max-width: 720px;
  color: #4b5563;
  font-size: 18px;
}

.section {
  margin-top: 28px;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
}

.category-grid a,
.item {
  display: block;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #ffffff;
  color: #111827;
  text-decoration: none;
}

.item-list {
  display: grid;
  gap: 12px;
}

.item-category {
  color: #2563eb;
  font-size: 13px;
  font-weight: 700;
}

.item p {
  color: #4b5563;
}
</style>
