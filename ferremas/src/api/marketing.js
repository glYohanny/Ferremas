import axios from 'axios';

// Ajusta esta URL base para que coincida con los endpoints de tu marketing_app
const apiClient = axios.create({
    baseURL: 'http://localhost:8000/api/marketing/', // Ejemplo
    // headers: {
    //   'Authorization': `Bearer ${localStorage.getItem('token')}`
    // }
});

export const getPromociones = () => apiClient.get('/promociones/');
export const getNotificaciones = () => apiClient.get('/notificaciones/');

export default apiClient;