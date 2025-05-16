import axios from 'axios';
import { API_BASE_URL } from './config';
import { getAuthHeaders } from './autentificacion'; // Para enviar el token si el usuario está logueado

/**
 * Crea un nuevo pedido.
 * @param {Object} datosPedido - Los datos del pedido.
 * Ejemplo:
 * {
 *   // direccion_envio: "Calle Falsa 123",
 *   // comuna: 1, // ID de la comuna
 *   // telefono_contacto: "123456789",
 *   // email_contacto: "cliente@example.com", // Podría tomarse del usuario logueado
 *   items: [{ producto_id: 1, cantidad: 2 }, { producto_id: 2, cantidad: 1 }],
 *   // El backend debería calcular el total basado en los precios de los productos
 * }
 */
export const crearPedido = async (datosPedido) => {
  try {
    // Asumimos que el endpoint en tu backend será algo como '/pedidos/crear/' o '/ordenes/'
    // Necesitarás crear este endpoint en tu API de Django.
    const response = await axios.post(`${API_BASE_URL}/pedidos/pedidos/`, datosPedido, { headers: getAuthHeaders() });
    return response.data; // Debería devolver los detalles del pedido creado o un mensaje de éxito
  } catch (error) {
    console.error("Error al crear el pedido:", error.response?.data || error.message);
    throw error.response?.data || new Error(error.response?.data?.detail || 'Error al procesar el pedido.');
  }
};