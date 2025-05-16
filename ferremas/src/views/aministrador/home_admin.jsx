import React from 'react';
import { Link } from 'react-router-dom'; // Para la navegación

function HomePageAdmin({ currentUser }) {
  return (
    <div className="min-h-screen bg-slate-100 p-4 sm:p-6 md:p-8">
      <header className="mb-8">
        <h1 className="text-3xl sm:text-4xl font-bold text-slate-800">
          Panel de Administración
        </h1>
        <p className="text-lg text-slate-600">
          Bienvenido, {currentUser?.nombre_usuario || 'Administrador'}.
        </p>
      </header>

      <main>
        <section className="mb-10">
          <h2 className="text-2xl font-semibold text-slate-700 mb-4">Accesos Rápidos</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {/* Ejemplo de tarjetas de acceso rápido */}
            <Link to="/admin/gestion-usuarios" className="block p-6 bg-white rounded-lg shadow hover:shadow-md transition-shadow">
              <h3 className="text-xl font-semibold text-slate-800 mb-2">Gestión de Usuarios</h3>
              <p className="text-slate-600 text-sm">Crear, editar y administrar usuarios del sistema.</p>
            </Link>

            <Link to="/admin/informes" className="block p-6 bg-white rounded-lg shadow hover:shadow-md transition-shadow">
              <h3 className="text-xl font-semibold text-slate-800 mb-2">Informes</h3>
              <p className="text-slate-600 text-sm">Generar reportes de ventas, desempeño y más.</p>
            </Link>

            <Link to="/admin/productos" className="block p-6 bg-white rounded-lg shadow hover:shadow-md transition-shadow">
              <h3 className="text-xl font-semibold text-slate-800 mb-2">Productos y Catálogo</h3>
              <p className="text-slate-600 text-sm">Administrar el catálogo de productos.</p>
            </Link>

            <Link to="/admin/promociones" className="block p-6 bg-white rounded-lg shadow hover:shadow-md transition-shadow">
              <h3 className="text-xl font-semibold text-slate-800 mb-2">Estrategias y Promociones</h3>
              <p className="text-slate-600 text-sm">Crear y gestionar campañas de marketing.</p>
            </Link>

            <Link to="/admin/inventario" className="block p-6 bg-white rounded-lg shadow hover:shadow-md transition-shadow">
              <h3 className="text-xl font-semibold text-slate-800 mb-2">Inventario General</h3>
              <p className="text-slate-600 text-sm">Consultar y gestionar el stock.</p>
            </Link>

            <Link to="/admin/configuracion" className="block p-6 bg-white rounded-lg shadow hover:shadow-md transition-shadow">
              <h3 className="text-xl font-semibold text-slate-800 mb-2">Configuración</h3>
              <p className="text-slate-600 text-sm">Ajustes generales del sistema.</p>
            </Link>
          </div>
        </section>
        {/* Aquí podrías añadir un resumen del dashboard, KPIs, etc. */}
      </main>
    </div>
  );
}

export default HomePageAdmin;