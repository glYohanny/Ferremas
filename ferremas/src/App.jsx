// c:\Users\pedro\Desktop\ferremas2\ferremas\src\App.jsx
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'; // Importa componentes de react-router-dom
import { getCurrentUser, refreshToken, logout } from './api/autentificacion';
// import {registro_cliente} from './api/usuarios'; // Esta importación parece no usarse aquí directamente

// Importa tus componentes de página/vista
import LoginForm from './views/secion/inicio_secion.jsx';
import RegistroForm from './views/secion/registro_cliente.jsx'; // Importa RegistroForm aquí

function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const attemptAutoLogin = async () => {
      const refreshTokenValue = localStorage.getItem('refreshToken') || sessionStorage.getItem('refreshToken');
      if (refreshTokenValue) {
        try {
          await refreshToken();
          const user = await getCurrentUser();
          setCurrentUser(user);
        } catch (error) {
          logout();
          setCurrentUser(null);
        }
      }
      setIsLoading(false);
    };
    attemptAutoLogin();
  }, []);

  const handleLoginSuccess = (user) => {
    setCurrentUser(user);
    // Podrías navegar a otra ruta aquí si es necesario
  };

  const handleLogout = () => {
    logout();
    setCurrentUser(null);
    // Navegar al login
  };

  if (isLoading) {
    return <div className="min-h-screen flex items-center justify-center">Cargando aplicación...</div>;
  }

  return (
    <Router>
      {/* Podrías tener un Navbar aquí que cambie según currentUser */}
      {currentUser && (
        <div>
          <span>Bienvenido, {currentUser.nombre_usuario}! (Rol: {currentUser.rol?.nombre_rol || 'No definido'})</span>
          <button onClick={handleLogout}>Cerrar Sesión</button>
        </div>
      )}
      <Routes>
        <Route 
          path="/login" 
          element={!currentUser ? <LoginForm onLoginSuccess={handleLoginSuccess} /> : <Navigate to="/" />} 
        />
        <Route 
          path="/registro" 
          element={!currentUser ? <RegistroForm /> : <Navigate to="/" />} 
        />
        <Route 
          path="/" 
          element={currentUser ? <div>Página Principal Protegida</div> : <Navigate to="/login" />} 
        />
        {/* Añade más rutas aquí */}
      </Routes>
    </Router>
  );
}

export default App;
