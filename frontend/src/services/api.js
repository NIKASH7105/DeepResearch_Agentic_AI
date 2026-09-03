import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Research APIs
export const researchApi = {
  // Start a new research session
  startResearch: async (data) => {
    const response = await api.post('/research/start', data);
    return response.data;
  },

  // Get research session details
  getSession: async (sessionId) => {
    const response = await api.get(`/research/${sessionId}`);
    return response.data;
  },

  // Get research status
  getStatus: async (sessionId) => {
    const response = await api.get(`/research/${sessionId}/status`);
    return response.data;
  },

  // Get research sources
  getSources: async (sessionId) => {
    const response = await api.get(`/research/${sessionId}/sources`);
    return response.data;
  },

  // Get research report
  getReport: async (sessionId) => {
    const response = await api.get(`/research/${sessionId}/report`);
    return response.data;
  },

  // List all research sessions
  listSessions: async () => {
    const response = await api.get('/research/');
    return response.data;
  },
};

// Health check
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;
