import React from 'react';
import { Link } from 'react-router-dom';

const NavbarPublic = () => {
  return (
    <nav className="bg-slate-700 text-white shadow-md sticky top-0 z-40"> {/* z-40 para estar debajo de NavbarCliente si ambos se muestran por error */}
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-14">
          {/* Logo o Nombre de la Tienda */}
          <div className="flex-shrink-0">
            <Link to="/" className="text-xl font-bold text-yellow-400 hover:text-yellow-300">
              Ferremás
            </Link>
          </div>

          {/* Enlaces para Iniciar Sesión / Registrarse */}
          <div className="flex items-center space-x-4">
            <Link
              to="/login"
              className="px-3 py-2 rounded-md text-sm font-medium hover:bg-slate-600 transition-colors"
            >
              Iniciar Sesión
            </Link>
            <Link to="/registro" className="px-3 py-2 rounded-md text-sm font-medium bg-sky-500 hover:bg-sky-600 transition-colors">
              Registrarse
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default NavbarPublic;