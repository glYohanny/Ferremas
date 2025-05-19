import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { obtenerProductos } from '../../api/productos'; // Asumiendo que tienes esta función
import { toast } from 'react-toastify';

// Componente para una tarjeta de producto simple (puedes reutilizar o crear uno más elaborado)
const ProductoCardMini = ({ producto }) => (
  <div className="border rounded-lg shadow overflow-hidden">
    <Link to={`/productos/${producto.id}`}>
      {producto.imagen_url ? (
        <img src={producto.imagen_url} alt={producto.nombre_producto} className="w-full h-40 object-cover" />
      ) : (
        <div className="w-full h-40 bg-slate-200 flex items-center justify-center text-slate-500">
          Imagen no disponible
        </div>
      )}
      <div className="p-3">
        <h3 className="text-md font-semibold text-slate-700 truncate" title={producto.nombre_producto}>{producto.nombre_producto}</h3>
        <p className="text-sm text-slate-800 font-bold">${producto.precio ? parseFloat(producto.precio).toFixed(2) : 'N/A'}</p>
      </div>
    </Link>
  </div>
);

function HomePage({ currentUser }) {
  // Determinar el nombre del rol, con un valor por defecto si no está disponible
  const userRole = currentUser?.rol?.nombre_rol || 'Usuario Desconocido';
  const [productosDestacados, setProductosDestacados] = useState([]);
  const [loadingDestacados, setLoadingDestacados] = useState(false);

  useEffect(() => {
    const cargarDestacados = async () => {
      setLoadingDestacados(true);
      try {
        // Podrías tener un parámetro en tu API para obtener "destacados" o simplemente tomar los primeros N
        const data = await obtenerProductos({ limit: 4 }); // Ejemplo: obtener 4 productos
        setProductosDestacados(data.results || data);
      } catch (error) {
        toast.error("Error al cargar productos destacados.");
        console.error("Error fetching featured products:", error);
      } finally {
        setLoadingDestacados(false);
      }
    };
    cargarDestacados();
  }, []);

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Sección Hero/Banner Principal */}
      <section className="bg-slate-700 text-white py-12 px-4 text-center">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          ¡Bienvenido a Ferremás, {currentUser?.nombre_usuario || 'Invitado'}!
        </h1>
        <p className="text-lg md:text-xl mb-8">
          Tu ferretería de confianza con todo lo que necesitas.
        </p>
        <Link 
          to="/" 
          className="bg-yellow-500 hover:bg-yellow-600 text-slate-900 font-bold py-3 px-8 rounded-lg text-lg transition duration-300"
        >
          Explorar Catálogo
        </Link>
      </section>

      <div className="container mx-auto p-4 md:p-8">
        {currentUser && (
          <div className="bg-white p-6 rounded-lg shadow-md mb-8 text-center flex flex-col sm:flex-row justify-center items-center space-y-2 sm:space-y-0 sm:space-x-4">
            <p className="text-lg text-slate-600">
              Sesión iniciada como: <span className="font-semibold text-slate-700">{userRole}</span>
            </p>
            {/* Enlaces específicos para usuarios logueados */}
            <Link to="/mis-pedidos" className="text-sky-600 hover:text-sky-700 font-semibold hover:underline">Mis Pedidos</Link>
            <Link to="/mi-perfil" className="text-sky-600 hover:text-sky-700 font-semibold hover:underline">Mi Perfil</Link>
          </div>
        )}

        {/* Sección de Productos Destacados */}
        {loadingDestacados && <p className="text-center py-4">Cargando productos destacados...</p>}
        {!loadingDestacados && productosDestacados.length > 0 && (
          <section className="mb-12">
            <h2 className="text-2xl font-semibold text-slate-800 mb-6 text-center md:text-left">Productos Destacados</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {productosDestacados.map(producto => <ProductoCardMini key={producto.id} producto={producto} />)}
            </div>
          </section>
        )}

        {/* Aquí podrías añadir secciones para Categorías, Promociones, etc. */}

        <footer className="text-center mt-12 py-6 border-t border-slate-200">
          <p className="text-sm text-slate-500">&copy; {new Date().getFullYear()} Ferremás. Todos los derechos reservados.</p>
        </footer>
      </div>
    </div>
  );
}

export default HomePage;