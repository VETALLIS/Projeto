import axios from 'axios';

const api = axios.create({
  baseURL: 'http://10.135.60.25:3000/api', // Substitua pelo seu IP Local
});

export default api;