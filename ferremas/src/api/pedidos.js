import axios from 'axios';

// Ajusta esta URL base para que coincida con los endpoints de tu pedidos_app
const apiClient = axios.create({
    baseURL: 'http://localhost:8000/api/pedidos/', // Ejemplo
    // headers: {
    //   'Authorization': `Bearer ${localStorage.getItem('token')}`
    // }
});

export const getPedidos = () => apiClient.get('/');
export const createPedido = (data) => apiClient.post('/', data);
export const getPedidoById = (id) => apiClient.get(`/${id}/`);
// Añade funciones para detalles de pedido, estados, etc.

export default apiClient;