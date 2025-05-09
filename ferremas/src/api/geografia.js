import axios from 'axios';

// Ajusta esta URL base para que coincida con los endpoints de tu geografia_app
const apiClient = axios.create({
    baseURL: 'http://localhost:8000/api/geografia/', // Ejemplo
    // headers: {
    //   'Authorization': `Bearer ${localStorage.getItem('token')}`
    // }
});

export const getRegiones = () => apiClient.get('/regiones/');
export const getComunasByRegion = (regionId) => apiClient.get(`/comunas/?region=${regionId}`); // Ejemplo de filtro

export default apiClient;