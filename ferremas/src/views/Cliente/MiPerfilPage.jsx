import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../components/AuthContext';
import { toast } from 'react-toastify';
// Importaciones actualizadas para Heroicons v2 (ejemplo con outline de 24px)
import { UserCircleIcon } from '@heroicons/react/24/outline';
import { EnvelopeIcon } from '@heroicons/react/24/outline'; // MailIcon se llama EnvelopeIcon en v2
// import { PhoneIcon } from '@heroicons/react/24/outline'; // Descomentar si se añade teléfono
import { Cog6ToothIcon } from '@heroicons/react/24/outline'; // CogIcon se llama Cog6ToothIcon en v2 (o similar)
// Asumimos que tendrás una función para actualizar el perfil en tu API
import { actualizarPerfilUsuario } from '../../api/usuarios'; // Importar la función API

const MiPerfilPage = () => {
  const { currentUser, updateUserProfile } = useAuth(); // Usar la nueva función del contexto
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    // email: '', // El email usualmente no se cambia tan fácilmente o requiere verificación
    // telefono: '', // Si añades teléfono
  });
  const [loadingUpdate, setLoadingUpdate] = useState(false);


  if (!currentUser) {
    return (
      <div className="container mx-auto p-4 sm:p-6 lg:p-8 text-center">
        <p>Cargando información del perfil...</p>
        <p className="mt-2 text-sm text-slate-500">Si este mensaje persiste, intenta <Link to="/login" className="text-sky-600 hover:underline">iniciar sesión</Link> de nuevo.</p>
      </div>
    );
  }

  // Sincronizar formData con currentUser cuando currentUser cambie o al entrar en modo edición
  useEffect(() => {
    if (currentUser) {
      setFormData({
        first_name: currentUser.first_name || '',
        last_name: currentUser.last_name || '',
        // email: currentUser.email || '',
        // telefono: currentUser.cliente_profile?.telefono || '', // Ajustar según tu estructura
      });
    }
  }, [currentUser, isEditing]); // Se ejecuta si currentUser cambia o si isEditing cambia

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoadingUpdate(true);
    try {
      // Solo envía los campos que quieres permitir actualizar.
      // El backend debería ignorar campos no permitidos o no enviados.
      const datosParaActualizar = {
        first_name: formData.first_name,
        last_name: formData.last_name,
      };
      const usuarioActualizado = await actualizarPerfilUsuario(datosParaActualizar);
      console.log("Respuesta del backend (usuarioActualizado):", usuarioActualizado);

      updateUserProfile(usuarioActualizado); // Llama a la función del contexto que también actualiza localStorage

      toast.success('Perfil actualizado con éxito.');
      setIsEditing(false);
    } catch (error) {
      toast.error(error.message || 'Error al actualizar el perfil.');
      console.error("Error al actualizar perfil:", error);
    } finally {
      setLoadingUpdate(false);
    }
  };

  // Ejemplo de campos a mostrar. Ajusta según los datos disponibles en currentUser
  const profileData = [
    { label: 'Nombre de Usuario', value: currentUser.nombre_usuario, icon: UserCircleIcon }, // UserCircleIcon es correcto
    { label: 'Email', value: currentUser.email, icon: EnvelopeIcon }, // Cambiado a EnvelopeIcon
    { label: 'Nombres', value: currentUser.first_name || 'No especificado', icon: UserCircleIcon },
    { label: 'Apellidos', value: currentUser.last_name || 'No especificado', icon: UserCircleIcon },
    { label: 'Rol', value: currentUser.rol?.nombre_rol || 'No especificado', icon: Cog6ToothIcon }, // Cambiado a Cog6ToothIcon
  ];

  return (
    <div className="container mx-auto p-4 sm:p-6 lg:p-8">
      <h1 className="text-3xl font-bold text-slate-800 mb-8 text-center">Mi Perfil</h1>
      
      <div className="bg-white max-w-2xl mx-auto p-6 sm:p-8 rounded-lg shadow-xl">
        <div className="flex flex-col items-center mb-8">
          <UserCircleIcon className="h-24 w-24 text-slate-500 mb-4" />
          <h2 className="text-2xl font-semibold text-slate-700">{currentUser.nombre_usuario}</h2>
          <p className="text-slate-500">{currentUser.email}</p>
        </div>

        {isEditing ? (
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="first_name" className="block text-sm font-medium text-slate-700 mb-1">Nombres</label>
              <input
                type="text"
                name="first_name"
                id="first_name"
                value={formData.first_name}
                onChange={handleChange}
                className="w-full p-3 border border-slate-300 rounded-md focus:ring-sky-500 focus:border-sky-500"
              />
            </div>
            <div>
              <label htmlFor="last_name" className="block text-sm font-medium text-slate-700 mb-1">Apellidos</label>
              <input
                type="text"
                name="last_name"
                id="last_name"
                value={formData.last_name}
                onChange={handleChange}
                className="w-full p-3 border border-slate-300 rounded-md focus:ring-sky-500 focus:border-sky-500"
              />
            </div>
            {/* Podrías añadir campo de teléfono aquí si lo gestionas */}
            {/* <div>
              <label htmlFor="telefono" className="block text-sm font-medium text-slate-700 mb-1">Teléfono</label>
              <input type="tel" name="telefono" id="telefono" value={formData.telefono} onChange={handleChange} className="w-full p-3 border border-slate-300 rounded-md focus:ring-sky-500 focus:border-sky-500" />
            </div> */}
            <div className="flex flex-col sm:flex-row gap-3 pt-4">
              <button type="submit" disabled={loadingUpdate} className="w-full sm:w-auto bg-sky-500 hover:bg-sky-600 text-white font-semibold py-2 px-6 rounded-lg transition duration-150 ease-in-out disabled:opacity-50">
                {loadingUpdate ? 'Guardando...' : 'Guardar Cambios'}
              </button>
              <button type="button" onClick={() => setIsEditing(false)} className="w-full sm:w-auto bg-slate-200 hover:bg-slate-300 text-slate-700 font-semibold py-2 px-6 rounded-lg transition duration-150 ease-in-out">
                Cancelar
              </button>
            </div>
          </form>
        ) : (
          <>
            <div className="space-y-4">
              {profileData.map((item, index) => (
                <div key={index} className="flex items-start py-3 border-b border-slate-200 last:border-b-0">
                  {item.icon && <item.icon className="h-6 w-6 text-sky-600 mr-4 mt-1 flex-shrink-0" />}
                  <div className="flex-grow">
                    <p className="text-sm font-medium text-slate-500">{item.label}</p>
                    <p className="text-slate-700 text-lg">{item.value}</p>
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-10 text-center">
              <button onClick={() => setIsEditing(true)} className="bg-sky-500 hover:bg-sky-600 text-white font-semibold py-2 px-6 rounded-lg mr-2">Editar Perfil</button>
              {/* <button className="bg-slate-500 hover:bg-slate-600 text-white font-semibold py-2 px-6 rounded-lg">Cambiar Contraseña</button> */}
            </div>
          </>
        )}
              </div>
    </div>
  );
};

export default MiPerfilPage;