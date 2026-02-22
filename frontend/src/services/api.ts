/**
 * API client service with authentication interceptors.
 *
 * Provides a configured axios instance for making authenticated API requests.
 */

import axios, { AxiosInstance, AxiosRequestConfig, AxiosError } from 'axios';

// API base URL from environment
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Token provider function type
type TokenProvider = () => Promise<string | null>;

class ApiClient {
  private client: AxiosInstance;
  private tokenProvider: TokenProvider | null = null;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000, // 30 second timeout
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  /**
   * Set the token provider function for authentication.
   * Should be called after AuthContext is initialized.
   */
  setTokenProvider(provider: TokenProvider): void {
    this.tokenProvider = provider;
  }

  /**
   * Setup request and response interceptors.
   */
  private setupInterceptors(): void {
    // Request interceptor: Add authentication token
    this.client.interceptors.request.use(
      async config => {
        if (this.tokenProvider) {
          const token = await this.tokenProvider();
          if (token) {
            config.headers.Authorization = `Bearer ${token}`;
          }
        }
        return config;
      },
      error => {
        return Promise.reject(error);
      }
    );

    // Response interceptor: Handle errors
    this.client.interceptors.response.use(
      response => response,
      (error: AxiosError) => {
        if (error.response) {
          // Server responded with error status
          const { status, data } = error.response;

          if (status === 401) {
            // Unauthorized - token expired or invalid
            console.error('Authentication failed:', data);
            // Could trigger logout or token refresh here
          } else if (status === 403) {
            // Forbidden
            console.error('Access forbidden:', data);
          } else if (status === 404) {
            // Not found
            console.error('Resource not found:', data);
          } else if (status >= 500) {
            // Server error
            console.error('Server error:', data);
          }
        } else if (error.request) {
          // Request made but no response
          console.error('No response from server:', error.request);
        } else {
          // Error setting up request
          console.error('Request setup error:', error.message);
        }

        return Promise.reject(error);
      }
    );
  }

  /**
   * Generic GET request
   */
  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.get<T>(url, config);
    return response.data;
  }

  /**
   * Generic POST request
   */
  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.post<T>(url, data, config);
    return response.data;
  }

  /**
   * Generic PUT request
   */
  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.put<T>(url, data, config);
    return response.data;
  }

  /**
   * Generic PATCH request
   */
  async patch<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.patch<T>(url, data, config);
    return response.data;
  }

  /**
   * Generic DELETE request
   */
  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.delete<T>(url, config);
    return response.data;
  }
}

// Export singleton instance
export const apiClient = new ApiClient();
export default apiClient;
