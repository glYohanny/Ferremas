import { API_BASE_URL } from './config'; // Importación nombrada
import apiClient from './cliente'; // Importar tu cliente Axios configurado

/**
 * Actualiza el perfil del usuario autenticado.
 * @param {object} profileData - Datos del perfil a actualizar (ej. { first_name, last_name }).
 */
export const actualizarPerfilUsuario = async (profileData) => {
  try {
    // El endpoint '/usuarios/me/' es común para el perfil del usuario actual.
    // DRF podría usar PATCH para actualizaciones parciales o PUT para completas.
    // Usaremos PATCH aquí, asumiendo que solo envías los campos que cambian.
    // La URL completa será construida por apiClient usando su baseURL y la ruta relativa.
    // Si tu backend usa /api/usuarios/me/, cambia la siguiente línea:
     const response = await apiClient.patch('/usuarios/usuario/me/', profileData); 
    return response.data; // Devuelve los datos del usuario actualizados desde el backend
  } catch (error) {
    console.error("Error al actualizar el perfil del usuario:", error.response?.data || error.message);
    const errorMessage = error.response?.data?.detail || 
                         (error.response?.data && typeof error.response.data === 'object' ? JSON.stringify(error.response.data) : null) ||
                         error.message || 
                         'Error desconocido al actualizar el perfil.';
    throw new Error(errorMessage);
  }
};