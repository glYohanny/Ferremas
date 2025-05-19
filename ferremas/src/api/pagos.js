// src/api/pagos.js (o donde tengas tus funciones API)
import apiClient from './cliente'; // Tu instancia de Axios configurada

export const iniciarTransaccionWebpay = async (pedidoId) => {
  try {
    const response = await apiClient.post('/pagos/webpay/crear-transaccion/', {
      pedido_id: pedidoId,
    });
    return response.data; // Esperamos { token: "...", url_redirect: "..." }
  } catch (error) {
    console.error("Error al iniciar transacción Webpay:", error.response?.data || error.message);
    throw error.response?.data || new Error('Error al iniciar el pago con Webpay.');
  }
};
