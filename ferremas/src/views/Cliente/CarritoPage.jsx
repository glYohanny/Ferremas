import React from 'react';
import { useCart } from '../../components/componets_CarritoCompra'; // Ajusta la ruta si es diferente
import { Link, useNavigate } from 'react-router-dom';
import { FaTrashAlt, FaPlus, FaMinus } from 'react-icons/fa'; // Íconos opcionales

const CartItem = ({ item, updateQuantity, removeItem }) => {
  const handleQuantityChange = (e) => {
    const newQuantity = parseInt(e.target.value, 10);
    if (!isNaN(newQuantity) && newQuantity >= 0) {
      updateQuantity(item.id, newQuantity);
    }
  };

  const incrementQuantity = () => {
    updateQuantity(item.id, item.quantity + 1);
  };

  const decrementQuantity = () => {
    if (item.quantity > 0) {
      updateQuantity(item.id, item.quantity - 1);
    }
  };

  return (
    <div className="flex flex-col sm:flex-row items-center justify-between border-b border-slate-200 py-6 last:border-b-0">
      <div className="flex items-center mb-4 sm:mb-0 w-full sm:w-2/5">
        <img 
          src={item.imagen_url || 'https://via.placeholder.com/80x80.png?text=No+Imagen'} 
          alt={item.nombre_producto} 
          className="w-20 h-20 object-cover rounded-md mr-4 shadow" 
        />
        <div>
          <Link to={`/productos/${item.id}`} className="text-lg font-semibold text-sky-600 hover:text-sky-700 hover:underline transition-colors">
            {item.nombre_producto}
          </Link>
          <p className="text-sm text-slate-500">Precio Unitario: ${parseFloat(item.precio).toFixed(2)}</p>
        </div>
      </div>
      
      <div className="flex items-center justify-between sm:justify-end w-full sm:w-3/5">
        <div className="flex items-center mx-2 sm:mx-4">
          <button 
            onClick={decrementQuantity} 
            className="p-2 border border-slate-300 rounded-l-md bg-slate-100 hover:bg-slate-200 transition-colors"
            aria-label="Disminuir cantidad"
          >
            <FaMinus className="text-slate-600" />
          </button>
          <input
            type="number"
            id={`quantity-${item.id}`}
            value={item.quantity}
            onChange={handleQuantityChange}
            min="0"
            className="w-12 text-center border-t border-b border-slate-300 focus:ring-sky-500 focus:border-sky-500"
            aria-label={`Cantidad de ${item.nombre_producto}`}
          />
          <button 
            onClick={incrementQuantity} 
            className="p-2 border border-slate-300 rounded-r-md bg-slate-100 hover:bg-slate-200 transition-colors"
            aria-label="Aumentar cantidad"
          >
            <FaPlus className="text-slate-600" />
          </button>
        </div>

        <p className="w-24 text-right font-semibold text-slate-700 mx-2 sm:mx-4">
          ${(parseFloat(item.precio) * item.quantity).toFixed(2)}
        </p>

        <button
          onClick={() => removeItem(item.id)}
          className="text-red-500 hover:text-red-700 p-2 rounded-md hover:bg-red-100 transition-colors"
          aria-label={`Eliminar ${item.nombre_producto} del carrito`}
        >
          <FaTrashAlt size={18} />
        </button>
      </div>
    </div>
  );
};

const CarritoPage = () => {
  const { cartItems, removeItem, updateQuantity, clearCart, getCartTotal, getCartItemCount } = useCart();
  const navigate = useNavigate();

  if (cartItems.length === 0) {
    return (
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12 text-center">
        <h1 className="text-3xl sm:text-4xl font-bold text-slate-800 mb-6">Tu Carrito de Compras</h1>
        <svg className="mx-auto h-24 w-24 text-slate-400 mb-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1">
          <path strokeLinecap="round" strokeLinejoin="round" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
        <p className="text-xl text-slate-600 mb-8">Parece que tu carrito está vacío.</p>
        <Link 
          to="/" // O a /productos si prefieres
          className="inline-block bg-sky-500 hover:bg-sky-600 text-white font-bold py-3 px-8 rounded-lg shadow-md hover:shadow-lg transition-all duration-300 ease-in-out transform hover:-translate-y-0.5"
        >
          Explorar Productos
        </Link>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-3xl sm:text-4xl font-bold text-slate-800 mb-10 text-center sm:text-left">
        Tu Carrito de Compras
      </h1>
      
      <div className="bg-white shadow-xl rounded-lg overflow-hidden">
        <div className="p-6">
          <div className="hidden sm:flex items-center justify-between text-xs text-slate-500 uppercase font-semibold border-b pb-3 mb-3">
            <div className="w-2/5">Producto</div>
            <div className="w-3/5 flex justify-end items-center">
              <div className="w-1/3 text-center">Cantidad</div>
              <div className="w-1/3 text-right">Subtotal</div>
              <div className="w-1/6 text-right">Quitar</div>
            </div>
          </div>

          {cartItems.map(item => (
            <CartItem key={item.id} item={item} updateQuantity={updateQuantity} removeItem={removeItem} />
          ))}
        </div>

        <div className="bg-slate-50 p-6 border-t border-slate-200">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
            <div>
              <h2 className="text-lg font-semibold text-slate-700">Resumen del Pedido</h2>
              <p className="text-sm text-slate-500">Total de ítems: {getCartItemCount()}</p>
            </div>
            <div className="text-right">
              <p className="text-sm text-slate-500">Subtotal:</p>
              <p className="text-2xl font-bold text-slate-800">${getCartTotal().toFixed(2)}</p>
              {/* Podrías añadir costos de envío e impuestos aquí en el futuro */}
            </div>
          </div>

          <div className="flex flex-col sm:flex-row justify-between gap-4">
            <button 
              onClick={clearCart} 
              className="w-full sm:w-auto order-2 sm:order-1 bg-red-500 hover:bg-red-600 text-white font-semibold py-3 px-6 rounded-lg shadow-md hover:shadow-lg transition-all duration-300 ease-in-out focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50"
            >
              Vaciar Carrito
            </button>
            <button 
              onClick={() => navigate('/checkout')}
              className="w-full sm:w-auto order-1 sm:order-2 bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-6 rounded-lg shadow-md hover:shadow-lg transition-all duration-300 ease-in-out focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50"
            >
              Proceder al Pago
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CarritoPage;
