export interface BaseResponse<T> {
  data: T | null;
  message: string;
  success: boolean;
  details?: string | null;
  error?: string | null;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface ApiError {
  success: false
  message: string
  error?: string
  detail?: string
  details?: any
  data?: any
}