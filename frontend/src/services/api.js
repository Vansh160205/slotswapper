import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  signup: (data) => api.post('/auth/signup', data),
  login: (data) => api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
};

// Events API
export const eventsAPI = {
  getMyEvents: () => api.get('/events'),
  createEvent: (data) => api.post('/events', data),
  updateEvent: (id, data) => api.put(`/events/${id}`, data),
  deleteEvent: (id) => api.delete(`/events/${id}`),
  getSwappableSlots: () => api.get('/swappable-slots'),
};

// Swap API
export const swapAPI = {
  createSwapRequest: (data) => api.post('/swap-request', data),
  respondToSwap: (id, accept) => api.post(`/swap-response/${id}`, { accept }),
  getIncomingRequests: () => api.get('/swap-requests/incoming'),
  getOutgoingRequests: () => api.get('/swap-requests/outgoing'),
  cancelSwapRequest: (id) => api.delete(`/swap-request/${id}`),
};

export default api;