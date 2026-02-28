import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
  timeout: 30000,
});

export const studyAPI = {
  generatePlan: (data) => api.post('/study/plan', data),
  getSample:    ()     => api.get('/study/sample'),
};

export const budgetAPI = {
  analyze:   (data) => api.post('/budget/analyze', data),
  getSample: ()     => api.get('/budget/sample'),
};

export const healthAPI = {
  check: () => api.get('/health'),
};

export const chatAPI = {
  ask:       (data) => api.post('/chat/ask', data),
  getTopics: ()     => api.get('/chat/topics'),
};

export default api;
