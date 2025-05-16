import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { obtenerProductoPorId } from '../../api/productos'; // Ajusta la ruta
import { toast } from 'react-toastify';
import { useCart } from '../../components/componets_CarritoCompra'; // Importar el hook del carrito

function DetalleProducto() {
  const { productoId } = useParams(); // Obtiene el ID (o slug) de la URL
  const [producto, setProducto] = useState(null);
  const [loading, setLoading] = useState(true);
  // const [error, setError] = useState(null); // Manejado por toasts
  const { addItem } = useCart(); // Obtener la función addItem del contexto del carrito
  const navigate = useNavigate();

  useEffect(() => {
    const cargarProducto = async () => {
      try {
        setLoading(true);
        const data = await obtenerProductoPorId(productoId);
        setProducto(data);
      } catch (err) {
        // setError(err.message || `Error al cargar el producto ${productoId}.`);
        toast.error(err.message || `Error al cargar el producto.`);
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    if (productoId) {
      cargarProducto();
    }
  }, [productoId]);

  const handleAddToCart = () => {
    if (producto && producto.stock > 0) {
      addItem(producto, 1); // Añade 1 unidad del producto
      toast.success(`${producto.nombre_producto} añadido al carrito!`);
    } else {
      toast.warn('Este producto está agotado o no se puede añadir.');
    }
  };
  if (loading) {
    return <div className="text-center py-10">Cargando detalle del producto...</div>;
  }

  // if (error) { // Manejado por toasts
  //   return <div className="text-center py-10 text-red-600">Error: {error}</div>;
  // }

  if (!producto) {
    return (
      <div className="text-center py-10">
        <p>Producto no encontrado.</p>
        <Link to="/" className="text-blue-600 hover:underline mt-4 inline-block">Volver al catálogo</Link>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4 md:p-8">
      <div className="flex justify-between items-center mb-6">
        <Link to="/" className="text-sky-600 hover:text-sky-700 hover:underline inline-flex items-center">
          &larr; Volver al Catálogo
        </Link>
        <button
          onClick={() => navigate('/carrito')}
          className="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-md shadow hover:shadow-md transition duration-300"
        >
          Ver Carrito
        </button>
      </div>
      <div className="grid md:grid-cols-2 gap-8 items-start">
        <div>
          {producto.imagen_url ? (
            <img src={producto.imagen_url} alt={producto.nombre_producto} className="w-full rounded-lg shadow-lg object-contain max-h-[500px]" />
          ) : (
            <div className="w-full h-96 bg-slate-200 flex items-center justify-center text-slate-500 rounded-lg shadow-lg">
              Imagen no disponible
            </div>
          )}
        </div>
        <div>
          <h1 className="text-3xl md:text-4xl font-bold text-slate-800 mb-3">{producto.nombre_producto}</h1>
          <p className="text-slate-500 text-sm mb-3">SKU: {producto.codigo_producto || 'N/A'} | Categoría: {producto.categoria?.nombre || 'N/A'}</p>
          <p className="text-2xl font-semibold text-slate-900 mb-4">${producto.precio ? parseFloat(producto.precio).toFixed(2) : 'N/A'}</p>
          <p className="text-slate-700 mb-6 leading-relaxed">{producto.descripcion || 'No hay descripción disponible.'}</p>
          <p className="text-sm text-slate-600 mb-4">Stock disponible: {producto.stock > 0 ? `${producto.stock} unidades` : 'Agotado'}</p>
          {/* Aquí iría el botón "Añadir al carrito" y selector de cantidad */}
          <button 
            onClick={handleAddToCart}
            className="w-full bg-sky-500 hover:bg-sky-600 text-white font-bold py-3 px-6 rounded-lg transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed" 
            disabled={!producto.stock || producto.stock <= 0}
          >
            {producto.stock > 0 ? 'Añadir al Carrito' : 'Producto Agotado'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default DetalleProducto;