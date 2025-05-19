import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getDetallePedidoCliente } from '../../api/pedidos';
import { toast } from 'react-toastify';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';

const DetallePedidoClientePage = () => {
  const { pedidoId } = useParams();
  const [pedido, setPedido] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const cargarDetallePedido = async () => {
      try {
        setLoading(true);
        setError('');
        const data = await getDetallePedidoCliente(pedidoId);
        setPedido(data);
      } catch (err) {
        setError(err.message || `No se pudo cargar el detalle del pedido ${pedidoId}.`);
        toast.error(err.message || `No se pudo cargar el detalle del pedido ${pedidoId}.`);
      } finally {
        setLoading(false);
      }
    };

    if (pedidoId) {
      cargarDetallePedido();
    }
  }, [pedidoId]);

  if (loading) {
    return <div className="container mx-auto p-4 text-center">Cargando detalle del pedido...</div>;
  }

  if (error) {
    return <div className="container mx-auto p-4 text-center text-red-500">{error}</div>;
  }

  if (!pedido) {
    return <div className="container mx-auto p-4 text-center">No se encontró el pedido.</div>;
  }

  return (
    <div className="container mx-auto p-4 sm:p-6 lg:p-8">
      <Link to="/mis-pedidos" className="text-sky-600 hover:text-sky-700 mb-6 inline-block">
        &larr; Volver a Mis Pedidos
      </Link>
      <h1 className="text-3xl font-bold text-slate-800 mb-6">Detalle del Pedido #{pedido.id}</h1>

      <div className="bg-white p-6 rounded-lg shadow-lg mb-6">
        <h2 className="text-xl font-semibold text-slate-700 mb-4 border-b pb-2">Información General</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-slate-600">
          <p><span className="font-semibold">Fecha:</span> {format(new Date(pedido.fecha), 'dd MMMM yyyy, HH:mm', { locale: es })}</p>
          <p><span className="font-semibold">Estado:</span> <span className={`px-2 py-0.5 text-sm font-medium rounded-full ${
                  pedido.estado_pedido?.nombre_estado === 'Entregado' ? 'bg-green-100 text-green-700' :
                  pedido.estado_pedido?.nombre_estado === 'Cancelado' ? 'bg-red-100 text-red-700' :
                  'bg-yellow-100 text-yellow-700'
                }`}>{pedido.estado_pedido?.nombre_estado || 'N/A'}</span></p>
          <p><span className="font-semibold">Total:</span> ${new Intl.NumberFormat('es-CL').format(parseFloat(pedido.total).toFixed(0))}</p>
          <p><span className="font-semibold">Método de Pago:</span> {pedido.metodo_pago?.descripcion_pago || 'N/A'}</p>
          <p><span className="font-semibold">Tipo de Entrega:</span> {pedido.tipo_entrega?.descripcion_entrega || 'N/A'}</p>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-lg mb-6">
        <h2 className="text-xl font-semibold text-slate-700 mb-4 border-b pb-2">Información de Contacto y Envío</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-slate-600">
          <p><span className="font-semibold">Nombre Contacto:</span> {pedido.nombre_completo_contacto}</p>
          <p><span className="font-semibold">Email Contacto:</span> {pedido.email_contacto}</p>
          <p><span className="font-semibold">Teléfono Contacto:</span> {pedido.telefono_contacto}</p>
          <p><span className="font-semibold">Dirección de Envío:</span> {pedido.direccion_envio}</p>
          <p><span className="font-semibold">Comuna de Envío:</span> {pedido.comuna_envio?.nombre_comuna || 'N/A'}</p>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h2 className="text-xl font-semibold text-slate-700 mb-4 border-b pb-2">Artículos del Pedido</h2>
        <div className="space-y-3">
          {pedido.detalles?.map((detalle) => (
            <div key={detalle.id} className="flex justify-between items-center p-3 border rounded-md">
              <div>
                <p className="font-medium text-slate-800">{detalle.producto?.nombre_producto || 'Producto Desconocido'}</p>
                <p className="text-sm text-slate-500">Cantidad: {detalle.cantidad}</p>
              </div>
              <p className="text-slate-700 font-semibold">${new Intl.NumberFormat('es-CL').format(parseFloat(detalle.precio_unitario_en_pedido || detalle.precio_unitario || 0) * detalle.cantidad)}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default DetallePedidoClientePage;