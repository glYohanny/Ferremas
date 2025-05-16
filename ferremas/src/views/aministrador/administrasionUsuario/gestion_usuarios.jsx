import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify'; // Importar toast
import { obtenerUsuarios, eliminarUsuario, actualizarEstadoUsuario } from '../../../api/admin'; // Importar nuevas funciones API

function GestionUsuariosPage({ currentUser }) { // Aceptar currentUser como prop
  const [usuarios, setUsuarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  // const [error, setError] = useState(''); // Se reemplaza por toasts

  useEffect(() => {
    const cargarUsuarios = async () => {
      try {
        setLoading(true);
        const data = await obtenerUsuarios();
        // DRF a veces pagina los resultados, o puede devolver un array directamente.
        // Ajusta según la estructura de respuesta de tu API.
        setUsuarios(Array.isArray(data) ? data : (data.results || []));
      } catch (err) {
        console.error("Error cargando usuarios:", err);
        toast.error(err.message || 'No se pudieron cargar los usuarios.');
      } finally {
        setLoading(false);
      }
    };

    cargarUsuarios();
  }, []);

  const handleToggleActivo = async (usuarioId, isActive) => {
    if (!window.confirm(`¿Estás seguro de que quieres ${isActive ? 'desactivar' : 'activar'} este usuario?`)) {
      return;
    }
    try {
      await actualizarEstadoUsuario(usuarioId, !isActive);
      setUsuarios(prevUsuarios =>
        prevUsuarios.map(u =>
          u.id === usuarioId ? { ...u, is_active: !isActive } : u
        )
      );
      toast.success(`Usuario ${isActive ? 'desactivado' : 'activado'} correctamente.`);
    } catch (err) {
      toast.error(err.message || 'Error al cambiar el estado del usuario.');
    }
  };

  const handleEliminarUsuario = async (usuarioId) => {
    if (!window.confirm('¿Estás seguro de que quieres eliminar este usuario? Esta acción no se puede deshacer.')) {
      return;
    }
    try {
      await eliminarUsuario(usuarioId);
      setUsuarios(prevUsuarios => prevUsuarios.filter(u => u.id !== usuarioId));
      toast.success('Usuario eliminado correctamente.');
    } catch (err) {
      // Si el error es porque el usuario no puede ser eliminado (ej. tiene registros asociados y hay PROTECT)
      // el backend debería devolver un error específico.
      toast.error(err.message || 'Error al eliminar el usuario.');
    }
  };


  return (
    <div className="min-h-screen bg-slate-100 p-4 sm:p-6 md:p-8">
      <header className="mb-6">
        <div className="flex justify-between items-center mb-2">
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-800">Gestión de Usuarios</h1>
          <button
            onClick={() => navigate('/admin/gestion-usuarios/crear')}
            className="bg-slate-700 hover:bg-slate-600 text-white font-medium py-2 px-4 rounded text-sm">
            Crear Nuevo Usuario
          </button>
        </div>
        <Link to="/" className="text-sm text-slate-600 hover:text-slate-800 hover:underline">
          &larr; Volver al Panel de Administración
        </Link>
      </header>
      <main className="bg-white p-6 rounded-lg shadow">
        {loading && <p className="text-slate-700 text-center py-4">Cargando usuarios...</p>}
        {/* El mensaje de error de carga general ahora se maneja con toast, pero podrías mantener uno aquí si prefieres */}
        {/* {error && <p className="text-red-600 bg-red-100 p-3 rounded text-center">{error}</p>} */}
        {/* Se ajusta la condición para no depender del estado 'error' que fue removido */}
        {!loading && (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-200">
              <thead className="bg-slate-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">ID</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Nombre Usuario</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Email</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Nombre Completo</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Rol</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Activo</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Acciones</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-slate-200">
                {usuarios.length > 0 ? usuarios.map((usuario) => (
                  <tr key={usuario.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">{usuario.id}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-900">{usuario.nombre_usuario}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">{usuario.email}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">{`${usuario.first_name || ''} ${usuario.last_name || ''}`.trim() || '-'}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">{usuario.rol?.nombre_rol || 'No asignado'}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      {usuario.is_active ?
                        <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">Activo</span> :
                        <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">Inactivo</span>
                      }
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <Link to={`/admin/gestion-usuarios/editar/${usuario.id}`} className="text-indigo-600 hover:text-indigo-900 mr-3">Editar</Link>
                      <button
                        disabled={currentUser && currentUser.id === usuario.id}
                        onClick={() => handleToggleActivo(usuario.id, usuario.is_active)}
                        className={`mr-3 ${usuario.is_active ? 'text-yellow-600 hover:text-yellow-900' : 'text-green-600 hover:text-green-900'} ${currentUser && currentUser.id === usuario.id ? 'opacity-50 cursor-not-allowed' : ''}`}
                      >
                        {usuario.is_active ? 'Desactivar' : 'Activar'}
                      </button>
                      <button
                        disabled={currentUser && currentUser.id === usuario.id}
                        onClick={() => handleEliminarUsuario(usuario.id)}
                        className={`text-red-600 hover:text-red-900 ${currentUser && currentUser.id === usuario.id ? 'opacity-50 cursor-not-allowed' : ''}`}
                      >
                        Eliminar
                      </button>
                    </td>
                  </tr>
                )) : (
                  <tr><td colSpan="7" className="px-6 py-4 text-center text-sm text-slate-500">No hay usuarios para mostrar.</td></tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  );
}

export default GestionUsuariosPage;