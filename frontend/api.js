// src/services/api.js
import axios from 'axios';

const API = axios.create({
  baseURL: 'https://daniexc.onrender.com',
});

export const getCandidates = () => API.get('/candidates');
export const addCandidate = (data) => API.post('/candidates', data);
