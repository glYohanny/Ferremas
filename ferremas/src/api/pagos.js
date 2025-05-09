import axios from 'axios';

// Ajusta esta URL base para que coincida con los endpoints de tu pagos_app
const apiClient = axios.create({
    baseURL: 'http://localhost:8000/api/pagos/', // Ejemplo
    // headers: {
    //   'Authorization': `Bearer ${localStorage.getItem('token')}`
    // }
});

export const getMetodosPago = () => apiClient.get('/metodos-pago/');
export const createTransaccion = (data) => apiClient.post('/transacciones/', data); // Ejemplo

export default apiClient;