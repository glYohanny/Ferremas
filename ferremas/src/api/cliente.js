import axios from 'axios';
import { API_BASE_URL } from './config';
import { refreshToken as refreshAuthToken, logout as performLogout } from './autentificacion'; // Renombrar para evitar confusión

const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

// Interceptor para añadir el token de acceso a las peticiones
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    console.log(`cliente.js interceptor: Adding token from localStorage to request headers for ${config.url}:`, token ? `Bearer ${token.substring(0, 10)}...` : 'No token found');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar errores 401 y refrescar el token
let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // Verificar si el error es 401 y no es una petición de refresco de token
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // Si ya se está refrescando el token, encolar la petición
        return new Promise(function(resolve, reject) {
          failedQueue.push({ resolve, reject });
        }).then(token => {
          originalRequest.headers['Authorization'] = 'Bearer ' + token;
          return apiClient(originalRequest);
        }).catch(err => {
          return Promise.reject(err);
        });
      }

      originalRequest._retry = true; // Marcar que ya se intentó reintentar
      isRefreshing = true;

      try {
        const newAccessToken = await refreshAuthToken(); // Llama a tu función refreshToken
        localStorage.setItem('accessToken', newAccessToken); // Actualiza el token en localStorage
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`; // Actualiza el header por defecto para futuras peticiones de esta instancia
        originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`; // Actualiza el header de la petición original
        processQueue(null, newAccessToken); // Procesar la cola con el nuevo token
        return apiClient(originalRequest); // Reintentar la petición original
      } catch (refreshError) {
        console.error('Error al refrescar token, deslogueando:', refreshError);
        processQueue(refreshError, null); // Procesar la cola con error
        performLogout(); // Llama a tu función de logout
        // Opcionalmente, redirigir al login: window.location.href = '/login';
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;
