import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../../components/componets_CarritoCompra'; // Ajusta la ruta si es diferente
import { crearPedido } from '../../api/pedidos';
import { getRegiones, getComunas } from '../../api/geografia'; // Para selectores de región y comuna
import { toast } from 'react-toastify';
import { useAuth } from '../../components/AuthContext'; // Para obtener datos del usuario logueado

const CheckoutPage = () => {
  const { cartItems, getCartTotal, clearCart, getCartItemCount } = useCart();
  const { currentUser } = useAuth(); // Obtener usuario actual
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    // Usar los campos del backend y datos del usuario si existen
    nombre_completo_contacto: currentUser?.cliente_profile?.nombre_completo_display || currentUser?.first_name || currentUser?.nombre_usuario || '',
    email_contacto: currentUser?.email || '',
    telefono_contacto: '',
    direccion_envio: '',
    region_id: '', // ID de la región seleccionada
    comuna_envio_id: '', // Coincide con el backend
    estado_pedido_id: '',
    tipo_entrega_id: '',
    metodo_pago_id: '',
    // nota_adicional: '', // Opcional
  });
  const [regiones, setRegiones] = useState([]);
  const [comunas, setComunas] = useState([]);
  const [estadosPedido, setEstadosPedido] = useState([]);
  const [tiposEntrega, setTiposEntrega] = useState([]);
  const [metodosPago, setMetodosPago] = useState([]);

  const [loadingRegiones, setLoadingRegiones] = useState(false);
  const [loadingComunas, setLoadingComunas] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [loadingOpciones, setLoadingOpciones] = useState(false);

  useEffect(() => {
    if (cartItems.length === 0 && !isSubmitting) { // Evitar redirección si se está enviando
      toast.info('Tu carrito está vacío. Redirigiendo al catálogo...');
      navigate('/');
    }
  }, [cartItems, navigate, isSubmitting]);

  useEffect(() => {
    const cargarRegiones = async () => {
      setLoadingRegiones(true);
      try {
        const data = await getRegiones();
        setRegiones(data || []);
      } catch (error) {
        toast.error('Error al cargar las regiones.');
      } finally {
        setLoadingRegiones(false);
      }
    };
    cargarRegiones();
  }, []);

  // Efecto para actualizar formData con datos de currentUser cuando esté disponible
  // y los campos correspondientes en formData estén vacíos (para no sobrescribir la entrada del usuario)
  useEffect(() => {
    if (currentUser) {
      setFormData(prevFormData => ({
        ...prevFormData,
        nombre_completo_contacto: prevFormData.nombre_completo_contacto || 
                                 currentUser?.cliente_profile?.nombre_completo_display || 
                                 currentUser?.first_name || 
                                 currentUser?.nombre_usuario || '',
        email_contacto: prevFormData.email_contacto || currentUser?.email || '',
      }));
    }
  }, [currentUser]); // Se ejecuta cuando currentUser cambia

  // Cargar opciones para los nuevos selectores (estado pedido, tipo entrega, método pago)
  useEffect(() => {
    const cargarOpcionesAdicionales = async () => {
      setLoadingOpciones(true);
      try {
        // Asumimos que estas funciones existen en api/pedidos.js o similar
        const { getEstadosPedido, getTiposEntrega, getMetodosPago } = await import('../../api/pedidos');
        const [estadosData, tiposData, metodosData] = await Promise.all([
          getEstadosPedido(),
          getTiposEntrega(),
          getMetodosPago(),
        ]);
        setEstadosPedido(estadosData || []);
        setTiposEntrega(tiposData || []);
        setMetodosPago(metodosData || []);

        // Opcional: Preseleccionar el primer valor si existe y el campo está vacío
        if (estadosData?.length > 0 && !formData.estado_pedido_id) {
          setFormData(prev => ({ ...prev, estado_pedido_id: estadosData[0].id }));
        }
        if (tiposData?.length > 0 && !formData.tipo_entrega_id) {
          setFormData(prev => ({ ...prev, tipo_entrega_id: tiposData[0].id }));
        }
        if (metodosData?.length > 0 && !formData.metodo_pago_id) {
          setFormData(prev => ({ ...prev, metodo_pago_id: metodosData[0].id }));
        }
      } catch (error) {
        toast.error('Error al cargar opciones del pedido.');
      } finally {
        setLoadingOpciones(false);
      }
    };
    cargarOpcionesAdicionales();
  }, []); // El array de dependencias vacío asegura que se ejecute solo una vez al montar

  useEffect(() => {
    if (formData.region_id) {
      const cargarComunas = async () => {
        setLoadingComunas(true);
        setFormData(prev => ({ ...prev, comuna_envio_id: '' })); // Resetear comuna seleccionada
        try {
          const data = await getComunas(formData.region_id);
          setComunas(data || []);
        } catch (error) {
          toast.error('Error al cargar las comunas para la región seleccionada.');
        } finally {
          setLoadingComunas(false);
        }
      };
      cargarComunas();
    } else {
      setComunas([]); // Si no hay región seleccionada, no mostrar comunas
    } // No es necesario limpiar setComunas([]) aquí si ya se hace arriba al cambiar region_id.
  }, [formData.region_id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    if (!formData.comuna_envio_id) { // Validar comuna_envio_id
        toast.error('Por favor, selecciona una región y una comuna.');
        setIsSubmitting(false);
        return;
    }
    if (!formData.estado_pedido_id || !formData.tipo_entrega_id || !formData.metodo_pago_id) {
        toast.error('Por favor, selecciona estado de pedido, tipo de entrega y método de pago.');
        setIsSubmitting(false);
        return;
    }

    const pedidoData = {
      nombre_completo_contacto: formData.nombre_completo_contacto,
      email_contacto: formData.email_contacto,
      telefono_contacto: formData.telefono_contacto,
      direccion_envio: formData.direccion_envio,
      comuna_envio_id: formData.comuna_envio_id,
      estado_pedido_id: formData.estado_pedido_id,
      tipo_entrega_id: formData.tipo_entrega_id,
      metodo_pago_id: formData.metodo_pago_id,
      items_input: cartItems.map(item => ({ producto_id: item.id, cantidad: item.quantity })), // Coincide con el backend
    };

    try {
      const pedidoCreado = await crearPedido(pedidoData);
      toast.success(`¡Pedido #${pedidoCreado.id || ''} realizado con éxito!`); // Asumiendo que el backend devuelve el ID del pedido
      clearCart();
      // Podrías redirigir a una página de confirmación de pedido
      // navigate(`/pedido-confirmado/${pedidoCreado.id}`);
      navigate('/'); // Por ahora, redirigimos al inicio
    } catch (error) {
      toast.error(error.message || 'Hubo un problema al procesar tu pedido.');
      console.error("Error al enviar pedido:", error)
    } finally {
      setIsSubmitting(false);
    }
  };

  if (getCartItemCount() === 0 && !isSubmitting) {
    return <div className="container mx-auto p-4 text-center">Redirigiendo...</div>;
  }

  return (
    <div className="container mx-auto p-4 sm:p-8">
      <h1 className="text-3xl font-bold text-slate-800 mb-8 text-center">Finalizar Compra</h1>
      <div className="grid md:grid-cols-3 gap-8">
        <div className="md:col-span-2 bg-white p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold text-slate-700 mb-6">Información de Envío y Contacto</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <input type="text" name="nombre_completo_contacto" value={formData.nombre_completo_contacto} onChange={handleChange} placeholder="Nombre Completo" required className="w-full p-3 border border-slate-300 rounded-md focus:ring-sky-500 focus:border-sky-500" />
            <input type="email" name="email_contacto" value={formData.email_contacto} onChange={handleChange} placeholder="Email de Contacto" required className="w-full p-3 border border-slate-300 rounded-md focus:ring-sky-500 focus:border-sky-500" />
            <input type="tel" name="telefono_contacto" value={formData.telefono_contacto} onChange={handleChange} placeholder="Teléfono de Contacto" required className="w-full p-3 border border-slate-300 rounded-md focus:ring-sky-500 focus:border-sky-500" />
            <input type="text" name="direccion_envio" value={formData.direccion_envio} onChange={handleChange} placeholder="Dirección de Envío (Calle y Número)" required className="w-full p-3 border border-slate-300 rounded-md focus:ring-sky-500 focus:border-sky-500" />
            
            {/* Nuevos Selectores */}
            <select name="estado_pedido_id" value={formData.estado_pedido_id} onChange={handleChange} required className="w-full p-3 border border-slate-300 rounded-md focus:ring-sky-500 focus:border-sky-500 bg-white">
              <option value="">{loadingOpciones ? "Cargando..." : "Selecciona Estado de Pedido"}</option>
              {estadosPedido.map(estado => (
                <option key={estado.id} value={estado.id}>{estado.nombre_estado}</option>
              ))}
            </select>

            <select name="tipo_entrega_id" value={formData.tipo_entrega_id} onChange={handleChange} required className="w-full p-3 border border-slate-300 rounded-md focus:ring-sky-500 focus:border-sky-500 bg-white">
              <option value="">{loadingOpciones ? "Cargando..." : "Selecciona Tipo de Entrega"}</option>
              {tiposEntrega.map(tipo => (
                <option key={tipo.id} value={tipo.id}>{tipo.descripcion_entrega}</option>
              ))}
            </select>

            <select name="metodo_pago_id" value={formData.metodo_pago_id} onChange={handleChange} required className="w-full p-3 border border-slate-300 rounded-md focus:ring-sky-500 focus:border-sky-500 bg-white">
              <option value="">{loadingOpciones ? "Cargando..." : "Selecciona Método de Pago"}</option>
              {metodosPago.map(metodo => (
                <option key={metodo.id} value={metodo.id}>{metodo.nombre_metodo}</option> // Asume que el campo es nombre_metodo
              ))}
            </select>

            <select name="region_id" value={formData.region_id} onChange={handleChange} required className="w-full p-3 border border-slate-300 rounded-md focus:ring-sky-500 focus:border-sky-500 bg-white">
              <option value="">{loadingRegiones ? "Cargando regiones..." : "Selecciona una Región"}</option>
              {regiones.map(region => (
                <option key={region.id} value={region.id}>{region.nombre_region}</option>
              ))}
            </select>

            <select 
              name="comuna_envio_id" // Coincide con el backend
              value={formData.comuna_envio_id} 
              onChange={handleChange} 
              required 
              disabled={!formData.region_id || loadingComunas} // Deshabilitar si no hay región o si están cargando comunas
              className="w-full p-3 border border-slate-300 rounded-md focus:ring-sky-500 focus:border-sky-500 bg-white disabled:bg-slate-100"
            >
              <option value="">{loadingComunas ? "Cargando comunas..." : (formData.region_id ? "Selecciona una Comuna" : "Selecciona una región primero")}</option>
              {comunas.map(comuna => (
                <option key={comuna.id} value={comuna.id}>{comuna.nombre_comuna || comuna.nombre}</option> 
              ))}
            </select>
            {/* <textarea name="nota_adicional" value={formData.nota_adicional} onChange={handleChange} placeholder="Nota adicional para tu pedido (opcional)" rows="3" className="w-full p-3 border border-slate-300 rounded-md focus:ring-sky-500 focus:border-sky-500"></textarea> */}
            
            <button type="submit" disabled={isSubmitting || getCartItemCount() === 0} className="w-full bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-6 rounded-lg shadow-md hover:shadow-lg transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed">
              {isSubmitting ? 'Procesando Pedido...' : 'Realizar Pedido'}
            </button>
          </form>
        </div>

        <div className="md:col-span-1 bg-slate-50 p-6 rounded-lg shadow-lg h-fit">
          <h2 className="text-xl font-semibold text-slate-700 mb-6 border-b pb-3">Resumen del Carrito</h2>
          {cartItems.map(item => (
            <div key={item.id} className="flex justify-between items-center py-2 border-b last:border-b-0 text-sm">
              <div>
                <p className="font-medium text-slate-700">{item.nombre_producto} <span className="text-xs text-slate-500">x{item.quantity}</span></p>
              </div>
              <p className="text-slate-600">${(parseFloat(item.precio) * item.quantity).toFixed(2)}</p>
            </div>
          ))}
          <div className="mt-6 pt-4 border-t">
            <div className="flex justify-between items-center font-bold text-lg">
              <span className="text-slate-700">Total:</span>
              <span className="text-slate-800">${getCartTotal().toFixed(2)}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CheckoutPage;