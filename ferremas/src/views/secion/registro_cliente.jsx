import React, { useState, useEffect } from 'react';
import { registrarCliente } from '../../api/registro'; // Ajusta la ruta si creaste usuarios.js o si está en autentificacion.js
import { login } from '../../api/autentificacion'; // Importar la función de login
import { useNavigate, Link } from 'react-router-dom'; // Descomenta y usa Link si es necesario
import { getComunas } from '../../api/geografia';

// Podrías pasar una función onLoginSuccess desde App.jsx si necesitas actualizar el estado global allí
// function RegistroForm({ onLoginSuccess }) {
function RegistroForm() { 
  const navigate = useNavigate(); // Para react-router-dom
  const [comunas, setComunas] = useState([]); // Estado para las comunas
  const [formData, setFormData] = useState({
    nombre_usuario: '',
    email: '',
    password: '',
    confirmPassword: '',
    first_name: '',
    last_name: '',
    direccion_detallada: '',
    telefono: '',
    comuna_id: '', // Para el ID de la comuna seleccionada
  });
  const [error, setError] = useState('');
  const [loadingComunas, setLoadingComunas] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // useEffect para cargar las comunas al montar el componente
  useEffect(() => {
    const cargarComunas = async () => {
      setLoadingComunas(true);
      setError(''); // Limpiar errores previos
      try {
        const data = await getComunas(); // Llama a tu función API
        setComunas(Array.isArray(data) ? data : []);
      } catch (err) {
        console.error("Error al cargar comunas:", err);
        setError('Error al cargar comunas. Por favor, recarga la página o inténtalo más tarde.');
      }
      setLoadingComunas(false);
    };
    cargarComunas();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMessage('');
    setIsSubmitting(true);

    if (formData.password !== formData.confirmPassword) {
      setError('Las contraseñas no coinciden.');
      setIsSubmitting(false);
      return;
    }
    if (formData.password.length < 8) { // Ejemplo de validación simple
        setError('La contraseña debe tener al menos 8 caracteres.');
        setIsSubmitting(false);
        return;
    }

    // Prepara los datos para enviar, excluyendo confirmPassword
    const { confirmPassword, ...userDataToSubmit } = formData;
    const originalPassword = formData.password; // Guardar la contraseña original para el login
    
    try {
      const registeredUser = await registrarCliente(userDataToSubmit);
      setSuccessMessage(`¡Registro exitoso para ${registeredUser.nombre_usuario}! Intentando iniciar sesión automáticamente...`);

      // Intentar iniciar sesión automáticamente
      try {
        const loginResponse = await login(userDataToSubmit.nombre_usuario, originalPassword);
        // Si onLoginSuccess es una prop para actualizar el estado en App.jsx:
        // if (onLoginSuccess) {
        //   onLoginSuccess(loginResponse.user || { nombre_usuario: userDataToSubmit.nombre_usuario, rol: loginResponse.rol }); 
        // }
        console.log('¡Inicio de sesión automático exitoso!', loginResponse); // Confirmación en consola
        setSuccessMessage(`¡Bienvenido, ${userDataToSubmit.nombre_usuario}! Has sido registrado e iniciado sesión.`);
        setFormData({ // Limpiar formulario
          nombre_usuario: '', email: '', password: '', confirmPassword: '',
          first_name: '', last_name: '', direccion_detallada: '', telefono: '', comuna_id: ''
        });
        // Redirigir a la página principal o dashboard después de un breve retraso
        setTimeout(() => navigate('/'), 2000); // Ajusta la ruta según sea necesario

      } catch (loginError) {
        console.error("Error en el inicio de sesión automático:", loginError);
        // El registro fue exitoso, pero el inicio de sesión automático falló.
        setError(`Registro exitoso, pero el inicio de sesión automático falló: ${loginError.message || 'Error desconocido'}. Por favor, intenta iniciar sesión manualmente.`);
        // Opcionalmente, redirigir a la página de login después de mostrar el mensaje
        setTimeout(() => navigate('/login'), 4000);
      }
    } catch (registrationError) {
      console.error("Error en el registro:", registrationError);
      const errorMessage = registrationError.response?.data ? (typeof registrationError.response.data === 'string' ? registrationError.response.data : JSON.stringify(registrationError.response.data)) : (registrationError.message || 'Ocurrió un error durante el registro.');
      setError(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Estilos Tailwind CSS (puedes personalizarlos)
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 p-4">
      <form onSubmit={handleSubmit} className="bg-white p-6 sm:p-8 rounded-lg shadow-sm w-full max-w-md">
        <h2 className="text-xl sm:text-2xl font-semibold text-center text-slate-800 mb-8">Registrar Nuevo Cliente</h2>
        
        {error && <p className="bg-red-50 text-red-600 px-3 py-2 rounded mb-4 text-xs sm:text-sm" role="alert">{error}</p>}
        {successMessage && <p className="bg-green-50 text-green-700 px-3 py-2 rounded mb-4 text-xs sm:text-sm" role="alert">{successMessage}</p>}

        <div className="mb-4">
          <label htmlFor="nombre_usuario" className="block text-slate-700 text-sm font-medium mb-1">Nombre de Usuario:</label>
          <input type="text" name="nombre_usuario" id="nombre_usuario" value={formData.nombre_usuario} onChange={handleChange} required className="appearance-none border border-slate-300 rounded w-full py-2 px-3 text-slate-700 leading-tight focus:outline-none focus:border-slate-500 focus:ring-1 focus:ring-slate-500" />
        </div>

        <div className="mb-4">
          <label htmlFor="email" className="block text-slate-700 text-sm font-medium mb-1">Email:</label>
          <input type="email" name="email" id="email" value={formData.email} onChange={handleChange} required className="appearance-none border border-slate-300 rounded w-full py-2 px-3 text-slate-700 leading-tight focus:outline-none focus:border-slate-500 focus:ring-1 focus:ring-slate-500" />
        </div>

        <div className="mb-4">
          <label htmlFor="first_name" className="block text-slate-700 text-sm font-medium mb-1">Nombre:</label>
          <input type="text" name="first_name" id="first_name" value={formData.first_name} onChange={handleChange} required className="appearance-none border border-slate-300 rounded w-full py-2 px-3 text-slate-700 leading-tight focus:outline-none focus:border-slate-500 focus:ring-1 focus:ring-slate-500" />
        </div>

        <div className="mb-4">
          <label htmlFor="last_name" className="block text-slate-700 text-sm font-medium mb-1">Apellido:</label>
          <input type="text" name="last_name" id="last_name" value={formData.last_name} onChange={handleChange} required className="appearance-none border border-slate-300 rounded w-full py-2 px-3 text-slate-700 leading-tight focus:outline-none focus:border-slate-500 focus:ring-1 focus:ring-slate-500" />
        </div>
        <div className="mb-4">
          <label htmlFor="password" className="block text-slate-700 text-sm font-medium mb-1">Contraseña:</label>
          <input type="password" name="password" id="password" value={formData.password} onChange={handleChange} required className="appearance-none border border-slate-300 rounded w-full py-2 px-3 text-slate-700 leading-tight focus:outline-none focus:border-slate-500 focus:ring-1 focus:ring-slate-500" />
        </div>

        <div className="mb-6">
          <label htmlFor="confirmPassword" className="block text-slate-700 text-sm font-medium mb-1">Confirmar Contraseña:</label>
          <input type="password" name="confirmPassword" id="confirmPassword" value={formData.confirmPassword} onChange={handleChange} required className="appearance-none border border-slate-300 rounded w-full py-2 px-3 text-slate-700 leading-tight focus:outline-none focus:border-slate-500 focus:ring-1 focus:ring-slate-500" />
        </div>

        <div className="mb-4">
          <label htmlFor="direccion_detallada" className="block text-slate-700 text-sm font-medium mb-1">Dirección Detallada:</label>
          <textarea name="direccion_detallada" id="direccion_detallada" value={formData.direccion_detallada} onChange={handleChange} required rows="3" className="appearance-none border border-slate-300 rounded w-full py-2 px-3 text-slate-700 leading-tight focus:outline-none focus:border-slate-500 focus:ring-1 focus:ring-slate-500"></textarea>
        </div>

        <div className="mb-4">
          <label htmlFor="telefono" className="block text-slate-700 text-sm font-medium mb-1">Teléfono (Opcional):</label>
          <input type="tel" name="telefono" id="telefono" value={formData.telefono} onChange={handleChange} className="appearance-none border border-slate-300 rounded w-full py-2 px-3 text-slate-700 leading-tight focus:outline-none focus:border-slate-500 focus:ring-1 focus:ring-slate-500" />
        </div>

        <div className="mb-6">
          <label htmlFor="comuna_id" className="block text-slate-700 text-sm font-medium mb-1">Comuna:</label>
          <select name="comuna_id" id="comuna_id" value={formData.comuna_id} onChange={handleChange} required className="appearance-none border border-slate-300 rounded w-full py-2 px-3 text-slate-700 leading-tight focus:outline-none focus:border-slate-500 focus:ring-1 focus:ring-slate-500">
            <option value="" disabled>{loadingComunas ? "Cargando comunas..." : "Seleccione una comuna"}</option>
            {!loadingComunas && comunas.length === 0 && !error && (
              <option value="" disabled>No hay comunas disponibles</option>
            )}
            {!loadingComunas && comunas.length > 0 && (
              comunas.map(comuna => <option key={comuna.id} value={comuna.id}>{comuna.nombre_comuna}</option>)
            )}
            {!loadingComunas && error && (
              <option value="" disabled>Error al cargar comunas</option>
            )}
          </select>
        </div>

        <button type="submit" disabled={isSubmitting} className="w-full bg-slate-800 hover:bg-slate-700 text-white font-medium py-2.5 px-4 rounded focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-opacity-50 disabled:opacity-50">
          {isSubmitting ? 'Procesando...' : 'Registrarse'}
        </button>
        
        <p className="text-center text-sm text-slate-600 mt-4">
          ¿Ya tienes una cuenta? <Link to="/login" className="font-medium text-slate-800 hover:underline">Inicia sesión</Link>
        </p>
      </form>
    </div>
  );
}

export default RegistroForm;
