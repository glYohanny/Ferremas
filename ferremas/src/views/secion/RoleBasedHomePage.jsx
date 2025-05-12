import React from 'react';
import { Navigate } from 'react-router-dom';
import HomePage from '../Cliente/home.jsx'; // Home por defecto o para Cliente
import HomePageVendedor from '../vendedor/home_vendedor.jsx';
import HomePageContador from '../contador/home_contador.jsx';
import HomePageBodegero from '../bodegero/home_bodegero.jsx';
import HomePageAdmin from '../aministrador/home_admin.jsx';

function RoleBasedHomePage({ currentUser }) {
  if (!currentUser) {
    // Esto no debería ocurrir si la ruta está protegida, pero es una salvaguarda
    return <Navigate to="/login" />;
  }

  const roleName = currentUser.rol?.nombre_rol;

  switch (roleName) {
    case 'Administrador':
      return <HomePageAdmin currentUser={currentUser} />;
    case 'Vendedor':
      return <HomePageVendedor currentUser={currentUser} />;
    case 'Contador': // Asegúrate que el nombre del rol coincida exactamente
      return <HomePageContador currentUser={currentUser} />;
    case 'Bodeguero': // Asegúrate que el nombre del rol coincida exactamente
      return <HomePageBodegero currentUser={currentUser} />;
    case 'Cliente':
      return <HomePage currentUser={currentUser} />; // Asumiendo que HomePage es para clientes
    default:
      // Si el rol no se reconoce o es un cliente sin un home específico (o si HomePage es el default)
      // Puedes redirigir a una página de error, mostrar un home genérico, o el home de cliente.
      console.warn(`Rol no reconocido o sin home específico: ${roleName}`);
      return <HomePage currentUser={currentUser} />; // O <Navigate to="/error-page" />
  }
}

export default RoleBasedHomePage;