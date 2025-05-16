import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { toast } from 'react-toastify'; // Importar toast
import { obtenerUsuario, actualizarUsuario, obtenerRoles } from '../../../api/admin'; // Necesitaremos obtenerUsuario y actualizarUsuario
import { obtenerSucursales } from '../../../api/sucursales';

const ROLES_CON_PERFIL_PERSONAL = ['Administrador', 'Vendedor', 'Bodeguero', 'Contador'];

function EditarUsuarioForm() {
  const { userId } = useParams(); // Obtener el ID del usuario de la URL
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    nombre_usuario: '',
    email: '',
    first_name: '',
    last_name: '',
    rol_id: '',
    is_active: true,
    rut_personal: '',
    sucursal_id_personal: '',
    // No incluimos password aquí, la actualización de contraseña debería ser un flujo separado
  });
  const [roles, setRoles] = useState([]);
  const [sucursales, setSucursales] = useState([]);
  const [selectedRolNombre, setSelectedRolNombre] = useState('');
  const [loading, setLoading] = useState(true); // Mantener loading para la carga inicial
  // const [error, setError] = useState(''); // Se reemplaza por toasts para errores de submit/carga de sucursales
  // const [successMessage, setSuccessMessage] = useState(''); // Se reemplaza por toasts

  useEffect(() => {
    const cargarDatosUsuario = async () => {
      try {
        setLoading(true);
        const [userDataResponse, rolesDataResponse] = await Promise.all([
          obtenerUsuario(userId), // Asegúrate de llamar a obtenerUsuario con el userId
          obtenerRoles()      // Y obtenerRoles para la lista de roles
        ]);

        setFormData({
          nombre_usuario: userDataResponse.nombre_usuario || '',
          email: userDataResponse.email || '',
          // No cargamos password aquí por seguridad
          first_name: userDataResponse.first_name || '',
          last_name: userDataResponse.last_name || '',
          rol_id: userDataResponse.rol?.id || '', // Usar el ID del rol
          is_active: userDataResponse.is_active,
          // Cargar datos de personal si existen
          rut_personal: userDataResponse.personal?.rut || '',
          sucursal_id_personal: userDataResponse.personal?.sucursal?.id || '',
        });
        setRoles(rolesDataResponse || []);

        const rolActual = rolesDataResponse.find(r => r.id === userDataResponse.rol?.id);
        setSelectedRolNombre(rolActual ? rolActual.nombre_rol : '');

      } catch (err) {
        console.error("Error cargando datos:", err);
        toast.error(err.message || 'Error al cargar datos del usuario o roles.');
      } finally {
        setLoading(false);
      }
    };
    cargarDatosUsuario();
  }, [userId]); // userId como dependencia para recargar si cambia

  useEffect(() => {
    const cargarSucursales = async () => {
      if (ROLES_CON_PERFIL_PERSONAL.includes(selectedRolNombre)) {
        try {
          const sucursalesData = await obtenerSucursales();
          setSucursales(sucursalesData || []);
        } catch (err) {
          // Si ya hay un error de carga principal, no mostrar otro toast por sucursales
          // o podrías decidir mostrarlo de todas formas.
          // Por simplicidad, mostraremos el error de sucursales también.
          console.error("Error cargando sucursales:", err);
          toast.error(err.message || 'Error al cargar sucursales.');
        }
      } else {
        setSucursales([]);
      }
    };
    if (selectedRolNombre) { // Solo cargar si ya tenemos un rol seleccionado
        cargarSucursales();
    }
  }, [selectedRolNombre]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));

    if (name === 'rol_id') {
      const rolSeleccionado = roles.find(r => r.id.toString() === value);
      setSelectedRolNombre(rolSeleccionado ? rolSeleccionado.nombre_rol : '');
      if (rolSeleccionado && !ROLES_CON_PERFIL_PERSONAL.includes(rolSeleccionado.nombre_rol)) {
        setFormData(prev => ({ ...prev, rut_personal: '', sucursal_id_personal: '' }));
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const { ...userDataToSubmit } = formData;

    if (!ROLES_CON_PERFIL_PERSONAL.includes(selectedRolNombre)) {
      delete userDataToSubmit.rut_personal;
      delete userDataToSubmit.sucursal_id_personal;
    } else {
      if (!userDataToSubmit.rut_personal) delete userDataToSubmit.rut_personal; // o enviar null
      if (!userDataToSubmit.sucursal_id_personal) delete userDataToSubmit.sucursal_id_personal; // o enviar null
    }

    if (userDataToSubmit.rol_id) {
        userDataToSubmit.rol_id = parseInt(userDataToSubmit.rol_id, 10);
    } else {
        delete userDataToSubmit.rol_id;
    }

    if (userDataToSubmit.sucursal_id_personal) {
        userDataToSubmit.sucursal_id_personal = parseInt(userDataToSubmit.sucursal_id_personal, 10);
    }

    try {
      console.log("Enviando datos para actualizar usuario:", userId, userDataToSubmit);
      const response = await actualizarUsuario(userId, userDataToSubmit);
      toast.success(response.message || 'Usuario actualizado exitosamente. Redirigiendo...');
      setTimeout(() => {
        navigate('/admin/gestion-usuarios');
      }, 2000);
    } catch (err) {
      console.error("Error en handleSubmit (actualizar):", err);
      toast.error(err.message || 'Error al actualizar el usuario.');
    }
  };

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Cargando datos del usuario...</div>;
  }

  const necesitaPerfilPersonal = ROLES_CON_PERFIL_PERSONAL.includes(selectedRolNombre);

  return (
    <div className="min-h-screen bg-slate-100 p-4 sm:p-6 md:p-8">
      <header className="mb-6">
        <h1 className="text-2xl sm:text-3xl font-bold text-slate-800 mb-2">Editar Usuario: {formData.nombre_usuario}</h1>
        <Link to="/admin/gestion-usuarios" className="text-sm text-slate-600 hover:text-slate-800 hover:underline">
          &larr; Volver a Gestión de Usuarios
        </Link>
      </header>
      <main className="bg-white p-6 rounded-lg shadow max-w-2xl mx-auto">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="nombre_usuario" className="block text-sm font-medium text-slate-700 mb-1">Nombre de Usuario:</label>
            <input type="text" name="nombre_usuario" id="nombre_usuario" value={formData.nombre_usuario} onChange={handleChange} className="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md shadow-sm placeholder-slate-400 focus:outline-none focus:ring-slate-500 focus:border-slate-500 sm:text-sm" required />
          </div>
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-slate-700 mb-1">Email:</label>
            <input type="email" name="email" id="email" value={formData.email} onChange={handleChange} className="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md shadow-sm placeholder-slate-400 focus:outline-none focus:ring-slate-500 focus:border-slate-500 sm:text-sm" required />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="first_name" className="block text-sm font-medium text-slate-700 mb-1">Nombres:</label>
              <input type="text" name="first_name" id="first_name" value={formData.first_name} onChange={handleChange} className="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md shadow-sm placeholder-slate-400 focus:outline-none focus:ring-slate-500 focus:border-slate-500 sm:text-sm" />
            </div>
            <div>
              <label htmlFor="last_name" className="block text-sm font-medium text-slate-700 mb-1">Apellidos:</label>
              <input type="text" name="last_name" id="last_name" value={formData.last_name} onChange={handleChange} className="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md shadow-sm placeholder-slate-400 focus:outline-none focus:ring-slate-500 focus:border-slate-500 sm:text-sm" />
            </div>
          </div>
          <div>
            <label htmlFor="rol_id" className="block text-sm font-medium text-slate-700 mb-1">Rol:</label>
            <select name="rol_id" id="rol_id" value={formData.rol_id} onChange={handleChange} className="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-slate-500 focus:border-slate-500 sm:text-sm" required>
              <option value="">Seleccione un rol</option>
              {roles.map(rol => (
                <option key={rol.id} value={rol.id}>{rol.nombre_rol}</option>
              ))}
            </select>
          </div>
          <div className="flex items-center">
            <input type="checkbox" name="is_active" id="is_active" checked={formData.is_active} onChange={handleChange} className="h-4 w-4 text-slate-600 border-slate-300 rounded focus:ring-slate-500" />
            <label htmlFor="is_active" className="ml-2 block text-sm text-slate-900">Usuario Activo</label>
          </div>

          {necesitaPerfilPersonal && (
            <div className="space-y-6 border-t border-slate-200 pt-6">
              <h5 className="text-lg font-medium text-slate-900">Datos del Personal</h5>
              <div>
                <label htmlFor="rut_personal" className="block text-sm font-medium text-slate-700 mb-1">RUT del Personal:</label>
                <input type="text" name="rut_personal" id="rut_personal" value={formData.rut_personal} onChange={handleChange} className="mt-1 block w-full px-3 py-2 bg-slate-50 border border-slate-300 rounded-md shadow-sm placeholder-slate-400 focus:outline-none focus:ring-slate-500 focus:border-slate-500 sm:text-sm" readOnly />

              </div>
              <div>
                <label htmlFor="sucursal_id_personal" className="block text-sm font-medium text-slate-700 mb-1">Sucursal:</label>
                <select name="sucursal_id_personal" id="sucursal_id_personal" value={formData.sucursal_id_personal} onChange={handleChange} className="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-slate-500 focus:border-slate-500 sm:text-sm">
                  <option value="">Seleccione una sucursal (opcional)</option>
                  {sucursales.map(sucursal => (
                    <option key={sucursal.id} value={sucursal.id}>{sucursal.nombre_sucursal}</option>
                  ))}
                </select>
              </div>
            </div>
          )}
          <div className="flex flex-col sm:flex-row gap-4 pt-4">
            <button type="button" onClick={() => navigate('/admin/gestion-usuarios')} className="w-full sm:w-auto flex justify-center py-2 px-4 border border-slate-300 rounded-md shadow-sm text-sm font-medium text-slate-700 bg-white hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-500">
              Cancelar
            </button>
            <button type="submit" className="w-full sm:w-auto flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-slate-700 hover:bg-slate-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-500">
              Guardar Cambios
            </button>
          </div>
        </form>
      </main>
    </div>
  );
}

export default EditarUsuarioForm;