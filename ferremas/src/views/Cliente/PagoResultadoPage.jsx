// src/views/Cliente/PagoResultadoPage.jsx (Nuevo archivo)
import React, { useEffect, useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';

const PagoResultadoPage = () => {
  const [searchParams] = useSearchParams();
  const [mensaje, setMensaje] = useState('');
  const [detalle, setDetalle] = useState('');

  useEffect(() => {
    const status = searchParams.get('status');
    const pedidoId = searchParams.get('pedido_id');
    // const tbkToken = searchParams.get('tbk_token'); // Podrías usarlo para más verificaciones si es necesario

    switch (status) {
      case 'aprobado':
        setMensaje(`¡Pago Aprobado para el Pedido #${pedidoId}!`);
        setDetalle('Gracias por tu compra. Hemos recibido tu pago y estamos procesando tu pedido.');
        // Aquí podrías limpiar el carrito si es apropiado
        break;
      case 'rechazado':
        setMensaje(`Pago Rechazado para el Pedido #${pedidoId}.`);
        setDetalle('Tu pago no pudo ser procesado. Por favor, intenta con otro método de pago o contacta a tu banco.');
        break;
      case 'abortado':
        setMensaje('Pago Cancelado.');
        setDetalle('Has cancelado el proceso de pago.');
        break;
      case 'error_confirmacion':
        setMensaje('Error en la Confirmación del Pago.');
        setDetalle('Ocurrió un error al intentar confirmar tu pago. Por favor, contacta a soporte.');
        break;
      default:
        setMensaje('Resultado del Pago Desconocido.');
        setDetalle('No se pudo determinar el estado de tu pago.');
    }
  }, [searchParams]);

  return (
    <div className="container mx-auto p-4 text-center">
      <h1 className="text-2xl font-bold mb-4">{mensaje}</h1>
      <p className="mb-6">{detalle}</p>
      <Link to="/" className="bg-sky-500 hover:bg-sky-600 text-white font-semibold py-2 px-4 rounded">
        Volver a la Tienda
      </Link>
      {searchParams.get('status') === 'aprobado' && searchParams.get('pedido_id') && (
        <Link to={`/mis-pedidos/${searchParams.get('pedido_id')}`} className="ml-4 bg-slate-200 hover:bg-slate-300 text-slate-700 font-semibold py-2 px-4 rounded">
          Ver Detalle del Pedido
        </Link>
      )}
    </div>
  );
};

export default PagoResultadoPage;
