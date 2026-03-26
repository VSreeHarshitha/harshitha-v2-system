import axios from 'axios';

const API_URL = "http://localhost:8000";

const api = axios.create({
  baseURL: API_URL,
});

// This "Interceptor" grabs the key from your browser's memory
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('x-admin-key');
  if (token) {
    config.headers['x-admin-key'] = token;
  }
  return config;
});

export default api;