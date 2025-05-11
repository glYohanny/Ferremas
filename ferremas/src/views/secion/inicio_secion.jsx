// En tu componente de frontend, por ejemplo, dentro de la función handleSubmit
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom'; // Importar useNavigate y Link
import { login, getCurrentUser } from '../../api/autentificacion'; // Ajusta la ruta

// El componente LoginForm ahora acepta onLoginSuccess como prop
function LoginForm({ onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [rememberMe, setRememberMe] = useState(false); // Nuevo estado para "Recordarme"
  // const [userData, setUserData] = useState(null); // Este estado local es menos crucial si App.jsx maneja currentUser
  const navigate = useNavigate(); // Hook para la navegación

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setUserData(null);
    try {
      await login(username, password, rememberMe); // Pasar el estado de rememberMe a la función login
      console.log('Login exitoso, obteniendo datos del usuario...');
      const currentUser = await getCurrentUser(); // Luego obtén los datos del usuario
      // setUserData(currentUser); // Actualizar estado local (opcional si App.jsx lo maneja)
      console.log('Datos del usuario:', currentUser);

      // ¡Importante! Llama a onLoginSuccess para actualizar el estado en App.jsx
      if (onLoginSuccess) {
        onLoginSuccess(currentUser);
      }

      // AQUÍ ES DONDE USAS LA CATEGORÍA/ROL
      if (currentUser && currentUser.rol) { // Asumiendo que el campo se llama 'rol'
        const userRoleName = currentUser.rol.nombre_rol; // O como se llame el campo del nombre en tu serializador de Rol
        console.log('Rol del usuario:', userRoleName);
        // En lugar de alert y window.location.href, usa navigate
        if (userRoleName === 'Administrador') {
          console.log('Redirigiendo a dashboard de administrador...');
          navigate('/admin-dashboard'); // Ejemplo de ruta para admin
        } else if (userRoleName === 'Cliente') {
          console.log('Redirigiendo a portal de cliente...');
          navigate('/'); // Ejemplo de ruta para cliente (página principal)
        } else {
          console.log(`Rol ${userRoleName} reconocido, redirigiendo a la página principal...`);
          navigate('/'); // Ruta por defecto
        }
      } else {
        console.warn('No se pudo determinar el rol del usuario.');
        navigate('/'); // Ruta por defecto si no hay rol
      }
      // Si no hay lógica de roles o después de la lógica de roles, podrías simplemente navegar a '/'
      // navigate('/'); // Descomenta si quieres una redirección general después del login exitoso

    } catch (err) {
      setError(err.message || 'Error en el proceso de inicio de sesión o al obtener datos del usuario.');
      console.error("Error detallado:", err);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 p-4">
      <form 
        onSubmit={handleSubmit} 
        className="bg-white p-6 sm:p-8 rounded-lg shadow-sm w-full max-w-sm" // Más sutil la sombra, un poco más pequeño el max-w
      >
        <h2 className="text-xl sm:text-2xl font-semibold text-center text-slate-800 mb-8">Iniciar Sesión</h2> 
        
        {error && (
          <p className="bg-red-50 text-red-600 px-3 py-2 rounded mb-4 text-xs sm:text-sm" role="alert"> {/* Error más sutil */}
            {error}
          </p>
        )}

        <div className="mb-4">
          <label htmlFor="username" className="block text-slate-700 text-sm font-medium mb-1"> {/* Menos bold, más espacio */}
            Usuario (nombre_usuario):
          </label>
          <input 
            id="username"
            type="text" 
            value={username} 
            onChange={(e) => setUsername(e.target.value)} 
            required 
            className="appearance-none border border-slate-300 rounded w-full py-2 px-3 text-slate-700 leading-tight focus:outline-none focus:border-slate-500 focus:ring-1 focus:ring-slate-500" // Sin sombra por defecto, borde más sutil
          />
        </div>
        <div className="mb-6">
          <label htmlFor="password" className="block text-slate-700 text-sm font-medium mb-1">
            Contraseña:
          </label>
          <input 
            id="password"
            type="password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            required 
            className="appearance-none border border-slate-300 rounded w-full py-2 px-3 text-slate-700 leading-tight focus:outline-none focus:border-slate-500 focus:ring-1 focus:ring-slate-500"
          />
        </div>
        <div className="mb-6 flex items-center">
          <input 
            id="remember-me" 
            type="checkbox" 
            checked={rememberMe} 
            onChange={(e) => setRememberMe(e.target.checked)}
            className="h-4 w-4 text-slate-600 border-slate-300 rounded focus:ring-slate-500"
          />
          <label htmlFor="remember-me" className="ml-2 block text-sm text-slate-900">
            Recordarme
          </label>
        </div>
        <div className="flex flex-col space-y-3"> {/* Menos espacio entre botones */}
          <button 
            type="submit"
            className="w-full bg-slate-800 hover:bg-slate-700 text-white font-medium py-2.5 px-4 rounded focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-opacity-50" // Botón principal más sobrio
          >
            Iniciar Sesión
          </button>
          <div className="flex flex-col sm:flex-row sm:justify-between text-xs sm:text-sm text-center space-y-2 sm:space-y-0 pt-2"> {/* Ajuste para móviles y luego escritorio */}
            <button 
              type="button" 
              onClick={() => navigate('/registro')} // Navegar a la página de registro
              className="font-normal text-slate-600 hover:text-slate-800 hover:underline"
            >
              Registrarse
            </button>
            {/* Para "Recuperar Contraseña", necesitarías una ruta y un componente */}
            <Link to="/recuperar-password" className="font-normal text-slate-600 hover:text-slate-800 hover:underline">
              Recuperar Contraseña
            </Link>
          </div>
        </div>

        {/* Mostrar userData localmente es opcional, ya que App.jsx ahora tendrá currentUser */}
        {/* {userData && ( ... ) } */}
      </form>
    </div>
  );
}

export default LoginForm;
