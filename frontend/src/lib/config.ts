/**
 * Application configuration constants
 *
 * Centralized configuration for the frontend application.
 */

/**
 * Application configuration
 */
export const CONFIG = {
  /**
   * API configuration
   */
  api: {
    /**
     * Base URL for the backend API
     * Defaults to localhost for development
     */
    baseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',

    /**
     * Request timeout in milliseconds
     */
    timeout: 30000,

    /**
     * Number of retry attempts for failed requests
     */
    retryAttempts: 3,

    /**
     * Delay between retry attempts in milliseconds
     */
    retryDelay: 1000,
  },

  /**
   * Feature flags
   */
  features: {
    /**
     * Enable error tracking (e.g., Sentry)
     */
    enableErrorTracking: import.meta.env.VITE_ENABLE_ERROR_TRACKING === 'true',

    /**
     * Enable debug mode
     */
    debug: import.meta.env.MODE === 'development',
  },

  /**
   * Application metadata
   */
  app: {
    name: 'Skogsstyrelsen API Gateway',
    version: '0.1.0',
  },
} as const;
