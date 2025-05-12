import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { solicitarResetPassword } from '../../api/recuperar_contraseña'; // Cambiado para importar la función correcta

function RecuperarPasswordForm() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');
    setIsSubmitting(true);

    if (!email) {
      setError('Por favor, ingresa tu correo electrónico.');
      setIsSubmitting(false);
      return;
    }

    try {
      const response = await solicitarResetPassword(email); // Llama a tu función API
      setMessage(response.message || 'Si existe una cuenta con este correo, recibirás un email con instrucciones para restablecer tu contraseña.');
      setEmail(''); // Limpiar el campo
    } catch (err) {
      console.error("Error al solicitar restablecimiento:", err);
      setError(err.message || 'Ocurrió un error al procesar tu solicitud. Inténtalo más tarde.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 p-4">
      <form onSubmit={handleSubmit} className="bg-white p-6 sm:p-8 rounded-lg shadow-sm w-full max-w-md">
        <h2 className="text-xl sm:text-2xl font-semibold text-center text-slate-800 mb-8">Recuperar Contraseña</h2>

        {error && <p className="bg-red-50 text-red-600 px-3 py-2 rounded mb-4 text-xs sm:text-sm" role="alert">{error}</p>}
        {message && <p className="bg-green-50 text-green-700 px-3 py-2 rounded mb-4 text-xs sm:text-sm" role="alert">{message}</p>}

        <div className="mb-4">
          <label htmlFor="email" className="block text-slate-700 text-sm font-medium mb-1">Correo Electrónico:</label>
          <input
            type="email"
            name="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="appearance-none border border-slate-300 rounded w-full py-2 px-3 text-slate-700 leading-tight focus:outline-none focus:border-slate-500 focus:ring-1 focus:ring-slate-500"
          />
        </div>

        <button type="submit" disabled={isSubmitting} className="w-full bg-slate-800 hover:bg-slate-700 text-white font-medium py-2.5 px-4 rounded focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-opacity-50 disabled:opacity-50">
          {isSubmitting ? 'Enviando...' : 'Enviar Enlace de Restablecimiento'}
        </button>

        <p className="text-center text-sm text-slate-600 mt-6">
          <Link to="/login" className="font-medium text-slate-800 hover:underline">Volver a Iniciar Sesión</Link>
        </p>
      </form>
    </div>
  );
}

export default RecuperarPasswordForm;