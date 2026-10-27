import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
    withCredentials: true, // Essential for sending session cookies
});

export const portfolioApi = {
    // Private endpoints
    create: (data: any) => api.post('/portfolios/', data),
    list: () => api.get('/portfolios/'),
    update: (id: string, data: any) => api.put(`/portfolios/${id}`, data),
    addProject: (id: string, data: any) => api.post(`/portfolios/${id}/projects`, data),
    
    // Public endpoints
    getPublic: (slug: string) => api.get(`/portfolio/${slug}`),
    getPublicProjects: (slug: string) => api.get(`/portfolio/${slug}/projects`),
};

export default api;
