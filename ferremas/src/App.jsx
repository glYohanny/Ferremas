// c:\Users\pedro\Desktop\ferremas2\ferremas\src\App.jsx
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'; // Importa componentes de react-router-dom
import { ToastContainer } from 'react-toastify'; // Importar ToastContainer
import 'react-toastify/dist/ReactToastify.css'; // Importar CSS de react-toastify
import { CartProvider } from './components/componets_CarritoCompra'; // Asegúrate de que la ruta sea correcta
import { AuthProvider, useAuth } from './components/AuthContext'; // Importar AuthProvider y useAuth


// Importa tus componentes de página/vista
import LoginForm from './views/secion/inicio_secion.jsx';
import RegistroForm from './views/secion/registro_cliente.jsx'; // Importa RegistroForm aquí
import RecuperarPasswordForm from './views/secion/recuperar_contraseña.jsx'; // Importar el nuevo componente
import ConfirmarRecuperacionForm from './views/secion/confirmacion_de_recuperacion.jsx'; 
import RoleBasedHomePage from './views/secion/RoleBasedHomePage.jsx'; // Importar el nuevo componente
import GestionUsuariosPage from './views/aministrador/administrasionUsuario/gestion_usuarios.jsx'; // Importar el nuevo componente
import CrearUsuarioForm from './views/aministrador/administrasionUsuario/CrearUsuarioForm.jsx'; // Importar el nuevo componente
import EditarUsuarioForm from './views/aministrador/administrasionUsuario/EditarUsuarioForm.jsx'; // Importar el formulario de edición
import CatalogoProductos from './views/cliente/CatalogoProductos.jsx';
import DetalleProducto from './views/cliente/DetalleProducto.jsx';
import CarritoPage from './views/Cliente/CarritoPage'; // Nueva importación
import CheckoutPage from './views/Cliente/CheckoutPage.jsx'; // Nueva importación


function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <Router>
          <AppContent /> {/* Mover el contenido principal a un componente hijo */}
        </Router>
      </CartProvider>
    </AuthProvider>
  );
}

// Nuevo componente para acceder al contexto de autenticación
function AppContent() {
  const { currentUser, loading, logout } = useAuth(); // Obtener currentUser y loading de AuthContext

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Cargando aplicación...</div>;
  }

  return (
    <>
      {/* Navbar o sección de bienvenida que usa currentUser y logout del AuthContext */}
      {currentUser && (
        <div className="p-4 bg-slate-100 text-right">
          <span>Bienvenido, {currentUser.nombre_usuario}! (Rol: {currentUser.rol?.nombre_rol || 'No definido'})</span>
          <button onClick={logout} className="ml-4 bg-red-500 hover:bg-red-600 text-white font-semibold py-1 px-3 rounded">Cerrar Sesión</button>
        </div>
      )}
      <Routes>
          <Route 
            path="/login" 
            // LoginForm ahora usará useAuth() para el login y para saber si ya está autenticado
            element={!currentUser ? <LoginForm /> : <Navigate to="/dashboard" />}
          />
          <Route 
            path="/registro" 
            element={!currentUser ? <RegistroForm /> : <Navigate to="/" />} 
          />
          <Route 
            path="/recuperar-password"
            element={!currentUser ? <RecuperarPasswordForm /> : <Navigate to="/" />} // Solo accesible si no está logueado
          />
          <Route 
            path="/reset-password-confirm/:uidb64/:token/"
            element={!currentUser ? <ConfirmarRecuperacionForm /> : <Navigate to="/" />} 
          />
          {/* Rutas específicas del Administrador */}
          <Route
            path="/admin/gestion-usuarios"
            element={
              <PrivateRoute roles={['Administrador']}>
                <GestionUsuariosPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/admin/gestion-usuarios/crear"
            element={
              <PrivateRoute roles={['Administrador']}>
                <CrearUsuarioForm />
              </PrivateRoute>
            }
          />
          <Route
            path="/admin/gestion-usuarios/editar/:userId" // Ruta con parámetro para el ID del usuario
            element={
              <PrivateRoute roles={['Administrador']}>
                <EditarUsuarioForm />
              </PrivateRoute>
            }
          />
          {/* Rutas Públicas / Cliente */}
          <Route path="/" element={<CatalogoProductos />} /> {/* Esta es tu página de inicio pública */}
          <Route path="/productos/:productoId" element={<DetalleProducto />} /> 
          <Route path="/carrito" element={<CarritoPage />} /> {/* Nueva ruta para el carrito */}
          <Route path="/checkout" element={<CheckoutPage />} /> {/* Nueva ruta para checkout */}
          <Route 
            path="/dashboard"
            element={
              <PrivateRoute>
                <RoleBasedHomePage /> {/* Ya no se pasa currentUser como prop */}
              </PrivateRoute>
            }
          />
          {/* Si tienes una página 404 personalizada, podrías añadirla aquí: */}
          {/* <Route path="*" element={<NotFound />} /> */}

          {/* Añade más rutas aquí */}
        </Routes>
    </>
  );
}

const PrivateRoute = ({ children, roles }) => {
  const { currentUser, isAuthenticated, loading } = useAuth();
  console.log('PrivateRoute Render:', { currentUser: !!currentUser, isAuthenticated, loading, requiredRoles: roles }); // Log state for debugging
  console.log('AppContent Render:', { currentUser: !!currentUser, loading, isAuthenticated: !!currentUser }); // Log state for debugging
  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Verificando autenticación...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  if (roles && !roles.includes(currentUser?.rol?.nombre_rol)) {
    // Si se especifican roles y el usuario no tiene uno de ellos
    // Podrías redirigir a una página de "Acceso Denegado" o al dashboard por defecto
    console.warn(`Acceso denegado para el rol: ${currentUser?.rol?.nombre_rol}. Roles requeridos: ${roles.join(', ')}`);
    return <Navigate to="/dashboard" />; // O una página de acceso denegado
  }

  return children;
};

export default App;
