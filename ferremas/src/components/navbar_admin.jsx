import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext'; // Ajusta la ruta si es necesario
import {
  HomeIcon,
  UsersIcon,
  CubeIcon, // Para Productos
  DocumentTextIcon, // Para Pedidos/Reportes (antes DocumentReportIcon)
  Cog6ToothIcon, // Para Configuración (antes CogIcon)
  ArrowLeftOnRectangleIcon, // Para Logout (antes LogoutIcon)
  Bars3Icon, // Para Menú (antes MenuIcon)
  XMarkIcon, // Para Cerrar (antes XIcon)
} from '@heroicons/react/24/outline'; // Usando Heroicons v2

const NavbarAdmin = () => {
  const { currentUser, logout } = useAuth();
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(false); // Para el menú móvil

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error("Error al cerrar sesión (Admin):", error);
    }
  };

  const adminNavLinks = [
    { name: 'Dashboard', href: '/admin/dashboard', icon: HomeIcon },
    { name: 'Usuarios', href: '/admin/gestion-usuarios', icon: UsersIcon },
    // { name: 'Productos', href: '/admin/gestion-productos', icon: CubeIcon }, // Descomentar cuando tengas la ruta
    // { name: 'Pedidos', href: '/admin/pedidos', icon: DocumentTextIcon }, // Descomentar cuando tengas la ruta
    // { name: 'Configuración', href: '/admin/configuracion', icon: Cog6ToothIcon }, // Descomentar cuando tengas la ruta
  ];

  return (
    <>
      {/* Sidebar para escritorio (fijo a la izquierda) */}
      <div className="hidden md:flex md:w-64 md:flex-col md:fixed md:inset-y-0">
        <div className="flex flex-col flex-grow pt-5 pb-4 overflow-y-auto bg-slate-800">
          <div className="flex items-center flex-shrink-0 px-4">
            <Link to="/admin/dashboard" className="text-2xl font-bold text-yellow-400">
              Admin Ferremás
            </Link>
          </div>
          <nav className="mt-5 flex-1 px-2 space-y-1">
            {adminNavLinks.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className="group flex items-center px-2 py-2 text-sm font-medium rounded-md text-slate-300 hover:bg-slate-700 hover:text-white"
              >
                <item.icon className="mr-3 flex-shrink-0 h-6 w-6 text-slate-400 group-hover:text-slate-300" aria-hidden="true" />
                {item.name}
              </Link>
            ))}
          </nav>
          <div className="mt-auto p-2">
             <button
                onClick={handleLogout}
                className="w-full group flex items-center px-2 py-2 text-sm font-medium rounded-md text-slate-300 hover:bg-red-700 hover:text-white bg-red-600"
              >
                <ArrowLeftOnRectangleIcon className="mr-3 flex-shrink-0 h-6 w-6 text-slate-300 group-hover:text-slate-200" aria-hidden="true" />
                Cerrar Sesión
              </button>
          </div>
        </div>
      </div>

      {/* Navbar superior para móvil (para el botón de menú) */}
      {/* Esta parte es opcional si solo quieres el sidebar. Si la necesitas, la desarrollamos. */}
      {/* Por ahora, el contenido principal se desplazará con `ml-64` en `App.jsx` */}

      {/* Aquí podrías añadir un Navbar superior para pantallas pequeñas con un botón de menú si el sidebar no es suficiente */}
    </>
  );
};

export default NavbarAdmin;