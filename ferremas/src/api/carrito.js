import axios from 'axios';

// Ajusta esta URL base para que coincida con los endpoints de tu carrito_app
const apiClient = axios.create({
    baseURL: 'http://localhost:8000/api/carrito/', // Ejemplo
    // headers: {
    //   'Authorization': `Bearer ${localStorage.getItem('token')}` // El carrito usualmente requiere autenticación
    // }
});

export const getCarrito = () => apiClient.get('/'); // Asumiendo que el usuario solo tiene un carrito accesible en /
export const addItemToCarrito = (data) => apiClient.post('/items/', data); // Ejemplo para añadir items

export default apiClient;