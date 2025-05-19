// c:\Users\pedro\Desktop\ferremas2\ferremas\src\App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom'; // Importa useLocation
import { ToastContainer } from 'react-toastify'; // Importar ToastContainer
import 'react-toastify/dist/ReactToastify.css'; // Importar CSS de react-toastify
import { CartProvider } from './components/componets_CarritoCompra'; // Asegúrate de que la ruta sea correcta
import { AuthProvider, useAuth } from './components/AuthContext'; // Importar AuthProvider y useAuth


// Importa tus componentes de página/vista
// Vistas de Sesión
import LoginForm from './views/secion/inicio_secion.jsx';
import RegistroForm from './views/secion/registro_cliente.jsx'; // Importa RegistroForm aquí
import RecuperarPasswordForm from './views/secion/recuperar_contraseña.jsx'; // Importar el nuevo componente
import ConfirmarRecuperacionForm from './views/secion/confirmacion_de_recuperacion.jsx'; 
import RoleBasedHomePage from './views/secion/RoleBasedHomePage.jsx'; // Importar el nuevo componente

//navbar
import NavbarPublic from './components/NavbarPublic.jsx'; // Importar NavbarPublic
import NavbarAdmin from './components/navbar_admin.jsx'; // Ejemplo si la carpeta es 'administrador'
import NavbarCliente from './components/NavbarCliente.jsx'; // Importar NavbarCliente

// Vistas de Administrador
import GestionUsuariosPage from './views/aministrador/administrasionUsuario/gestion_usuarios.jsx'; // Importar el nuevo componente
import CrearUsuarioForm from './views/aministrador/administrasionUsuario/CrearUsuarioForm.jsx'; // Importar el nuevo componente
import EditarUsuarioForm from './views/aministrador/administrasionUsuario/EditarUsuarioForm.jsx'; // Importar el formulario de edición

//vistas de cliente
import CatalogoProductos from './views/Cliente/CatalogoProductos.jsx';
import DetalleProducto from './views/Cliente/DetalleProducto.jsx';
import CarritoPage from './views/Cliente/CarritoPage'; // Nueva importación
import CheckoutPage from './views/Cliente/CheckoutPage.jsx'; // Nueva importación
import MisPedidosPage from './views/Cliente/MisPedidos.jsx'; // Nueva importación
import DetallePedidoClientePage from './views/Cliente/DetallePedidoClientePage.jsx'; // Nueva importación
import MiPerfilPage from './views/Cliente/MiPerfilPage.jsx'; // Nueva importación
import PagoResultadoPage from './views/Cliente/PagoResultadoPage.jsx'; // Nueva importación


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
  const location = useLocation(); // Hook para obtener la ubicación actual

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Cargando aplicación...</div>;
  }

  const isAdminRoute = location.pathname.startsWith('/admin');
  const showAdminNavbar = isAdminRoute && currentUser && currentUser.rol?.nombre_rol === 'Administrador';
  
  // Mostrar NavbarCliente si el usuario está logueado, no es ruta de admin, y no es el rol de admin
  const showClienteNavbar = currentUser && !isAdminRoute && currentUser.rol?.nombre_rol !== 'Administrador';

  // Mostrar NavbarPublic si no hay usuario logueado y no es una ruta de admin
  const showPublicNavbar = !currentUser && !isAdminRoute;

  console.log('AppContent - currentUser:', currentUser);
  console.log('AppContent - isAdminRoute:', isAdminRoute);
  console.log('AppContent - showAdminNavbar:', showAdminNavbar);
  console.log('AppContent - showClienteNavbar:', showClienteNavbar);
  console.log('AppContent - showPublicNavbar:', showPublicNavbar);
  // Mostrar la barra de bienvenida genérica solo si no hay otra navbar y el usuario está logueado
  const showGenericWelcomeBar = currentUser && !showAdminNavbar && !showClienteNavbar;

  let mainContentPadding = "p-0"; // Default padding
  if (showAdminNavbar) {
    mainContentPadding = "ml-64 p-4"; // Padding para cuando el sidebar del admin está presente
  } else if (showClienteNavbar) {
    mainContentPadding = "pt-16"; // Padding top para el NavbarCliente sticky (h-16 = 4rem)
  } else if (showPublicNavbar) { // NavbarPublic tiene h-14
    mainContentPadding = "pt-14"; // Padding top para el NavbarPublic sticky (h-14 = 3.5rem)
  }
  return (
    <>
      {showAdminNavbar && <NavbarAdmin />}
      {showClienteNavbar && <NavbarCliente />}
      {showPublicNavbar && <NavbarPublic />}
      
      {showGenericWelcomeBar && (
        <div className="p-4 bg-slate-100 text-right">
          <span>Bienvenido, {currentUser.nombre_usuario}! (Rol: {currentUser.rol?.nombre_rol || 'No definido'})</span>
          <button onClick={logout} className="ml-4 bg-red-500 hover:bg-red-600 text-white font-semibold py-1 px-3 rounded">Cerrar Sesión</button>
        </div>
      )}
      <div className={mainContentPadding}>
        <Routes>
          <Route 
            path="/login" 
            // LoginForm ahora usará useAuth() para el login y para saber si ya está autenticado
            element={!currentUser ? <LoginForm /> : <Navigate to="/dashboard" />}
          />
          <Route 
            path="/registro" 
            element={!currentUser ? <RegistroForm /> : <Navigate to="/dashboard" />} // Redirigir al dashboard si ya está logueado
          />
          <Route 
            path="/recuperar-password"
            element={!currentUser ? <RecuperarPasswordForm /> : <Navigate to="/dashboard" />}
          />
          <Route 
            path="/reset-password-confirm/:uidb64/:token/"
            element={!currentUser ? <ConfirmarRecuperacionForm /> : <Navigate to="/dashboard" />} 
          />
          {/* Rutas de Cliente (protegidas y públicas) */}          <Route 
            path="/" 
            element={ // Lógica para la página de inicio según el rol
              currentUser && currentUser.rol?.nombre_rol !== 'Administrador' 
              ? <RoleBasedHomePage /> // Clientes y otros roles no admin van a su dashboard/home
              : currentUser && currentUser.rol?.nombre_rol === 'Administrador'
                ? <Navigate to="/admin/dashboard" /> // Admin va a su dashboard
                : <CatalogoProductos /> // No logueado ve el catálogo público
            } 
          />
          <Route path="/catalogo" element={<CatalogoProductos />} /> {/* Nueva ruta para el catálogo completo */}
          <Route path="/productos/:productoId" element={<DetalleProducto />} /> 
          <Route path="/pago/resultado" element={<PagoResultadoPage />} />
          <Route path="/carrito" element={
            <PrivateRoute roles={['Cliente', 'Vendedor', 'Bodeguero', 'Contador']}> {/* Permitir a otros roles ver/usar carrito si es necesario */}
              <CarritoPage />
            </PrivateRoute>
          } />
          <Route path="/checkout" element={
            <PrivateRoute roles={['Cliente', 'Vendedor']}> {/* Solo clientes y vendedores pueden hacer checkout */}
              <CheckoutPage />
            </PrivateRoute>
          } />
          <Route
              path="/mis-pedidos"
              element={
                <PrivateRoute roles={['Cliente']}>
                  <MisPedidosPage />
                </PrivateRoute>
              }
            />
            <Route
              path="/mis-pedidos/:pedidoId"
              element={
                <PrivateRoute roles={['Cliente']}>
                  <DetallePedidoClientePage />
                </PrivateRoute>
              }
            />
            <Route
              path="/mi-perfil"
              element={
                <PrivateRoute> {/* Cualquier usuario logueado puede ver su perfil */}
                  <MiPerfilPage />
                </PrivateRoute>
              }
            />
          <Route 
            path="/dashboard"
            element={
              <PrivateRoute>
                <RoleBasedHomePage /> {/* Ya no se pasa currentUser como prop */}
              </PrivateRoute>
            }
          />
          
          {/* Rutas específicas del Administrador */}
          {/* Asumo que /admin/dashboard es la home del admin, si no, ajustar la redirección de arriba */}
          <Route
            path="/admin/dashboard" 
            element={
              <PrivateRoute roles={['Administrador']}>
                <RoleBasedHomePage /> 
              </PrivateRoute>
            }
          />
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
          {/* Si tienes una página 404 personalizada, podrías añadirla aquí: */}
          {/* <Route path="*" element={<NotFound />} /> */}

          {/* Añade más rutas aquí */}
        </Routes>
      </div>
      <ToastContainer position="bottom-right" autoClose={3000} hideProgressBar={false} newestOnTop={false} closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
    </>
  );
}

const PrivateRoute = ({ children, roles }) => {
  const { currentUser, isAuthenticated, loading } = useAuth();
  const location = useLocation(); // Para redirigir guardando la ubicación original

  // console.log('PrivateRoute Render:', { 
  //   pathname: location.pathname, 
  //   isAuthenticated, 
  //   userRole: currentUser?.rol?.nombre_rol, 
  //   requiredRoles: roles });

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Verificando autenticación...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  if (roles && (!currentUser?.rol?.nombre_rol || !roles.includes(currentUser.rol.nombre_rol))) {
    // Si se especifican roles y el usuario no tiene uno de ellos
    // Podrías redirigir a una página de "Acceso Denegado" o al dashboard por defecto
    console.warn(`Acceso denegado para el rol: ${currentUser?.rol?.nombre_rol}. Roles requeridos: ${roles.join(', ')} en ruta ${location.pathname}`);
    return <Navigate to="/dashboard" replace />; // O una página de acceso denegado
  }

  return children;
};

export default App;
