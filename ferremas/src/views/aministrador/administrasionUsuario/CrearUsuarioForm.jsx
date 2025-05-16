import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom'; // Importar Link
import { toast } from 'react-toastify'; // Importar toast
import { crearUsuarioAdmin, obtenerRoles } from '../../../api/admin'; // Asumiendo que estas funciones están en admin.js
import { obtenerSucursales } from '../../../api/sucursales'; // Necesitarás crear esta función API

const ROLES_CON_PERFIL_PERSONAL = ['Administrador', 'Vendedor', 'Bodeguero', 'Contador']; // Asegúrate que coincidan con el backend

function CrearUsuarioForm() {
  const [formData, setFormData] = useState({
    nombre_usuario: '',
    email: '',
    password: '',
    confirm_password: '',
    first_name: '',
    last_name: '',
    rol_id: '',
    is_active: true,
    // Campos para el perfil de Personal (opcionales)
    rut_personal: '',
    sucursal_id_personal: '',
  });
  const [roles, setRoles] = useState([]);
  const [sucursales, setSucursales] = useState([]);
  const [selectedRolNombre, setSelectedRolNombre] = useState('');
  const [rutError, setRutError] = useState(''); // Estado para el error del RUT
  const [emailError, setEmailError] = useState(''); // Estado para el error del email
  // const [error, setError] = useState(''); // Se reemplaza por toasts
  // const [successMessage, setSuccessMessage] = useState(''); // Se reemplaza por toasts
  const navigate = useNavigate();

  // Función para validar el formato del RUT Chileno
  const validarRutChileno = (rut) => {
    if (!rut) return ''; // No hay error si está vacío (a menos que sea obligatorio)
    const rutPattern = /^\d{1,8}-[\dkK]$/;
    if (!rutPattern.test(rut)) {
      return 'Formato de RUT inválido. Ejemplo: 12345678-9 o 12345678-K';
    }
    return ''; // Sin error
  };

  // Función para validar el formato del Email
  const validarEmail = (email) => {
    if (!email) return ''; // No hay error si está vacío (a menos que sea obligatorio)
    // Expresión regular simple para formato de email
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
      return 'Formato de email inválido.';
    }
    return ''; // Sin error
  };
  useEffect(() => {
    const cargarRoles = async () => {
      try {
        const rolesData = await obtenerRoles();
        setRoles(rolesData || []); // Asegura que rolesData no sea undefined
      } catch (err) {
        toast.error(err.message || 'Error al cargar roles');
      }
    };
    cargarRoles();
  }, []);

  useEffect(() => {
    const cargarSucursales = async () => {
      if (ROLES_CON_PERFIL_PERSONAL.includes(selectedRolNombre)) {
        try {
          const sucursalesData = await obtenerSucursales(); // Asume que esta función devuelve un array
          setSucursales(sucursalesData || []);
        } catch (err) {
          toast.error(err.message || 'Error al cargar sucursales');
        }
      } else {
        setSucursales([]); // Limpiar sucursales si el rol no requiere perfil de personal
      }
    };
    cargarSucursales();
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
      // Limpiar campos de personal si el rol no lo requiere
      if (rolSeleccionado && !ROLES_CON_PERFIL_PERSONAL.includes(rolSeleccionado.nombre_rol)) {
        setFormData(prev => ({
          ...prev,
          rut_personal: '',
          sucursal_id_personal: '',
        }));
      }
    }

    // Validar RUT en tiempo real mientras se escribe
    if (name === 'rut_personal') {
      const error = validarRutChileno(value);
      setRutError(error);
    }

    // Validar Email en tiempo real mientras se escribe
    if (name === 'email') {
      const error = validarEmail(value);
      setEmailError(error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.password !== formData.confirm_password) {
      toast.error('Las contraseñas no coinciden.');
      return;
    }

    // Validar Email antes de enviar
    const emailValidationError = validarEmail(formData.email);
    if (emailValidationError) {
      console.log("VALIDATION FAIL: Email format - ", emailValidationError); // DEBUG
      setEmailError(emailValidationError);
      toast.error(emailValidationError);
      return; // Detener el envío
    } else {
      setEmailError(''); // Limpiar error si es válido
    }
    
    // Validar RUT si el rol lo requiere
    if (necesitaPerfilPersonal) {
      if (!formData.rut_personal) { // RUT es requerido pero está vacío
        const errorMsg = 'El RUT del personal es requerido para este rol.';
        console.log("VALIDATION FAIL: RUT required - ", errorMsg); // DEBUG
        setRutError(errorMsg);
        toast.error(errorMsg);
        return; // Detener el envío
      } else { // RUT tiene valor, validar formato
        const rutFormatError = validarRutChileno(formData.rut_personal);
        if (rutFormatError) {
          console.log("VALIDATION FAIL: RUT format - ", rutFormatError); // DEBUG
          setRutError(rutFormatError);
          toast.error(rutFormatError);
          return; // Detener el envío
        }
      }
    } else { // Si no necesita perfil personal, limpiar error de RUT
      setRutError('');
    }

    // Validar si la sucursal es requerida y no está seleccionada
    if (necesitaPerfilPersonal && !formData.sucursal_id_personal) { // Simplificada la condición
      const errorMsg = 'Debe seleccionar una sucursal para este rol.';
      console.log("VALIDATION FAIL: Sucursal required - ", errorMsg); // DEBUG
      toast.error(errorMsg);
        return; // Detener el envío
      }

    // Prepara los datos a enviar, excluyendo confirm_password
    // y solo incluyendo campos de personal si son necesarios y tienen valor
    const { confirm_password, ...userDataToSubmit } = formData;

    if (!ROLES_CON_PERFIL_PERSONAL.includes(selectedRolNombre)) {
      delete userDataToSubmit.rut_personal;
      delete userDataToSubmit.sucursal_id_personal;
    } else {
      // Asegurarse de que los campos de personal solo se envíen si tienen valor
      // y el rol lo requiere. El backend espera null si no se provee.
      if (!userDataToSubmit.rut_personal) delete userDataToSubmit.rut_personal;
      if (!userDataToSubmit.sucursal_id_personal) delete userDataToSubmit.sucursal_id_personal;
    }
    
    // Convertir rol_id y sucursal_id_personal a número si tienen valor, o enviar null/undefined
    if (userDataToSubmit.rol_id) {
        userDataToSubmit.rol_id = parseInt(userDataToSubmit.rol_id, 10);
    } else {
        delete userDataToSubmit.rol_id; // O enviar null si el backend lo prefiere para "sin rol"
    }

    if (userDataToSubmit.sucursal_id_personal) {
        userDataToSubmit.sucursal_id_personal = parseInt(userDataToSubmit.sucursal_id_personal, 10);
    } else if (ROLES_CON_PERFIL_PERSONAL.includes(selectedRolNombre)) {
        // Si el rol requiere personal pero no se seleccionó sucursal,
        // podrías enviar null o dejar que el backend lo maneje si es opcional.
        // Por ahora, si no hay valor, no se envía (delete userDataToSubmit.sucursal_id_personal; ya lo hizo)
    }


    try {
      console.log("Enviando datos para crear usuario:", userDataToSubmit);
      const response = await crearUsuarioAdmin(userDataToSubmit);
      toast.success(response.message || 'Usuario creado exitosamente. Redirigiendo...');
      setTimeout(() => {
        navigate('/admin/gestion-usuarios'); // O a donde quieras redirigir
      }, 2000);
    } catch (err) {
      console.error("Error en handleSubmit:", err);
      let displayMessage = 'Error al crear el usuario. Inténtalo de nuevo.'; // Mensaje genérico por defecto
      if (err && err.message) {
        const backendMessage = String(err.message);
        console.log("Backend error message:", backendMessage); // DEBUG
        // Intentar mostrar un mensaje más específico si es por duplicado
        if (backendMessage.toLowerCase().includes("email already exists")) {
          displayMessage = "El correo electrónico ingresado ya existe.";
        } else if (backendMessage.toLowerCase().includes("nombre usuario already exists")) { // Ajusta "nombre usuario" si la clave del backend es diferente
          displayMessage = "El nombre de usuario ingresado ya existe.";
        } // Podrías añadir más condiciones para otros errores comunes del backend
      }
      toast.error(displayMessage);
    }
  };

  const necesitaPerfilPersonal = ROLES_CON_PERFIL_PERSONAL.includes(selectedRolNombre);

  return (
    <div className="min-h-screen bg-slate-100 p-4 sm:p-6 md:p-8">
      <header className="mb-6">
        <h1 className="text-2xl sm:text-3xl font-bold text-slate-800 mb-2">Crear Nuevo Usuario</h1>
        <Link to="/admin/gestion-usuarios" className="text-sm text-slate-600 hover:text-slate-800 hover:underline">
          &larr; Volver a Gestión de Usuarios
        </Link>
      </header>
      <main className="bg-white p-6 rounded-lg shadow max-w-2xl mx-auto">
        {/* Los mensajes de error y éxito ahora se manejan con toasts */}
        {/* {error && <div className="mb-4 p-3 rounded bg-red-100 text-red-700 text-sm">{error}</div>} */}
        {/* {successMessage && <div className="mb-4 p-3 rounded bg-green-100 text-green-700 text-sm">{successMessage}</div>} */}
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Campos del Usuario */}
          <div>
            <label htmlFor="nombre_usuario" className="block text-sm font-medium text-slate-700 mb-1">Nombre de Usuario:</label>
            <input type="text" name="nombre_usuario" id="nombre_usuario" value={formData.nombre_usuario} onChange={handleChange} className="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md shadow-sm placeholder-slate-400 focus:outline-none focus:ring-slate-500 focus:border-slate-500 sm:text-sm" required />
          </div>
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-slate-700 mb-1">Email:</label>
            <input type="email" name="email" id="email" value={formData.email} onChange={handleChange} className="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md shadow-sm placeholder-slate-400 focus:outline-none focus:ring-slate-500 focus:border-slate-500 sm:text-sm" required />
            {emailError && <p className="mt-1 text-xs text-red-600">{emailError}</p>}
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
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-slate-700 mb-1">Contraseña:</label>
              <input type="password" name="password" id="password" value={formData.password} onChange={handleChange} className="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md shadow-sm placeholder-slate-400 focus:outline-none focus:ring-slate-500 focus:border-slate-500 sm:text-sm" required minLength="8" />
            </div>
            <div>
              <label htmlFor="confirm_password" className="block text-sm font-medium text-slate-700 mb-1">Confirmar Contraseña:</label>
              <input type="password" name="confirm_password" id="confirm_password" value={formData.confirm_password} onChange={handleChange} className="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md shadow-sm placeholder-slate-400 focus:outline-none focus:ring-slate-500 focus:border-slate-500 sm:text-sm" required />
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

          {/* Campos del Perfil de Personal (condicional) */}
          {necesitaPerfilPersonal && (
            <div className="space-y-6 border-t border-slate-200 pt-6">
              <h5 className="text-lg font-medium text-slate-900">Datos del Personal</h5>
              <div>
                <label htmlFor="rut_personal" className="block text-sm font-medium text-slate-700 mb-1">RUT del Personal:</label>
                <input type="text" name="rut_personal" id="rut_personal" value={formData.rut_personal} onChange={handleChange} className="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md shadow-sm placeholder-slate-400 focus:outline-none focus:ring-slate-500 focus:border-slate-500 sm:text-sm" />
                {rutError && <p className="mt-1 text-xs text-red-600">{rutError}</p>}
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
            <button 
              type="button" 
              onClick={() => navigate('/admin/gestion-usuarios')}
              className="w-full sm:w-auto flex justify-center py-2 px-4 border border-slate-300 rounded-md shadow-sm text-sm font-medium text-slate-700 bg-white hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-500"
            >
              Cancelar
            </button>
            <button type="submit" className="w-full sm:w-auto flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-slate-700 hover:bg-slate-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-500">
              Crear Usuario
            </button>
          </div>
        </form>
      </main>
    </div>
  );
}

export default CrearUsuarioForm;
