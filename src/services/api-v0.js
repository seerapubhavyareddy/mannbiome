// services/api.js - Updated with Clinical Trials method
// const API_BASE_URL = 'https://yd3weja3cp.us-east-2.awsapprunner.com';
const API_BASE_URL = 'https://gnss5bq5km.us-east-2.awsapprunner.com';

// const API_BASE_URL = 'http://localhost:8001';
class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      console.log(`🔍 API Request: ${config.method || 'GET'} ${url}`);
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log(`✅ API Response:`, data);
      return data;
    } catch (error) {
      console.error(`❌ API request failed: ${endpoint}`, error);
      throw error;
    }
  }

  // Health check
  async healthCheck() {
    return this.request('/api/health-check');
  }

  // User methods
  async getUserProfile(userId) {
    return this.request(`/api/user/${userId}/profile`);
  }

  // Customer methods
  async getCustomerMicrobiomeData(customerId) {
    return this.request(`/api/customer/${customerId}/microbiome-data`);
  }

  async getCustomerDashboardData(customerId) {
    return this.request(`/api/customer/${customerId}/dashboard-data`);
  }

  // Health domain details
  async getHealthDomainDetails(domainId, customerId = null) {
    const endpoint = customerId 
      ? `/api/health-domains/${domainId}/details?customer_id=${customerId}`
      : `/api/health-domains/${domainId}/details`;
    return this.request(endpoint);
  }

  // Clinical trials methods
  async getClinicalTrials(filters = {}) {
    const params = new URLSearchParams();
    
    if (filters.search) params.append('search', filters.search);
    if (filters.category && filters.category !== 'all') params.append('category', filters.category);
    if (filters.status && filters.status !== 'all') params.append('status', filters.status);
    if (filters.phase && filters.phase !== 'all') params.append('phase', filters.phase);
    
    const queryString = params.toString();
    const endpoint = `/api/clinical-trials${queryString ? `?${queryString}` : ''}`;
    
    return this.request(endpoint);
  }

  // ============================================
  // NEW MODAL DATA METHODS - PROPERLY FORMATTED
  // ============================================

  /**
   * Get detailed modal data for a health domain
   * @param {number} domainId - Domain ID (1=gut, 2=liver, 3=heart, 4=skin, 5=cognitive, 6=aging)
   * @param {number} customerId - Customer ID
   * @returns {Promise} - Modal data including health metrics, species, pathways, recommendations
   */
  async getHealthDomainModalData(domainId, customerId) {
    const endpoint = `/api/health-domains/${domainId}/modal-data/${customerId}`;
    return this.request(endpoint);
  }

  /**
   * Get only species carousel data for a domain
   * @param {number} domainId - Domain ID
   * @param {number} customerId - Customer ID
   * @returns {Promise} - Species carousel data
   */
  async getSpeciesCarouselData(domainId, customerId) {
    const endpoint = `/api/health-domains/${domainId}/species-carousel/${customerId}`;
    return this.request(endpoint);
  }

  /**
   * Get only pathway carousel data for a domain
   * @param {number} domainId - Domain ID
   * @param {number} customerId - Customer ID
   * @returns {Promise} - Pathway carousel data
   */
  async getPathwayCarouselData(domainId, customerId) {
    const endpoint = `/api/health-domains/${domainId}/pathway-carousel/${customerId}`;
    return this.request(endpoint);
  }

  /**
   * Get only recommendations data for a domain
   * @param {number} domainId - Domain ID
   * @param {number} customerId - Customer ID
   * @returns {Promise} - Recommendations data
   */
  async getRecommendationsData(domainId, customerId) {
    const endpoint = `/api/health-domains/${domainId}/recommendations-only/${customerId}`;
    return this.request(endpoint);
  }

  // Add this method to your existing apiService class in services/api.js

/**
 * Get clinical trials for a specific health domain
 * @param {string} domainId - Domain ID (gut, liver, heart, skin, cognitive, aging)
 * @param {number} customerId - Customer ID for eligibility checking
 * @param {number} limit - Maximum number of trials to return (default: 5)
 * @returns {Promise} - Clinical trials data with eligibility
 */
async getDomainClinicalTrials(domainId, customerId, limit = 5) {
  const endpoint = `/api/health-domains/${domainId}/clinical-trials?customer_id=${customerId}&limit=${limit}`;
  return this.request(endpoint);
}

  // Test connection
  async testConnection() {
    try {
      const response = await this.healthCheck();
      return {
        connected: true,
        status: response.status,
        message: response.message || 'Connected successfully'
      };
    } catch (error) {
      return {
        connected: false,
        error: error.message,
        message: 'Failed to connect to API'
      };
    }
  }
}

// Create and export a singleton instance
const apiService = new ApiService();
export default apiService;