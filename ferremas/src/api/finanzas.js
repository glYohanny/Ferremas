import axios from 'axios';

// Ajusta esta URL base para que coincida con los endpoints de tu finanzas_app
const apiClient = axios.create({
    baseURL: 'http://localhost:8000/api/finanzas/', // Ejemplo
    // headers: {
    //   'Authorization': `Bearer ${localStorage.getItem('token')}` // Si requiere autenticación
    // }
});

export const getTiposCambio = () => apiClient.get('/tipos-cambio/'); // Ejemplo

export default apiClient;