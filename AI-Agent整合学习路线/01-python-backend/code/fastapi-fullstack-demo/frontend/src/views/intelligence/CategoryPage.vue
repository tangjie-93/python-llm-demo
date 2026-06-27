<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { fetchContents } from '@/api/intelligence';
import type { ContentItem } from '@/types/intelligence';

const route = useRoute();
const items = ref<ContentItem[]>([]);

async function load() {
  items.value = await fetchContents(String(route.params.category));
}

onMounted(load);
watch(() => route.params.category, load);
</script>

<template>
  <section>
    <h1>{{ route.params.category }}</h1>
    <div class="item-list">
      <RouterLink v-for="item in items" :key="item.id" class="item" :to="`/contents/${item.id}`">
        <strong>{{ item.title }}</strong>
        <p>{{ item.summary }}</p>
        <span>{{ item.source_name }}</span>
      </RouterLink>
    </div>
  </section>
</template>

<style scoped>
.item-list {
  display: grid;
  gap: 12px;
}

.item {
  display: block;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #ffffff;
  color: #111827;
  text-decoration: none;
}

.item p,
.item span {
  color: #4b5563;
}
</style>
