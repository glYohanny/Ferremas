import React, { useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import axios from 'axios'; // Importar axios
import { API_BASE_URL } from '../../api/config'; // Asumiendo que tienes API_BASE_URL en un archivo de config

// import { confirmarResetPassword } from '../../api/recuperar_contraseña'; // Necesitarás crear esta función API

function ResetPasswordConfirmForm() {
  const { uidb64, token } = useParams(); // Obtener uidb64 y token de la URL
  const navigate = useNavigate();

  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');
    setIsSubmitting(true);

    if (!newPassword || !confirmPassword) {
      setError('Por favor, completa ambos campos de contraseña.');
      setIsSubmitting(false);
      return;
    }

    if (newPassword !== confirmPassword) {
      setError('Las contraseñas no coinciden.');
      setIsSubmitting(false);
      return;
    }

    if (newPassword.length < 8) {
        setError('La nueva contraseña debe tener al menos 8 caracteres.');
        setIsSubmitting(false);
        return;
    }

    try {
      const response = await confirmarResetPassword(uidb64, token, newPassword, confirmPassword); // Llama a la función API definida abajo
      setMessage(response.message || 'Tu contraseña ha sido restablecida exitosamente. Ahora puedes iniciar sesión con tu nueva contraseña.');
      // Limpiar campos y redirigir al login después de un momento
      setNewPassword('');
      setConfirmPassword('');
      setTimeout(() => {
        navigate('/login');
      }, 3000);
    } catch (err) {
      console.error("Error al confirmar restablecimiento:", err);
      setError(err.message || 'Ocurrió un error al restablecer tu contraseña. El enlace podría haber expirado o ser inválido.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 p-4">
      <form onSubmit={handleSubmit} className="bg-white p-6 sm:p-8 rounded-lg shadow-sm w-full max-w-md">
        <h2 className="text-xl sm:text-2xl font-semibold text-center text-slate-800 mb-8">Restablecer Contraseña</h2>

        {error && <p className="bg-red-50 text-red-600 px-3 py-2 rounded mb-4 text-xs sm:text-sm" role="alert">{error}</p>}
        {message && <p className="bg-green-50 text-green-700 px-3 py-2 rounded mb-4 text-xs sm:text-sm" role="alert">{message}</p>}

        <div className="mb-4">
          <label htmlFor="newPassword" className="block text-slate-700 text-sm font-medium mb-1">Nueva Contraseña:</label>
          <input
            type="password"
            id="newPassword"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            required
            className="appearance-none border border-slate-300 rounded w-full py-2 px-3 text-slate-700 leading-tight focus:outline-none focus:border-slate-500 focus:ring-1 focus:ring-slate-500"
          />
        </div>

        <div className="mb-6">
          <label htmlFor="confirmPassword" className="block text-slate-700 text-sm font-medium mb-1">Confirmar Nueva Contraseña:</label>
          <input
            type="password"
            id="confirmPassword"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
            className="appearance-none border border-slate-300 rounded w-full py-2 px-3 text-slate-700 leading-tight focus:outline-none focus:border-slate-500 focus:ring-1 focus:ring-slate-500"
          />
        </div>

        <button type="submit" disabled={isSubmitting} className="w-full bg-slate-800 hover:bg-slate-700 text-white font-medium py-2.5 px-4 rounded focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-opacity-50 disabled:opacity-50">
          {isSubmitting ? 'Restableciendo...' : 'Restablecer Contraseña'}
        </button>
      </form>
    </div>
  );
};
export const confirmarResetPassword = async (uidb64, token, newPassword, confirmPassword) => {
  try {    
    const response = await axios.post(`${API_BASE_URL}/usuarios/password-reset-confirm/`, {
      uidb64,
      token,
      new_password: newPassword, // Asegúrate que los nombres de los campos coincidan con lo que espera tu backend
      confirm_password: confirmPassword,
    });
    return response.data; // Debería devolver un mensaje de éxito
  } catch (error) {
    console.error("Error en confirmarResetPassword API:", error.response || error);
    let errorMessage = 'Error al confirmar el restablecimiento de contraseña.';
    if (error.response && error.response.data) {
      // Intenta obtener un mensaje más específico del backend
      errorMessage = typeof error.response.data === 'string' ? error.response.data :
                     error.response.data.error || error.response.data.message || JSON.stringify(error.response.data);
    } else if (error.request) {
      errorMessage = 'No se pudo conectar con el servidor. Inténtalo de nuevo.';
    } else {
      errorMessage = error.message;
    }
    throw new Error(errorMessage);
  }
}
export default ResetPasswordConfirmForm;