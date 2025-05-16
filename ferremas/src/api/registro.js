// Ejemplo de contenido para src/api/registro.js o src/api/usuarios.js

import axios from 'axios';
import { API_BASE_URL } from './config'; // Importar la URL base

// Asegúrate que la URL base y el endpoint sean los correctos para tu API de registro
const API_REGISTRO_URL = `${API_BASE_URL}/usuarios/registro/cliente/`; // Usar la URL base importada

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
      const status = error.response.status;

      if (status === 500) {
        errorMessage = "Ocurrió un error inesperado en el servidor. Por favor, inténtalo más tarde o contacta a soporte si el problema persiste.";
      } else if (typeof errorData === 'object' && errorData !== null) {
        // Si es un objeto, intenta concatenar los mensajes de error de cada campo.
        // Esto es útil para errores de validación de DRF (usualmente status 400).
        errorMessage = Object.keys(errorData)
          .map(key => `${key.replace("_", " ")}: ${Array.isArray(errorData[key]) ? errorData[key].join(', ') : errorData[key]}`) // Reemplaza guiones bajos para legibilidad
          .join('\n'); // Unir con nueva línea para mejor legibilidad si hay múltiples errores
        // Si el objeto parseado no generó un mensaje (ej. es un objeto de error no estándar sin mensajes de campo)
        if (!errorMessage.trim()) {
            errorMessage = errorData.detail || "Error en los datos enviados. Por favor, revisa el formulario.";
        }
      } else if (errorData && errorData.detail) {
        errorMessage = errorData.detail;
      } else if (typeof errorData === 'string' && errorData.length < 300) { // Evitar mostrar HTML largo como mensaje
        errorMessage = errorData;
      } else {
        // Fallback más genérico para otros errores del servidor con respuesta
        errorMessage = `Error del servidor (código: ${status}). Inténtalo más tarde.`;
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
