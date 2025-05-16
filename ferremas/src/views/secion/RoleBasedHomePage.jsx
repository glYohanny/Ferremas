import React, { useEffect } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import HomePage from '../Cliente/Home.jsx'; // Home por defecto o para Cliente
import HomePageVendedor from '../vendedor/home_vendedor.jsx';
import HomePageContador from '../contador/home_contador.jsx';
import HomePageBodegero from '../bodegero/home_bodegero.jsx';
import HomePageAdmin from '../aministrador/home_admin.jsx';
import { useAuth } from '../../components/AuthContext.jsx'; // Importar useAuth

function RoleBasedHomePage() {
  const { currentUser } = useAuth(); // Obtener currentUser del contexto
  const navigate = useNavigate();

  useEffect(() => {
    if (!currentUser) {
      // Si por alguna razón currentUser se vuelve null mientras estamos aquí, redirigir a login.
      // Esto es una salvaguarda, PrivateRoute ya debería haber manejado esto.
      console.log('RoleBasedHomePage: currentUser es null, redirigiendo a /login');
      navigate('/login');
    }
  }, [currentUser, navigate]);

  if (!currentUser) {
    // Mostrar un loader o null mientras el useEffect maneja la redirección si es necesario
    return null; // O un spinner de carga
  }

  const roleName = currentUser.rol?.nombre_rol;

  // La lógica del switch permanece igual, pero ahora currentUser viene del contexto
  switch (roleName) {
    case 'Administrador': return <HomePageAdmin currentUser={currentUser} />;
    case 'Vendedor': return <HomePageVendedor currentUser={currentUser} />;
    case 'Contador': return <HomePageContador currentUser={currentUser} />;
    case 'Bodeguero': return <HomePageBodegero currentUser={currentUser} />;
    case 'Cliente': return <HomePage currentUser={currentUser} />;
    default:
      console.warn(`RoleBasedHomePage: Rol no reconocido o sin home específico: ${roleName}. Mostrando HomePage por defecto.`);
      return <HomePage currentUser={currentUser} />;
  }
}

export default RoleBasedHomePage;