import axios from 'axios';

// URL base de la API de mindicador.cl que provee datos del Banco Central de Chile
const MININDICADOR_API_URL = 'https://mindicador.cl/api';

/**
 * Obtiene los principales indicadores económicos (incluyendo divisas) del día.
 * @returns {Promise<Object>} Un objeto con los indicadores.
 * Ejemplo de respuesta para el dólar: data.dolar = { codigo: 'dolar', nombre: 'Dólar observado', unidad_medida: 'Pesos', fecha: 'YYYY-MM-DDTHH:mm:ss.SSSZ', valor: 930.5 }
 */
export const obtenerIndicadoresEconomicos = async () => {
  try {
    const response = await axios.get(MININDICADOR_API_URL);
    return response.data; // Devuelve todos los indicadores
  } catch (error) {
    console.error("Error al obtener indicadores económicos:", error.response || error.request || error.message);
    throw new Error('No se pudieron obtener los indicadores económicos del Banco Central.');
  }
};

// Podrías añadir funciones más específicas si solo necesitas una divisa, por ejemplo:
// export const obtenerValorDolar = async () => {
//   try {
//     const response = await axios.get(`${MININDICADOR_API_URL}/dolar`);
//     return response.data; // Devuelve info específica del dólar
//   } catch (error) { ... }
// };