import React, { createContext, useState, useContext, useEffect } from 'react';
import { 
  login as apiLoginUser, // <--- CAMBIO AQUÍ: Importar 'login' y renombrarlo a 'apiLoginUser'
  logout as apiLogout,
  getCurrentUser as apiGetCurrentUser,
  // refreshToken as apiRefreshToken // Si necesitas exponerlo o usarlo internamente
} from '../api/autentificacion'; // Ajusta la ruta si es necesario
import { jwtDecode } from 'jwt-decode'; // Necesitarás instalar jwt-decode: npm install jwt-decode

const AuthContext = createContext(null);

export const useAuth = () => {
  return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('authToken'));
  const [initialLoading, setInitialLoading] = useState(true); // Renombrado para claridad
  // const [loginLoading, setLoginLoading] = useState(false); // Opcional: para carga específica del login

  useEffect(() => {
    const storedToken = localStorage.getItem('authToken');
    const storedUser = localStorage.getItem('currentUser');

    if (storedToken) {
      try {
        const decodedToken = jwtDecode(storedToken);
        const currentTime = Date.now() / 1000;

        if (decodedToken.exp > currentTime) {
          setToken(storedToken);
          if (storedUser) {
            setCurrentUser(JSON.parse(storedUser));
          } else { // Token existe, pero datos del usuario no están en localStorage.
            // Si no hay usuario en localStorage pero sí token, podrías intentar obtenerlo de la API
            console.warn("Token encontrado pero no el usuario en localStorage. Intentando obtener datos del usuario...");
            // Esta es una función autoejecutable asíncrona dentro del useEffect
            (async () => {
              try {
                // apiGetCurrentUser debería usar el token almacenado (posiblemente a través de un interceptor de Axios o pasándolo explícitamente si es necesario)
                const user = await apiGetCurrentUser();
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
          logout();
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
      // Asumimos que apiLoginUser (originalmente 'login' de autentificacion.js)
      // espera username y password como argumentos separados.
      const data = await apiLoginUser(username, password); 
      
      const authToken = data.access || data.token; // O como se llame tu token
      let userToStore = data.user;

      if (!userToStore && authToken) {
        // Si los datos del usuario no vienen en la respuesta del login, intenta obtenerlos.
        console.warn("Datos del usuario no recibidos en la respuesta de login. Intentando obtenerlos...");
        try {
          // apiGetCurrentUser debería usar el nuevo token.
          // Esto funcionará si apiGetCurrentUser lee el token de localStorage,
          // o si tienes un interceptor de Axios que añade el token a las cabeceras.
          // Temporalmente, para que funcione, podrías necesitar que apiGetCurrentUser acepte un token.
          // O, más simple, si apiGetCurrentUser siempre usa el token de localStorage,
          // asegúrate de que localStorage.setItem('authToken', authToken) se llame ANTES de apiGetCurrentUser.
          // Para este ejemplo, asumimos que apiGetCurrentUser puede funcionar después de que el token se haya guardado.
          userToStore = await apiGetCurrentUser();
        } catch (fetchError) {
          console.error("Error al obtener datos del usuario después del login:", fetchError);
          throw new Error("Login exitoso, pero no se pudieron obtener los datos del usuario.");
        }
      }

      if (authToken && userToStore) {
        localStorage.setItem('authToken', authToken);
        localStorage.setItem('currentUser', JSON.stringify(userToStore));
        setToken(authToken);
        setCurrentUser(userToStore);
        return userToStore; // Devuelve el usuario para posible uso posterior
      } else {
        throw new Error(data.detail || "Credenciales inválidas o respuesta inesperada de la API");
      }
    } catch (error) {
      // setLoginLoading(false); // Opcional
      console.error("Error en login:", error);
      logout(); // Limpia en caso de error
      throw error; // Propaga el error para que el componente de login lo maneje
    }
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    setToken(null);
    setCurrentUser(null);
  };

  // Podrías añadir una función de registro aquí también si lo necesitas
  // const register = async (userData) => { ... }

  const value = { 
    currentUser, 
    token, 
    login, 
    logout, 
    loading: initialLoading, // Usar initialLoading para el estado de carga global
    isAuthenticated: !!token && !!currentUser // Más estricto: autenticado si existen token Y datos de usuario
  };

  return <AuthContext.Provider value={value}>{!initialLoading && children}</AuthContext.Provider>;
};