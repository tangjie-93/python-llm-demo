import api from '@/utils/api';
import type { AskResponse, ContentItem, DailyBrief, HomeData, SearchResult } from '@/types/intelligence';

export function fetchIntelligenceHome() {
  return api.get<HomeData>('/intelligence/home');
}

export function fetchCategories() {
  return api.get<string[]>('/intelligence/categories');
}

export function fetchContents(category?: string) {
  return api.get<ContentItem[]>('/intelligence/contents', {
    params: category ? { category } : {}
  });
}

export function fetchContentDetail(id: string | number) {
  return api.get<ContentItem | null>(`/intelligence/contents/${id}`);
}

export function fetchBriefs() {
  return api.get<DailyBrief[]>('/intelligence/briefs');
}

export function searchIntelligence(q: string) {
  return api.get<SearchResult[]>('/intelligence/search', { params: { q } });
}

export function askIntelligence(q: string) {
  return api.get<AskResponse>('/intelligence/ask', { params: { q } });
}
