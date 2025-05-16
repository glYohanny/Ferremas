import axios from 'axios';
import { API_BASE_URL } from './config'; // Asegúrate que esta ruta sea correcta

export const getRegiones = async () => {
  try {
    // Asume un endpoint como /api/regiones/ en tu backend
    const response = await axios.get(`${API_BASE_URL}/geografia/regiones/`);
    // Espera un array de objetos: [{id: 1, nombre: "Región Metropolitana"}, ...]
    return response.data.results || response.data; // Ajusta según la estructura de tu API (si usa paginación o no)
  } catch (error) {
    console.error("Error al cargar las regiones:", error.response?.data || error.message);
    throw error.response?.data || new Error('Error al cargar las regiones.');
  }
};

export const getComunas = async (regionId = null) => {
  try {
    let url = `${API_BASE_URL}/geografia/comunas/`;
    if (regionId) {
      // Asume que tu API puede filtrar comunas por un parámetro, ej: /api/comunas/?region=1
      // El nombre del parámetro (ej: 'region', 'region_id') dependerá de tu backend.
      url += `?region=${regionId}`; 
    }
    const response = await axios.get(url);
    // Espera un array de objetos: [{id: 1, nombre: "Santiago", region: 1 (o region_id: 1)}, ...]
    return response.data.results || response.data; // Ajusta según la estructura de tu API
  } catch (error) {
    console.error("Error al cargar las comunas:", error.response?.data || error.message);
    throw error.response?.data || new Error('Error al cargar las comunas.');
  }
};