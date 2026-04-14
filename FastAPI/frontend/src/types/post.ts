export interface Post {
  id: number;
  title: string;
  content: string;
  summary: string | null;
  author_id: number;
  is_published: boolean;
  view_count: number;
  created_at: string;
  updated_at: string;
  author?: PostAuthor;
  tags?: Tag[];
}

export interface PostAuthor {
  id: number;
  username: string;
  full_name: string | null;
}

export interface PostSimple {
  id: number;
  title: string;
  summary: string | null;
  author_id: number;
  is_published: boolean;
  view_count: number;
  created_at: string;
  updated_at: string;
  tags?: Tag[];
}

export interface Tag {
  id: number;
  name: string;
  description: string | null;
  created_at: string;
}

export interface TagWithPosts extends Tag {
  posts?: PostSimple[];
}

export interface CreatePostData {
  title: string;
  content: string;
  summary?: string;
  is_published?: boolean;
  tag_ids?: number[];
}

export interface UpdatePostData {
  title?: string;
  content?: string;
  summary?: string;
  is_published?: boolean;
  tag_ids?: number[];
}

export interface CreateTagData {
  name: string;
  description?: string;
}

export interface UpdateTagData {
  name?: string;
  description?: string;
}

export interface PostFilterParams {
  skip?: number;
  limit?: number;
  is_published?: boolean;
  author_id?: number;
  tag_id?: number;
}

export interface PaginationParams {
  page: number;
  limit: number;
  total: number;
}
