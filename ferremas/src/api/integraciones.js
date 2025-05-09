import axios from 'axios';

// Ajusta esta URL base para que coincida con los endpoints de tu integraciones_app
const apiClient = axios.create({
    baseURL: 'http://localhost:8000/api/integraciones/', // Ejemplo
    // headers: {
    //   'Authorization': `Bearer ${localStorage.getItem('token')}` // Si requiere autenticación
    // }
});

export const getApiLogs = () => apiClient.get('/api-logs/'); // Ejemplo

export default apiClient;