import apiClient from './cliente'; // Importar la instancia configurada de Axios
import { API_BASE_URL } from './config';
// Ya no necesitas getAuthHeaders aquí, el interceptor lo maneja

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
    // Usar apiClient en lugar de axios. No es necesario pasar headers manualmente.
    const response = await apiClient.post(`/pedidos/pedidos/`, datosPedido); // API_BASE_URL ya está en apiClient
    return response.data; // Debería devolver los detalles del pedido creado o un mensaje de éxito
  } catch (error) {
    console.error("Error al crear el pedido:", error.response?.data || error.message);
    throw error.response?.data || new Error(error.response?.data?.detail || 'Error al procesar el pedido.');
  }
};

/**
 * Obtiene la lista de estados de pedido disponibles.
 */
export const getEstadosPedido = async () => {
  try {
    // Endpoint: /api/pedidos/estados-pedido/
    const response = await apiClient.get(`/pedidos/estados-pedido/`);
    return response.data.results || response.data; // Maneja paginación si existe
  } catch (error) {
    console.error("Error al cargar los estados de pedido:", error.response?.data || error.message);
    throw error.response?.data || new Error('Error al cargar los estados de pedido.');
  }
};

/**
 * Obtiene la lista de tipos de entrega disponibles.
 */
export const getTiposEntrega = async () => {
  try {
    // Endpoint: /api/pedidos/tipos-entrega/
    const response = await apiClient.get(`/pedidos/tipos-entrega/`);
    return response.data.results || response.data; // Maneja paginación si existe
  } catch (error) {
    console.error("Error al cargar los tipos de entrega:", error.response?.data || error.message);
    throw error.response?.data || new Error('Error al cargar los tipos de entrega.');
  }
};

/**
 * Obtiene la lista de métodos de pago disponibles.
 */
export const getMetodosPago = async () => {
  try {
    // Endpoint: /api/pagos/metodos-pago/ (este viene de pagos_app)
    const response = await apiClient.get(`/pagos/metodos-pago/`);
    return response.data.results || response.data; // Maneja paginación si existe
  } catch (error) {
    console.error("Error al cargar los métodos de pago:", error.response?.data || error.message);
    throw error.response?.data || new Error('Error al cargar los métodos de pago.');
  }
};

/**
 * Obtiene la lista de pedidos del usuario autenticado.
 */
export const getMisPedidos = async () => {
  try {
    // El interceptor en apiClient se encargará de añadir el token.
    // El backend (PedidoViewSet.get_queryset) filtrará por el usuario.
    const response = await apiClient.get(`/pedidos/pedidos/`); // Endpoint base del PedidoViewSet
    return response.data.results || response.data; // Maneja paginación si DRF la tiene configurada por defecto
  } catch (error) {
    console.error("Error al cargar mis pedidos:", error.response?.data || error.message);
    throw error.response?.data || new Error('Error al cargar mis pedidos.');
  }
};

/**
 * Obtiene los detalles de un pedido específico por su ID.
 * @param {string|number} pedidoId - El ID del pedido.
 */
export const getDetallePedidoCliente = async (pedidoId) => {
  try {
    // El backend (PedidoViewSet) ya debería tener una ruta para retrieve por ID.
    const response = await apiClient.get(`/pedidos/pedidos/${pedidoId}/`);
    return response.data; // Devuelve el objeto completo del pedido
  } catch (error) {
    console.error(`Error al cargar el detalle del pedido ${pedidoId}:`, error.response?.data || error.message);
    throw error.response?.data || new Error(`Error al cargar el detalle del pedido ${pedidoId}.`);
  }
};