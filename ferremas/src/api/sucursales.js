import apiClient from './cliente'; // Importar apiClient en lugar de axios
import { API_BASE_URL } from './config'; 
// Ya no se necesita getAuthHeaders si usamos apiClient

/**
 * Obtiene la lista de todas las sucursales.
 */
export const obtenerSucursales = async () => {
  try {
    // Usar apiClient. La URL es relativa a API_BASE_URL configurada en apiClient.
    const response = await apiClient.get(`/sucursales/sucursal/`);
    return response.data.results || response.data;
  } catch (error) {
    console.error("Error al obtener sucursales:", error.response || error);
    throw new Error(error.response?.data?.detail || 'No se pudieron cargar las sucursales.');
  }
};