import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { obtenerProductos } from '../../api/productos'; // Ajusta la ruta si es necesario
import { toast } from 'react-toastify';
import { useCart } from '../../components/componets_CarritoCompra'; // Importar el hook del carrito

function CatalogoProductos() {
  const [productos, setProductos] = useState([]);
  const [loading, setLoading] = useState(true);
  // const [error, setError] = useState(null); // Manejado por toasts
  const { addItem } = useCart(); // Obtener la función addItem del contexto del carrito
  const navigate = useNavigate();

  useEffect(() => {
    const cargarProductos = async () => {
      try {
        setLoading(true);
        const data = await obtenerProductos();
        // Asegurarse de que 'productos' siempre sea un array
        if (data && Array.isArray(data.results)) {
          setProductos(data.results);
        } else if (Array.isArray(data)) {
          setProductos(data);
        } else {
          setProductos([]); // Por defecto a un array vacío si el formato no es el esperado
          console.warn("La respuesta de obtenerProductos no tiene el formato esperado (array o {results: array}):", data);
          // Podrías mostrar un toast aquí si data no es null/undefined pero no es el formato correcto
        }
      } catch (err) {
        // setError(err.message || 'Error al cargar productos.');
        toast.error(err.message || 'Error al cargar productos.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    cargarProductos();
      // Configurar el polling para recargar productos cada 30 segundos
    const intervalId = setInterval(cargarProductos, 30000); // Corregido: 30000 ms = 30 segundos

    // Función de limpieza para detener el polling cuando el componente se desmonte
    return () => {
      clearInterval(intervalId);
    };
  }, []);

  const handleAddToCart = (productoSeleccionado) => {
    if (productoSeleccionado && productoSeleccionado.stock > 0) {
      addItem(productoSeleccionado, 1); // Añade 1 unidad del producto
      toast.success(`${productoSeleccionado.nombre_producto} añadido al carrito!`);
    } else {
      toast.warn('Este producto está agotado o no se puede añadir.');
    }
  };

  if (loading) {
    return <div className="text-center py-10">Cargando productos...</div>;
  }

  // if (error) { // Manejado por toasts
  //   return <div className="text-center py-10 text-red-600">Error: {error}</div>;
  // }

  if (productos.length === 0) {
    return <div className="text-center py-10">No hay productos disponibles en este momento.</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-slate-800">Nuestro Catálogo</h1>
        <button
          onClick={() => navigate('/carrito')}
          className="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-md shadow hover:shadow-md transition duration-300"
        >
          Ver Carrito
        </button>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {productos.map((producto) => (
          <div key={producto.id} className="border rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 flex flex-col bg-white">
            <Link to={`/productos/${producto.id}`} className="block">
              {producto.imagen_url ? (
                <img src={producto.imagen_url} alt={producto.nombre_producto} className="w-full h-56 object-cover" />
              ) : (
                <div className="w-full h-56 bg-slate-200 flex items-center justify-center text-slate-500">
                  Imagen no disponible
                </div>
              )}
            </Link>
            <div className="p-4 flex flex-col flex-grow">
              <Link to={`/productos/${producto.id}`} className="block">
                <h2 className="text-xl font-semibold text-slate-700 mb-2 truncate" title={producto.nombre_producto}>{producto.nombre_producto}</h2>
                <p className="text-slate-600 mb-1 text-sm">Categoría: {producto.categoria?.nombre_categoria || 'N/A'}</p>
                <p className="text-lg font-bold text-slate-800">${producto.precio ? parseFloat(producto.precio).toFixed(2) : 'N/A'}</p>
              </Link>
              <button
                onClick={() => handleAddToCart(producto)}
                disabled={!producto.stock || producto.stock <= 0}
                className="mt-auto w-full bg-sky-500 hover:bg-sky-600 text-white font-semibold py-2 px-4 rounded-md shadow hover:shadow-md transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {producto.stock > 0 ? 'Añadir al Carrito' : 'Agotado'}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default CatalogoProductos;