import React, { createContext, useState, useContext, useEffect } from 'react';
import { 
  login as apiLoginUser, // <--- CAMBIO AQUÍ: Importar 'login' y renombrarlo a 'apiLoginUser'
  logout as apiLogout,
  getCurrentUser as apiGetCurrentUser,
  apiClient // Asegúrate de que autentificacion.js exporte apiClient
  // refreshToken as apiRefreshToken // Si necesitas exponerlo o usarlo internamente
} from '../api/autentificacion'; // Ajusta la ruta si es necesario
import { jwtDecode } from 'jwt-decode'; // Necesitarás instalar jwt-decode: npm install jwt-decode

const AuthContext = createContext(null);

export const useAuth = () => {
  return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('accessToken')); // <--- CAMBIO: Usar 'accessToken'
  const [refreshToken, setRefreshToken] = useState(localStorage.getItem('refreshToken'));
  const [initialLoading, setInitialLoading] = useState(true); // Renombrado para claridad
  // const [loginLoading, setLoginLoading] = useState(false); // Opcional: para carga específica del login

  useEffect(() => {
    const storedToken = localStorage.getItem('accessToken'); // <--- CAMBIO: Usar 'accessToken'
    const storedUser = localStorage.getItem('currentUser'); // Esto está bien
    const storedRefreshToken = localStorage.getItem('refreshToken'); // Esto está bien

    if (storedToken && storedRefreshToken) { // Verificar ambos tokens para una sesión "recordada"
      try {
        const decodedToken = jwtDecode(storedToken);
        const currentTime = Date.now() / 1000;

        if (decodedToken.exp > currentTime) {
          setToken(storedToken);
          setRefreshToken(storedRefreshToken); // Establecer token de refresco en el estado
          // Configurar la cabecera de autorización en la instancia de Axios al cargar desde localStorage
          if (apiClient && storedToken) {
             apiClient.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`;
          }
          if (storedUser) {
            setCurrentUser(JSON.parse(storedUser));
          } else { // Token existe, pero datos del usuario no están en localStorage.
            console.log("AuthContext useEffect: Token en localStorage, pero no datos de usuario. Intentando obtenerlos...");
            // Esta es una función autoejecutable asíncrona dentro del useEffect
            (async () => {
              try {
                // apiGetCurrentUser debería usar el token almacenado (posiblemente a través de un interceptor de Axios o pasándolo explícitamente si es necesario)
                const user = await apiGetCurrentUser();
                console.log("AuthContext useEffect: Datos de usuario obtenidos:", user);
                setCurrentUser(user);
                localStorage.setItem('currentUser', JSON.stringify(user));
              } catch (fetchError) {
                console.error("Error al obtener datos del usuario durante la carga inicial:", fetchError);
                // Si no se pueden obtener los datos del usuario, el token podría ser inválido o el usuario no existe.
                logout(); 
              }
            })();
          }
        } else {
          // Token expirado
          // Aquí es donde idealmente intentarías usar el storedRefreshToken para obtener un nuevo authToken.
          // Por ahora, si el token de acceso está expirado, cerramos sesión (esto se mejoraría con la lógica de refresco de token).
          console.warn("Token de acceso expirado durante la carga inicial. Se necesita implementar el flujo de refresco de token.");
          logout(); // Esto se mejoraría con la lógica de refresco de token.
        }
      } catch (error) {
        console.error("Error decodificando token:", error);
        logout(); // Token inválido o corrupto
      }
    }
    setInitialLoading(false); // Establecer en false después de la verificación inicial
  }, []);

  // Cambiada la firma para aceptar username y password
  const login = async (username, password) => { 
    // setLoginLoading(true); // Opcional
    try {
      console.log(`AuthContext: Iniciando login para usuario "${username}"`);
      // Asumimos que apiLoginUser (originalmente 'login' de autentificacion.js)
      // espera username y password como argumentos separados.
      const data = await apiLoginUser(username, password); 

      const authToken = data.access || data.token; // O como se llame tu token
      const newRefreshToken = data.refresh; // Asumimos que la API de login devuelve 'refresh'
      let userToStore = data.user;

      console.log("AuthContext: Respuesta de apiLoginUser (tokens):", { hasAuthToken: !!authToken, hasNewRefreshToken: !!newRefreshToken, userReceived: userToStore });

      if (authToken) {
        // Paso 1: apiLoginUser (desde autentificacion.js) ya guardó 'accessToken' en localStorage/sessionStorage.
        // AuthContext necesita actualizar su estado interno y las cabeceras por defecto de apiClient.
        // No es necesario que AuthContext vuelva a guardar 'authToken' o 'accessToken' aquí si apiLoginUser lo hizo.

        // Actualizar la cabecera de autorización por defecto de Axios
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${authToken}`;
        // console.log("AuthContext login: Axios Authorization header set."); // Opcional si el flujo funciona
        if (newRefreshToken) {
          // apiLoginUser (desde autentificacion.js) ya guardó 'refreshToken' en localStorage/sessionStorage.
        }

        // Paso 2: Si los datos del usuario no vinieron con el login, obtenerlos usando el nuevo token.
        if (!userToStore) {
          console.log("AuthContext: Datos de usuario no en respuesta de login. Llamando a apiGetCurrentUser...");
          try {
            userToStore = await apiGetCurrentUser(); // Esta llamada ahora debería usar el nuevo token.
            console.log("AuthContext: Respuesta de apiGetCurrentUser:", userToStore);
          } catch (fetchError) {
            console.error("Error al obtener datos del usuario después del login (con nuevo token):", fetchError);
            await logout(); // Limpiar todo si no se pueden obtener los detalles del usuario.
            throw new Error("Token de login obtenido, pero no se pudieron obtener los datos del usuario.");
          }
        }

        // Paso 3: Si tenemos los datos del usuario (ya sea del login inicial o de apiGetCurrentUser).
        if (userToStore) {
          localStorage.setItem('currentUser', JSON.stringify(userToStore));
          setToken(authToken); // Actualizar estado del token
          if (newRefreshToken) {
            setRefreshToken(newRefreshToken); // Actualizar estado del refresh token
          }
          setCurrentUser(userToStore); // <<<< ¡ACTUALIZAR EL ESTADO currentUser CON EL NUEVO USUARIO!
          console.log("AuthContext: Estado currentUser actualizado con:", {id: userToStore?.id, nombre_usuario: userToStore?.nombre_usuario, rol: userToStore?.rol?.nombre_rol});
          return userToStore; // Devuelve el usuario para posible uso posterior
        } else {
          // Este caso significa que se obtuvo un token, pero no se pudieron obtener/encontrar los datos del usuario.
          console.error("AuthContext: Token obtenido, pero userToStore sigue vacío después de intentar obtenerlo.");
          await logout(); // Limpiar.
          throw new Error("Token de login obtenido, pero no se pudieron obtener los detalles completos del usuario.");
        }
      } else {
        // No se recibió authToken de apiLoginUser.
        throw new Error(data.detail || "No se recibió token de autenticación de la API.");
      }
    } catch (error) {
      // This catch handles errors from apiLoginUser or the throw from the inner catch
      // setLoginLoading(false); // Opcional
      console.error("Error en login:", error);
      // Considera si logout() aquí es siempre lo correcto, o si el error ya fue manejado.
      // Si el error es por "credenciales inválidas", logout() es seguro.
      await logout(); // Asegurar limpieza.
      throw error; // Propaga el error para que el componente de login lo maneje
    }
  };

  const logout = () => {
    // apiLogout (desde autentificacion.js) ya se encarga de limpiar 'accessToken' y 'refreshToken'
    // de localStorage y sessionStorage.
    // AuthContext solo necesita limpiar su estado y las cabeceras de apiClient.
    // localStorage.removeItem('accessToken'); // Redundante si apiLogout lo hace
    localStorage.removeItem('refreshToken'); // Eliminar token de refresco
    localStorage.removeItem('currentUser');
    // Limpiar la cabecera de autorización por defecto de Axios
    if (apiClient.defaults.headers.common['Authorization']) {
      delete apiClient.defaults.headers.common['Authorization'];
      // console.log("AuthContext logout: Axios Authorization header deleted."); // Opcional
    }
    setToken(null); // Limpiar estado del token
    setRefreshToken(null); // Limpiar estado del token de refresco
    setCurrentUser(null);
  };

  // Nueva función para actualizar el perfil del usuario en el contexto y localStorage
  const updateUserProfileInContext = (newProfileData) => {
    setCurrentUser(prevUser => {
      const updatedUser = { ...prevUser, ...newProfileData };
      // Asegúrate de que el objeto 'updatedUser' sea completo y correcto
      localStorage.setItem('currentUser', JSON.stringify(updatedUser)); 
      // console.log("AuthContext: updateUserProfileInContext - currentUser actualizado:", updatedUser); // Opcional
      return updatedUser;
    });
  };

  // Podrías añadir una función de registro aquí también si lo necesitas
  // const register = async (userData) => { ... }

  const value = { 
    currentUser,
    // setCurrentUser, // Considera si aún necesitas exponer el setter crudo
    updateUserProfile: updateUserProfileInContext, // Exponer la nueva función
    token,
    refreshToken, // Exponer el token de refresco si es necesario fuera del contexto
    login,
    logout,
    loading: initialLoading, // Usar initialLoading para el estado de carga global
    isAuthenticated: !!token && !!currentUser // Más estricto: autenticado si existen token Y datos de usuario
  };
  return <AuthContext.Provider value={value}>{!initialLoading && children}</AuthContext.Provider>;
};