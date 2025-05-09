import axios from 'axios';

// Ajusta esta URL base para que coincida con los endpoints de tu inventario_app
const apiClient = axios.create({
    baseURL: 'http://localhost:8000/api/inventario/', // Ejemplo
    // headers: {
    //   'Authorization': `Bearer ${localStorage.getItem('token')}`
    // }
});

export const getInventario = () => apiClient.get('/'); // Asumiendo que /inventario/ es el endpoint principal
export const getHistorialStock = (productoId) => apiClient.get(`/historial-stock/?producto=${productoId}`); // Ejemplo

export default apiClient;