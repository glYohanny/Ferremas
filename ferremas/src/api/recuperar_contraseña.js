import axios from 'axios';

// Asume que API_BASE_URL está definida aquí o importada de otro archivo de configuración
const API_BASE_URL = 'http://localhost:8000/api'; // Ejemplo, ajusta según tu configuración

// NUEVA FUNCIÓN PARA SOLICITAR RESTABLECIMIENTO DE CONTRASEÑA
export const solicitarResetPassword = async (email) => {
  try {
    // La URL completa sería algo como: http://localhost:8000/api/usuarios/password-reset-request/
    const response = await axios.post(`${API_BASE_URL}/usuarios/password-reset-request/`, { email });
    return response.data; // Debería devolver el mensaje de éxito del backend
  } catch (error) {
    console.error("Error en solicitarResetPassword API:", error.response || error);
    let errorMessage = 'Error al solicitar el restablecimiento de contraseña.';
    if (error.response && error.response.data) {
      // Intenta obtener un mensaje más específico del backend
      if (typeof error.response.data === 'string') {
        errorMessage = error.response.data;
      } else if (error.response.data.error) { // Si el backend devuelve { "error": "mensaje" }
        errorMessage = error.response.data.error;
      } else if (error.response.data.message) { // Si el backend devuelve { "message": "mensaje" }
        errorMessage = error.response.data.message;
      } else { // Como último recurso, convierte el objeto de error a string
        errorMessage = JSON.stringify(error.response.data);
      }
    } else if (error.request) {
      errorMessage = 'No se pudo conectar con el servidor. Inténtalo de nuevo.';
    } else { // Otros errores (ej. error de configuración de la petición)
      errorMessage = error.message;
    }
    throw new Error(errorMessage);
  }
};
export const confirmarResetPassword = async (uidb64, token, newPassword, confirmPassword) => {
  try {
    // La URL completa sería algo como: http://localhost:8000/api/usuarios/password-reset-confirm/
    // Ajusta la ruta según cómo la definas en tu backend.
    const response = await axios.post(`${API_BASE_URL}/usuarios/password-reset-confirm/`, {
      uidb64,
      token,
      new_password: newPassword, // Asegúrate que los nombres de los campos coincidan con lo que espera tu backend
      confirm_password: confirmPassword,
    });
    return response.data; // Debería devolver un mensaje de éxito
  } catch (error) {
    console.error("Error en confirmarResetPassword API:", error.response || error);
    let errorMessage = 'Error al confirmar el restablecimiento de contraseña.';
    if (error.response && error.response.data) {
      // Intenta obtener un mensaje más específico del backend
      errorMessage = typeof error.response.data === 'string' ? error.response.data :
                     error.response.data.error || error.response.data.message || JSON.stringify(error.response.data);
    } else if (error.request) {
      errorMessage = 'No se pudo conectar con el servidor. Inténtalo de nuevo.';
    } else {
      errorMessage = error.message;
    }
    throw new Error(errorMessage);
  }
};