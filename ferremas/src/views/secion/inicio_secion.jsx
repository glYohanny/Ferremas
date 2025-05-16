// En tu componente de frontend, por ejemplo, dentro de la función handleSubmit
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom'; // Importar useNavigate y Link
// import { login, getCurrentUser } from '../../api/autentificacion'; // Estas llamadas API deben ir DENTRO de la función login del AuthContext
import { toast } from 'react-toastify'; // Importar toast
import { useAuth } from '../../components/AuthContext'; // Importar useAuth

// El componente LoginForm ahora usa useAuth()
function LoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [rememberMe, setRememberMe] = useState(false); // Re-introducir el estado para "Recordarme"
  const navigate = useNavigate(); // Hook para la navegación
  // Obtener la función de login del AuthContext en el nivel superior del componente
  const { login: authLogin } = useAuth(); 

  // const [userData, setUserData] = useState(null); 

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); // Es buena práctica limpiar errores anteriores al intentar de nuevo
    // La variable 'authLogin' ya está disponible desde el scope superior del componente,
    // donde se obtuvo correctamente con useAuth(). No es necesario volver a llamarlo aquí.

    try {
      // Llamar a la función login del AuthContext.
      // Esta función DEBE manejar la llamada a la API, guardar el token,
      // obtener los datos del usuario y actualizar el estado del contexto (currentUser).
      await authLogin(username, password); // Pasa solo username y password si rememberMe se maneja en el backend o AuthContext

      toast.success("¡Inicio de sesión exitoso! Redirigiendo..."); // Notificación de éxito

      // La redirección ahora se maneja principalmente en App.jsx
      // a través del componente <Navigate to="/dashboard" />
      // que se activa cuando currentUser se actualiza en el AuthContext.
      // RoleBasedHomePage en /dashboard se encargará de la redirección final por rol.
      // No necesitas lógica de redirección compleja aquí.

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
