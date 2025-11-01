/**
 * API Client for Fintech AI Backend
 * Communicates with FastAPI backend at http://localhost:8000
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds for analysis requests
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      console.error('API Error:', error.response.data);
      throw new Error(error.response.data.error || 'API request failed');
    } else if (error.request) {
      // Request made but no response
      console.error('Network Error:', error.request);
      throw new Error('Cannot connect to backend. Please ensure the API server is running.');
    } else {
      // Something else happened
      console.error('Error:', error.message);
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
