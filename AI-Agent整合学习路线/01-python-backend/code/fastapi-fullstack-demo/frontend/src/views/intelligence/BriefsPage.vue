<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { fetchBriefs } from '@/api/intelligence';
import type { DailyBrief } from '@/types/intelligence';

const briefs = ref<DailyBrief[]>([]);

onMounted(async () => {
  briefs.value = await fetchBriefs();
});
</script>

<template>
  <section>
    <h1>每日简报</h1>
    <article v-for="brief in briefs" :key="brief.id" class="brief">
      <h2>{{ brief.title }}</h2>
      <p>{{ brief.summary }}</p>
      <section v-for="section in brief.sections" :key="section.category">
        <h3>{{ section.category }}</h3>
        <ul>
          <li v-for="item in section.items" :key="item.id">{{ item.title }}</li>
        </ul>
      </section>
    </article>
  </section>
</template>

<style scoped>
.brief {
  margin-bottom: 20px;
  padding: 18px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #ffffff;
}
</style>
