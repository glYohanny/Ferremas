import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/geografia/'; // Ajusta si tu URL base es diferente

/**
 * Obtiene la lista de todas las comunas.
 */
export const getComunas = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}comunas/`);
    // La API de DRF con paginación devuelve los resultados en response.data.results
    // Si no usas paginación o es un ReadOnlyModelViewSet simple, podría ser solo response.data
    return response.data.results || response.data; 
  } catch (error) {
    console.error('Error al obtener las comunas:', error.response ? error.response.data : error.message);
    throw error; // Relanzar para que el componente pueda manejarlo
  }
};