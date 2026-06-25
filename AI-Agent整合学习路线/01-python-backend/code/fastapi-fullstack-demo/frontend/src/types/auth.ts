export interface BaseResponse<T> {
  data: T | null;
  message: string;
  success: boolean;
  details?: string | null;
  error?: string | null;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface ApiError {
  success: false
  message: string
  error?: string
  detail?: string
  details?: any
  data?: any
}