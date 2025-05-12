import React from 'react';

function HomePageBodegero({ currentUser }) {
  // Determinar el nombre del rol, con un valor por defecto si no está disponible
  const userRole = currentUser?.rol?.nombre_rol || 'Usuario Desconocido';

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-slate-100 p-4">
      <div className="bg-white p-8 rounded-lg shadow-md text-center">
        <h1 className="text-3xl font-bold text-slate-800 mb-4">
          ¡Hola, {currentUser?.nombre_usuario || 'Invitado'}!
        </h1>
        <p className="text-lg text-slate-600">
          Has iniciado sesión como: <span className="font-semibold text-slate-700">{userRole}</span>
        </p>
        {/* Aquí podrías añadir más contenido específico de la página de inicio */}
        <p className="mt-6 text-sm text-slate-500">
          Bienvenido a Ferremas.
        </p>
      </div>
    </div>
  );
}

export default HomePageBodegero;