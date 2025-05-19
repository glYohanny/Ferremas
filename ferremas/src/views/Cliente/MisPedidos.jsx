import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getMisPedidos } from '../../api/pedidos';
import { toast } from 'react-toastify';
import { format } from 'date-fns'; // Para formatear fechas
import { es } from 'date-fns/locale'; // Para formato de fecha en español

const MisPedidosPage = () => {
  const [pedidos, setPedidos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const cargarPedidos = async () => {
      try {
        setLoading(true);
        setError('');
        const data = await getMisPedidos();
        setPedidos(data || []); // Asegurarse de que sea un array
      } catch (err) {
        setError(err.message || 'No se pudieron cargar tus pedidos.');
        toast.error(err.message || 'No se pudieron cargar tus pedidos.');
      } finally {
        setLoading(false);
      }
    };

    cargarPedidos();
  }, []);

  if (loading) {
    return <div className="container mx-auto p-4 text-center">Cargando tus pedidos...</div>;
  }

  if (error) {
    return <div className="container mx-auto p-4 text-center text-red-500">{error}</div>;
  }

  return (
    <div className="container mx-auto p-4 sm:p-6 lg:p-8">
      <h1 className="text-3xl font-bold text-slate-800 mb-8 text-center">Mis Pedidos</h1>
      {pedidos.length === 0 ? (
        <div className="text-center text-slate-600">
          <p className="mb-4">Aún no has realizado ningún pedido.</p>
          <Link to="/" className="text-sky-600 hover:text-sky-700 font-semibold">
            Ir a la tienda
          </Link>
        </div>
      ) : (
        <div className="space-y-6">
          {pedidos.map((pedido) => (
            <div key={pedido.id} className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300">
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-4">
                <h2 className="text-xl font-semibold text-sky-700 mb-2 sm:mb-0">Pedido #{pedido.id}</h2>
                <span className={`px-3 py-1 text-sm font-medium rounded-full ${
                  pedido.estado_pedido?.nombre_estado === 'Entregado' ? 'bg-green-100 text-green-700' :
                  pedido.estado_pedido?.nombre_estado === 'Cancelado' ? 'bg-red-100 text-red-700' :
                  'bg-yellow-100 text-yellow-700' // Pendiente, En preparación, Enviado
                }`}>
                  {pedido.estado_pedido?.nombre_estado || 'Estado Desconocido'}
                </span>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 text-slate-700">
                <p><span className="font-semibold">Fecha:</span> {format(new Date(pedido.fecha), 'dd MMMM yyyy, HH:mm', { locale: es })}</p>
                <p><span className="font-semibold">Total:</span> ${new Intl.NumberFormat('es-CL').format(parseFloat(pedido.total || 0))}</p>
                <p><span className="font-semibold">Tipo de Entrega:</span> {pedido.tipo_entrega?.descripcion_entrega || 'N/A'}</p>
              </div>
              <div className="mt-6 text-right">
                <Link to={`/mis-pedidos/${pedido.id}`} className="text-sky-600 hover:text-sky-700 font-semibold">
                  Ver Detalles
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MisPedidosPage;