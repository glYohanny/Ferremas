import axios from 'axios';

// Ajusta esta URL base para que coincida con los endpoints de tu sucursales_app
const apiClient = axios.create({
    baseURL: 'http://localhost:8000/api/sucursales/', // Ejemplo
    // headers: {
    //   'Authorization': `Bearer ${localStorage.getItem('token')}`
    // }
});

export const getSucursales = () => apiClient.get('/');
export const getBodegasBySucursal = (sucursalId) => apiClient.get(`/bodegas/?sucursal=${sucursalId}`); // Ejemplo

export default apiClient;