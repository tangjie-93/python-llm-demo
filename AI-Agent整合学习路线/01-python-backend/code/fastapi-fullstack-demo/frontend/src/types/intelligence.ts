export interface ContentItem {
  id: number;
  title: string;
  url: string;
  source_name: string;
  published_at: string | null;
  summary: string;
  key_points: string[];
  category: string;
  tags: string[];
  importance: number;
  reason: string;
}

export interface DailyBrief {
  id: number;
  brief_date: string;
  title: string;
  summary: string;
  sections: Array<{
    category: string;
    items: Array<{
      id: number;
      title: string;
      summary: string;
      url: string;
      tags: string[];
      importance: number;
      reason: string;
    }>;
  }>;
  generated_at: string;
}

export interface HomeData {
  latest_items: ContentItem[];
  brief: DailyBrief | null;
  categories: string[];
}

export interface SearchResult {
  result_type: string;
  id: number;
  title: string;
  summary: string;
  category: string;
  tags: string[];
  source: string;
}

export interface AskResponse {
  answer: string;
  refused: boolean;
  citations: Array<{
    source_type: string;
    id: number;
    title: string;
    excerpt: string;
  }>;
}
