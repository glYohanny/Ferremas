import axios from 'axios';
import { API_BASE_URL } from './config'; 
import { getAuthHeaders } from './autentificacion'; // Importar desde autenticacion.js

/**
 * Obtiene la lista de todas las sucursales.
 */
export const obtenerSucursales = async () => {
  try {
    // Asegúrate que el endpoint '/sucursales/sucursal/' sea el correcto según tu API de Django
    const response = await axios.get(`${API_BASE_URL}/sucursales/sucursal/`, { headers: getAuthHeaders() });
    // Ajusta según la estructura de tu respuesta, DRF con paginación usualmente tiene 'results'
    return response.data.results || response.data;
  } catch (error) {
    console.error("Error al obtener sucursales:", error.response || error);
    throw new Error(error.response?.data?.detail || 'No se pudieron cargar las sucursales.');
  }
};