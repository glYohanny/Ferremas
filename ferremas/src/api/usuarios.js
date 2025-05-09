import axios from 'axios';

// Ajusta esta URL base para que coincida con los endpoints de tu usuarios_app
const apiClient = axios.create({
    baseURL: 'http://localhost:8000/api/usuarios/', // Ejemplo
    // headers: {
    //   'Authorization': `Bearer ${localStorage.getItem('token')}`
    // }
});

export const getUsuarios = () => apiClient.get('/');
export const getUsuarioById = (id) => apiClient.get(`/${id}/`);
export const createUsuario = (data) => apiClient.post('/', data);
export const updateUsuario = (id, data) => apiClient.put(`/${id}/`, data);
export const deleteUsuario = (id) => apiClient.delete(`/${id}/`);
// Añade funciones específicas para roles, clientes, personal, etc., si es necesario

export default apiClient;