import axios from 'axios';
import { API_BASE_URL } from './config'; // Asumiendo que tienes tu URL base configurada

// No necesitas getAuthHeaders aquí si los endpoints son públicos (AllowAny)

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  // No se añaden headers de autenticación por defecto si son públicos
});

export const obtenerProductos = async (queryParams = {}) => { // Renombrado el parámetro para mayor claridad
  try {
    const urlPath = '/productos/producto';
    console.log('[productos.js] Intentando obtener productos de:', `${apiClient.defaults.baseURL}${urlPath}`, 'con parámetros:', queryParams);

    const response = await apiClient.get(urlPath, { params: queryParams }); // Pasar queryParams bajo la clave 'params'
    return response.data; // DRF ViewSet usualmente devuelve { count, next, previous, results } para listas
  } catch (error) {
    console.error("Error al obtener productos:", error.response || error);
    throw error.response?.data || new Error('Error al obtener productos');
  }
};

export const obtenerProductoPorId = async (productoId) => {
  try {
    // Si API_BASE_URL es 'http://localhost:8000/api',
    // la URL correcta relativa es `/productos/${productoId}/`.
    const urlPath = `/productos/producto/${productoId}/`;
    console.log('[productos.js] Intentando obtener producto por ID de:', `${apiClient.defaults.baseURL}${urlPath}`);
    const response = await apiClient.get(urlPath);
    return response.data;
  } catch (error) {
    console.error(`Error al obtener producto ${productoId}:`, error.response || error);
    throw error.response?.data || new Error(`Error al obtener producto ${productoId}`);
  }
};

// Podrías añadir obtenerCategorias si lo necesitas explícitamente,
// aunque a menudo la categoría viene anidada en el producto.
// export const obtenerCategorias = async () => { ... }