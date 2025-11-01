/**
 * API Client for Fintech AI Backend
 * Communicates with FastAPI backend at http://localhost:8000
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

console.log('🔗 API Base URL:', API_BASE_URL);

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds for analysis requests
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for debugging
apiClient.interceptors.request.use(
  (config) => {
    console.log('📤 API Request:', {
      method: config.method?.toUpperCase(),
      url: config.url,
      baseURL: config.baseURL,
      fullURL: `${config.baseURL}${config.url}`,
      data: config.data,
      params: config.params
    });
    return config;
  },
  (error) => {
    console.error('❌ Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log('📥 API Response:', {
      status: response.status,
      statusText: response.statusText,
      data: response.data,
      url: response.config.url
    });
    return response;
  },
  (error) => {
    console.error('❌ API Error Details:', {
      message: error.message,
      code: error.code,
      response: error.response ? {
        status: error.response.status,
        statusText: error.response.statusText,
        data: error.response.data
      } : 'No response',
      request: error.request ? 'Request was made but no response received' : 'No request made',
      config: {
        url: error.config?.url,
        method: error.config?.method,
        baseURL: error.config?.baseURL
      }
    });

    if (error.response) {
      // Server responded with error status (4xx, 5xx)
      const errorMessage = error.response.data?.error ||
                          error.response.data?.message ||
                          error.response.statusText ||
                          'API request failed';
      console.error('🚨 Server Error:', errorMessage);
      throw new Error(errorMessage);
    } else if (error.request) {
      // Request made but no response
      console.error('🚨 Network Error: No response from server');
      throw new Error(`Cannot connect to backend at ${API_BASE_URL}. Please ensure the API server is running on port 8000.`);
    } else {
      // Something else happened
      console.error('🚨 Unknown Error:', error.message);
      throw error;
    }
  }
);

/**
 * Check API health status
 * @returns {Promise<Object>} Health status data
 */
export const checkHealth = async () => {
  const response = await apiClient.get('/health');
  return response.data;
};

/**
 * Analyze a company by ticker
 * @param {string} ticker - Stock ticker symbol (e.g., 'AAPL')
 * @returns {Promise<Object>} Analysis results
 */
export const analyzeCompany = async (ticker) => {
  const response = await apiClient.post('/analyze', { ticker });
  return response.data;
};

/**
 * Get recent analyses
 * @param {number} limit - Number of results to return (default: 10)
 * @returns {Promise<Object>} Recent analyses
 */
export const getRecentAnalyses = async (limit = 10) => {
  const response = await apiClient.get('/recent', { params: { limit } });
  return response.data;
};

/**
 * Get all companies in database
 * @returns {Promise<Object>} List of companies
 */
export const getCompanies = async () => {
  const response = await apiClient.get('/companies');
  return response.data;
};

/**
 * Get company details by ticker
 * @param {string} ticker - Stock ticker symbol
 * @param {number} limit - Number of analyses to return (default: 5)
 * @returns {Promise<Object>} Company details and analyses
 */
export const getCompanyDetails = async (ticker, limit = 5) => {
  const response = await apiClient.get(`/company/${ticker}`, { params: { limit } });
  return response.data;
};

/**
 * Get database statistics
 * @returns {Promise<Object>} Database stats
 */
export const getStats = async () => {
  const response = await apiClient.get('/stats');
  return response.data;
};

/**
 * Get API information
 * @returns {Promise<Object>} API info
 */
export const getApiInfo = async () => {
  const response = await apiClient.get('/');
  return response.data;
};

// Export default client for custom requests
export default apiClient;
