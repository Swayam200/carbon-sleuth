import axios from 'axios';

const api = axios.create({
  // Use relative path so requests go to the same domain (Vercel),
  // hitting the 'rewrites' rule in vercel.json which proxies to VPS.
  baseURL: '/api',
});

export default api;
