// Ejemplo: src/api/auth.js (en tu proyecto frontend)
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/'; // URL base de tu API

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

      // Configura axios para enviar el token en futuras peticiones
      // Considerar usar una instancia de Axios dedicada o interceptores para un manejo más robusto.
      if (axios.defaults?.headers?.common) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
      }
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
  // Elimina el header de autorización de axios
  if (axios.defaults?.headers?.common) {
    delete axios.defaults.headers.common['Authorization'];
  }
};

// ... (otras importaciones y funciones de autenticación) ...

export const getAuthHeaders = () => {
  const token = localStorage.getItem('accessToken'); // O de donde obtengas tu token
  if (token) {
    return { Authorization: `Bearer ${token}` };
  }
  return {};
};

// ... (resto de tus funciones de autenticación) ...


// Opcional: Función para refrescar el token de acceso
export const refreshToken = async () => {
    // Intenta obtener de localStorage primero, luego de sessionStorage
  const currentRefreshToken = localStorage.getItem('refreshToken') || sessionStorage.getItem('refreshToken');
  if (!currentRefreshToken) {
    return Promise.reject("No refresh token available");
  }
  try {
    const response = await axios.post(`${API_URL}token/refresh/`, {
      refresh: currentRefreshToken
    });
    if (response.data.access) {
      // Almacenar el nuevo accessToken. Considerar la misma lógica de storage que en login si es necesario.
      // Por simplicidad y dado que los accessTokens son cortos, localStorage es común aquí.
      const storage = localStorage.getItem('refreshToken') ? localStorage : sessionStorage; // O simplemente localStorage
      storage.setItem('accessToken', response.data.access);
      
      if (axios.defaults?.headers?.common) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
      }
      return response.data.access;
    
    } else {
      // Si no hay accessToken en la respuesta, algo salió mal
      throw new Error("No se recibió un nuevo token de acceso al refrescar.");
    }
  } catch (error) {
    console.error('Error al refrescar el token:', error);
    // Si el refresh token es inválido o expiró, probablemente debas desloguear al usuario
    logout();
    throw error;
  }
};


// Función para obtener el usuario actual (ejemplo de petición autenticada)
// Necesitarás un endpoint en tu API Django, por ejemplo: /api/usuarios/me/
export const getCurrentUser = async () => {
  try {
    // Asegúrate de que el token de autorización ya esté configurado en axios.defaults.headers.common
    // La función login() ya hace esto.
    const response = await axios.get(`${API_URL}usuarios/usuario/me/`); // URL ajustada a la correcta
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
