import axios from 'axios';
import { API_BASE_URL } from './config'; // Asegúrate que API_BASE_URL esté definida y exportada desde config.js

const getAuthHeaders = () => {
  const token = localStorage.getItem('accessToken') || sessionStorage.getItem('accessToken');
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export const obtenerUsuarios = async () => {
  try {
    // Ajusta la URL si tu endpoint de usuarios es diferente.
    // Usualmente, si tienes un UsuarioViewSet, la ruta sería algo como '/usuarios/usuarios/'
    // o simplemente '/usuarios/' si el router no añade el nombre del modelo.
    // Verifica tu backend: la ruta correcta es /api/usuarios/usuario/ (singular)
    const response = await axios.get(`${API_BASE_URL}/usuarios/usuario/`, { headers: getAuthHeaders() });
    return response.data;
  } catch (error) {
    console.error("Error al obtener usuarios:", error.response || error);
    let errorMessage = 'Error al cargar la lista de usuarios.';
    if (error.response && error.response.data && error.response.data.detail) {
      errorMessage = error.response.data.detail;
    } else if (error.response && typeof error.response.data === 'string' && error.response.data.length < 300) {
      errorMessage = error.response.data;
    } else if (error.response && error.response.data) {
      // Para errores de validación u otros errores estructurados
      const errorData = error.response.data;
      if (typeof errorData === 'object' && errorData !== null) {
        errorMessage = Object.keys(errorData)
          .map(key => `${key.replace("_", " ")}: ${Array.isArray(errorData[key]) ? errorData[key].join(', ') : errorData[key]}`)
          .join('\n');
        if (!errorMessage.trim()) errorMessage = "Error procesando la solicitud.";
      } else {
        errorMessage = `Error del servidor (código: ${error.response.status}).`;
      }
    } else if (error.request) {
      errorMessage = 'No se pudo conectar con el servidor.';
    } else {
      errorMessage = error.message;
    }
    throw new Error(errorMessage);
  }
};

export const crearUsuarioAdmin = async (userData) => {
  try {
    // Ajusta la URL si tu endpoint para crear usuarios por admin es diferente.
    // Podría ser algo como '/usuarios/admin/crear/' o similar.
    const response = await axios.post(`${API_BASE_URL}/usuarios/usuario/`, userData, { headers: getAuthHeaders() });
    return response.data;
  } catch (error) {
    console.error("Error al crear usuario:", error.response || error);
    let errorMessage = 'Error al crear el usuario.';
     if (error.response && error.response.data) {
      const errorData = error.response.data;
      if (error.response.status === 500) {
        errorMessage = "Ocurrió un error inesperado en el servidor al crear el usuario.";
      } else if (typeof errorData === 'object' && errorData !== null) {
        errorMessage = Object.keys(errorData)
          .map(key => `${key.replace("_", " ")}: ${Array.isArray(errorData[key]) ? errorData[key].join(', ') : errorData[key]}`)
          .join('\n');
        if (!errorMessage.trim()) errorMessage = errorData.detail || "Error en los datos enviados para crear el usuario.";
      } else if (typeof errorData === 'string' && errorData.length < 300) {
        errorMessage = errorData;
      } else {
        errorMessage = `Error del servidor (código: ${error.response.status}) al crear el usuario.`;
      }
    } else if (error.request) {
      errorMessage = 'No se pudo conectar con el servidor para crear el usuario.';
    } else {
      errorMessage = error.message;
    }
    throw new Error(errorMessage);
  }
};

export const obtenerRoles = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/usuarios/roles/`, { headers: getAuthHeaders() });
    return response.data.results || response.data; // Maneja paginación si existe
  } catch (error) {
    console.error("Error al obtener roles:", error.response || error);
    // Podrías tener un manejo de errores similar al de obtenerUsuarios si es necesario
    throw new Error(error.response?.data?.detail || 'No se pudieron cargar los roles.');
  }
};


export const eliminarUsuario = async (userId) => {
  try {
    // El endpoint para eliminar un usuario específico suele ser /usuarios/usuario/{id}/
    await axios.delete(`${API_BASE_URL}/usuarios/usuario/${userId}/`, { headers: getAuthHeaders() });
    // No se devuelve nada en una eliminación exitosa (status 204)
  } catch (error) {
    console.error(`Error al eliminar usuario ${userId}:`, error.response || error);
    let errorMessage = 'Error al eliminar el usuario.';
    if (error.response && error.response.data) {
      errorMessage = error.response.data.detail || (typeof error.response.data === 'string' ? error.response.data : JSON.stringify(error.response.data));
    } else if (error.request) {
      errorMessage = 'No se pudo conectar con el servidor.';
    } else {
      errorMessage = error.message;
    }
    throw new Error(errorMessage);
  }
};

export const actualizarEstadoUsuario = async (userId, isActive) => {
  try {
    // Para actualizar solo el estado, se usa PATCH.
    // El endpoint es el mismo que para obtener/actualizar un usuario.
    const response = await axios.patch(`${API_BASE_URL}/usuarios/usuario/${userId}/`, { is_active: isActive }, { headers: getAuthHeaders() });
    return response.data;
  } catch (error) {
    console.error(`Error al actualizar estado del usuario ${userId}:`, error.response || error);
    let errorMessage = 'Error al actualizar el estado del usuario.';
     if (error.response && error.response.data) {
      errorMessage = error.response.data.detail || (typeof error.response.data === 'string' ? error.response.data : JSON.stringify(error.response.data));
    } else if (error.request) {
      errorMessage = 'No se pudo conectar con el servidor.';
    } else {
      errorMessage = error.message;
    }
    throw new Error(errorMessage);
  }
};

export const obtenerUsuario = async (userId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/usuarios/usuario/${userId}/`, { headers: getAuthHeaders() });
    return response.data;
  } catch (error) {
    console.error(`Error al obtener usuario ${userId}:`, error.response || error);
    let errorMessage = 'Error al obtener los datos del usuario.';
    if (error.response && error.response.data) {
      errorMessage = error.response.data.detail || (typeof error.response.data === 'string' ? error.response.data : JSON.stringify(error.response.data));
    } else if (error.request) {
      errorMessage = 'No se pudo conectar con el servidor.';
    } else {
      errorMessage = error.message;
    }
    throw new Error(errorMessage);
  }
};

export const actualizarUsuario = async (userId, userData) => {
  try {
    // Usamos PATCH para actualizaciones parciales, PUT si reemplazamos todo el objeto.
    // El backend (UsuarioSerializer) debe estar preparado para manejar los campos enviados.
    const response = await axios.patch(`${API_BASE_URL}/usuarios/usuario/${userId}/`, userData, { headers: getAuthHeaders() });
    return response.data;
  } catch (error) {
    console.error(`Error al actualizar usuario ${userId}:`, error.response || error);
    let errorMessage = 'Error al actualizar el usuario.';
    if (error.response && error.response.data) {
      errorMessage = error.response.data.detail || (typeof error.response.data === 'object' ? Object.values(error.response.data).flat().join(' ') : JSON.stringify(error.response.data));
    } else if (error.request) {
      errorMessage = 'No se pudo conectar con el servidor.';
    } else {
      errorMessage = error.message;
    }
    throw new Error(errorMessage);
  }
};