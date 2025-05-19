import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import { useCart } from './componets_CarritoCompra';
// Importaciones actualizadas para Heroicons v2 (ejemplo con outline de 24px)
import { ShoppingCartIcon } from '@heroicons/react/24/outline';
import { UserCircleIcon } from '@heroicons/react/24/outline';
import { ClipboardDocumentListIcon } from '@heroicons/react/24/outline'; // ClipboardListIcon -> ClipboardDocumentListIcon
import { ArrowLeftOnRectangleIcon } from '@heroicons/react/24/outline'; // LogoutIcon -> ArrowLeftOnRectangleIcon (o similar)
import { Bars3Icon } from '@heroicons/react/24/outline'; // MenuIcon -> Bars3Icon
import { XMarkIcon } from '@heroicons/react/24/outline'; // XIcon -> XMarkIcon


const NavbarCliente = () => {
  const { currentUser, logout } = useAuth();
  const { getCartItemCount } = useCart();
  const navigate = useNavigate();
  const [menuAbierto, setMenuAbierto] = useState(false);

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error("Error al cerrar sesión:", error);
      // Manejar el error, quizás mostrar un toast
    }
  };

  const navLinks = [
    { name: 'Catálogo', href: '/catalogo' }, // Actualizado para apuntar a la nueva ruta
    { name: 'Mis Pedidos', href: '/mis-pedidos', icon: ClipboardDocumentListIcon },
    { name: 'Mi Perfil', href: '/mi-perfil', icon: UserCircleIcon },
  ];

  return (
    <nav className="bg-slate-800 text-white shadow-lg sticky top-0 z-50">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo o Nombre de la Tienda */}
          <div className="flex-shrink-0">
            <Link to="/" className="text-2xl font-bold text-yellow-400 hover:text-yellow-300">
              Ferremás
            </Link>
          </div>

          {/* Enlaces de Navegación - Escritorio */}
          <div className="hidden md:flex md:items-center md:space-x-4">
            {navLinks.map((link) => (
              <Link
                key={link.name}
                to={link.href}
                className="px-3 py-2 rounded-md text-sm font-medium hover:bg-slate-700 transition-colors"
              >
                {link.icon && <link.icon className="h-5 w-5 inline-block mr-1 mb-0.5" />}
                {link.name}
              </Link>
            ))}
            <Link to="/carrito" className="flex items-center px-3 py-2 rounded-md text-sm font-medium hover:bg-slate-700 transition-colors">
              <ShoppingCartIcon className="h-5 w-5 mr-1" />
              Carrito ({getCartItemCount()})
            </Link>
            <button
              onClick={handleLogout}
              className="flex items-center px-3 py-2 rounded-md text-sm font-medium bg-red-500 hover:bg-red-600 transition-colors"
            >
              <ArrowLeftOnRectangleIcon className="h-5 w-5 mr-1" />
              Cerrar Sesión
            </button>
          </div>

          {/* Botón de Menú Móvil */}
          <div className="md:hidden flex items-center">
            <Link to="/carrito" className="p-2 rounded-md hover:bg-slate-700 transition-colors mr-2">
              <ShoppingCartIcon className="h-6 w-6" />
              <span className="sr-only">Carrito ({getCartItemCount()})</span>
            </Link>
            <button onClick={() => setMenuAbierto(!menuAbierto)} className="p-2 rounded-md hover:bg-slate-700 transition-colors">
              {menuAbierto ? <XMarkIcon className="h-6 w-6" /> : <Bars3Icon className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Panel de Menú Móvil */}
      {menuAbierto && (
        <div className="md:hidden bg-slate-700">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            {navLinks.map((link) => (
              <Link key={link.name} to={link.href} className="block px-3 py-2 rounded-md text-base font-medium hover:bg-slate-600 transition-colors">{link.name}</Link>
            ))}
            <button onClick={handleLogout} className="w-full text-left block px-3 py-2 rounded-md text-base font-medium bg-red-500 hover:bg-red-600 transition-colors">Cerrar Sesión</button>
          </div>
        </div>
      )}
    </nav>
  );
};

export default NavbarCliente;