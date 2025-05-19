// Ejemplo: src/api/auth.js (en tu proyecto frontend)
import axios from 'axios';
import clientInstanceWithInterceptors from './cliente'; // Importar la instancia de cliente.js

const API_URL = 'http://localhost:8000/api/'; // URL base de tu API

// RE-EXPORTAR la instancia de cliente.js para que AuthContext y otros módulos la usen consistentemente
export const apiClient = clientInstanceWithInterceptors;

export const login = async (nombre_usuario, password, rememberMe = false) => {
  console.log("Intentando login con nombre_usuario:", nombre_usuario, "y password:", typeof password === 'string' && password.length > 0 ? "[CONTRASEÑA PRESENTE]" : "[CONTRASEÑA VACÍA O INVÁLIDA]", "Recordarme:", rememberMe);
  try {
    const response = await axios.post(`${API_URL}token/`, {
      nombre_usuario: nombre_usuario, // Usar el parámetro nombre_usuario
      password: password,
    });
    if (response.data.access) {
      // Almacena el token de acceso (y el de refresco si lo usas)
      const storage = rememberMe ? localStorage : sessionStorage;

      storage.setItem('accessToken', response.data.access);
      if (response.data.refresh) {
        storage.setItem('refreshToken', response.data.refresh);
      }

      // AuthContext se encargará de establecer apiClient.defaults.headers.common['Authorization']
      // después de que esta función de login devuelva el token.
      return response.data; // Devuelve los datos, incluyendo los tokens
    }
  } catch (error) {
    let errorMessage = 'Error desconocido en el inicio de sesión.';
    if (error.response) {
      console.error('Error en el inicio de sesión - Data:', error.response.data);
      console.error('Error en el inicio de sesión - Status:', error.response.status);
      errorMessage = error.response.data.detail || error.response.data.non_field_errors || JSON.stringify(error.response.data);
    } else if (error.request) {
      console.error('Error en el inicio de sesión - Request:', error.request);
      errorMessage = 'No se pudo conectar con el servidor. Inténtalo de nuevo.';
    } else {
      console.error('Error en el inicio de sesión - Message:', error.message);
      errorMessage = error.message;
    }
    throw new Error(errorMessage);
  }
};


export const logout = () => {
  // Elimina los tokens de ambos almacenamientos
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
  sessionStorage.removeItem('accessToken');
  sessionStorage.removeItem('refreshToken');
  // AuthContext se encargará de limpiar apiClient.defaults.headers.common['Authorization']
  // para la instancia apiClient (re-exportada arriba).
};

// ... (otras importaciones y funciones de autenticación) ...

// ... (resto de tus funciones de autenticación) ...


// Opcional: Función para refrescar el token de acceso
export const refreshToken = async () => {
    // Intenta obtener de localStorage primero, luego de sessionStorage
  const currentRefreshToken = localStorage.getItem('refreshToken') || sessionStorage.getItem('refreshToken');
  if (!currentRefreshToken) {
    return Promise.reject("No refresh token available");
  }
  try {
    // Usar axios directamente para el refresh, ya que apiClient podría entrar en un bucle de interceptor
    const response = await axios.post(`${API_URL}token/refresh/`, { 
      refresh: currentRefreshToken
    });
    if (response.data.access) {
      const newAccessToken = response.data.access;
      // El interceptor de respuesta en cliente.js (que llama a esta función)
      // ya se encarga de actualizar localStorage y apiClient.defaults.headers.common.
      // Solo necesitamos devolver el nuevo token.
      const storage = localStorage.getItem('refreshToken') ? localStorage : sessionStorage; // O simplemente localStorage
      storage.setItem('accessToken', newAccessToken); // Asegurar que se actualice en el storage correcto.
      return newAccessToken; // Devolver el nuevo token de acceso
    } else {
      // Si no hay accessToken en la respuesta, algo salió mal
      throw new Error("No se recibió un nuevo token de acceso al refrescar.");
    }
  } catch (error) {
    console.error('Error al refrescar el token:', error);
    // Si el refresh token es inválido o expiró, probablemente debas desloguear al usuario
    // El interceptor en cliente.js ya llama a performLogout (que es esta función logout) en caso de error de refresco.
    // logout(); // Redundante si el interceptor lo maneja.
    throw error;
  }
};


// Función para obtener el usuario actual (ejemplo de petición autenticada)
// Necesitarás un endpoint en tu API Django, por ejemplo: /api/usuarios/me/
export const getCurrentUser = async () => {
  try {
    // Usar la instancia apiClient (re-exportada de cliente.js),
    // que tiene los interceptores y cuyas cabeceras por defecto son manejadas por AuthContext.
    const response = await apiClient.get(`/usuarios/usuario/me/`); // URL relativa a API_BASE_URL
    return response.data; // Devuelve los datos del usuario, incluyendo su rol/categoría
  } catch (error) {
    let errorMessage = 'Error obteniendo la información del usuario.';
    if (error.response) {
      console.error('Error obteniendo usuario - Data:', error.response.data);
      console.error('Error obteniendo usuario - Status:', error.response.status);
      errorMessage = error.response.data.detail || JSON.stringify(error.response.data);
    } else if (error.request) {
      console.error('Error obteniendo usuario - Request:', error.request);
      errorMessage = 'No se pudo conectar con el servidor para obtener datos del usuario.';
    } else {
      console.error('Error obteniendo usuario - Message:', error.message);
    }
    throw new Error(errorMessage);
  }
};
