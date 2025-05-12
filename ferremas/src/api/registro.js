// Ejemplo de contenido para src/api/registro.js o src/api/usuarios.js

import axios from 'axios';

// Asegúrate que la URL base y el endpoint sean los correctos para tu API de registro
const API_REGISTRO_URL = 'http://localhost:8000/api/usuarios/registro/cliente/'; // O la URL que corresponda

export const registrarCliente = async (userData) => {
  try {
    const response = await axios.post(API_REGISTRO_URL, userData);
    return response.data;
  } catch (error) {
    let errorMessage = 'Error desconocido en el registro.';
    if (error.response) {
      console.error('Error en el registro - Data:', error.response.data);
      console.error('Error en el registro - Status:', error.response.status);
      const errorData = error.response.data;
      // Intenta obtener un mensaje de error más específico
      if (typeof errorData === 'object' && errorData !== null) {
        errorMessage = Object.entries(errorData)
          .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`)
          .join('; ');
      } else if (errorData && errorData.detail) {
        errorMessage = errorData.detail;
      } else if (typeof errorData === 'string') {
        errorMessage = errorData;
      } else {
        errorMessage = "Error en el servidor al procesar el registro.";
      }
    } else if (error.request) {
      errorMessage = 'No se pudo conectar con el servidor. Inténtalo de nuevo.';
    } else {
      errorMessage = error.message;
    }
    throw new Error(errorMessage);
  }
};

// Si tienes otras funciones API relacionadas con usuarios/registro, también irían aquí.
