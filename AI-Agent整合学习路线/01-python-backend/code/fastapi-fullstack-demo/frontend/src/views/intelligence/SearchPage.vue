<script setup lang="ts">
import { ref } from 'vue';
import { askIntelligence, searchIntelligence } from '@/api/intelligence';
import type { AskResponse, SearchResult } from '@/types/intelligence';

const query = ref('');
const results = ref<SearchResult[]>([]);
const answer = ref<AskResponse | null>(null);

async function runSearch() {
  if (!query.value.trim()) return;
  results.value = await searchIntelligence(query.value);
  answer.value = await askIntelligence(query.value);
}
</script>

<template>
  <section>
    <h1>搜索与问答</h1>
    <div class="search-row">
      <el-input v-model="query" placeholder="搜索 Agent、RAG、MCP 等主题" @keyup.enter="runSearch" />
      <el-button type="primary" @click="runSearch">搜索</el-button>
    </div>

    <section v-if="answer" class="answer">
      <h2>回答</h2>
      <p>{{ answer.answer }}</p>
      <ul>
        <li v-for="citation in answer.citations" :key="`${citation.source_type}-${citation.id}`">
          {{ citation.title }}：{{ citation.excerpt }}
        </li>
      </ul>
    </section>

    <section class="results">
      <h2>搜索结果</h2>
      <div v-for="result in results" :key="`${result.result_type}-${result.id}`" class="result">
        <strong>{{ result.title }}</strong>
        <p>{{ result.summary }}</p>
      </div>
    </section>
  </section>
</template>

<style scoped>
.search-row {
  display: flex;
  gap: 12px;
}

.answer,
.result {
  margin-top: 18px;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #ffffff;
}
</style>
