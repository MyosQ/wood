import { CONFIG } from './config';

const API_BASE_URL = CONFIG.api.baseUrl;

export interface ApiError {
  detail: string;
  type?: string;
  status_code?: number;
}

export class ApiException extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public errorType?: string
  ) {
    super(message);
    this.name = 'ApiException';
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let errorMessage = `API request failed: ${response.statusText}`;
    let errorType: string | undefined;

    try {
      const errorData: ApiError = await response.json();
      errorMessage = errorData.detail || errorMessage;
      errorType = errorData.type;
    } catch {
      // If parsing error response fails, use default message
    }

    throw new ApiException(errorMessage, response.status, errorType);
  }

  return response.json();
}

export async function apiRequest<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    return await handleResponse<T>(response);
  } catch (error) {
    if (error instanceof ApiException) {
      throw error;
    }
    // Network or other errors
    throw new ApiException(
      error instanceof Error ? error.message : 'Network error',
      0,
      'network_error'
    );
  }
}

export async function get<T>(endpoint: string): Promise<T> {
  return apiRequest<T>(endpoint, { method: 'GET' });
}

export async function post<T>(endpoint: string, data: unknown): Promise<T> {
  return apiRequest<T>(endpoint, {
    method: 'POST',
    body: JSON.stringify(data),
  });
}
