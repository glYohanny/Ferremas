import React, { createContext, useState, useContext, useEffect } from 'react';
// import { toast } from 'react-toastify'; // Opcional: para notificaciones

const CartContext = createContext();

export const useCart = () => {
  return useContext(CartContext);
};

export const CartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState(() => {
    try {
      const localData = localStorage.getItem('cartItems');
      return localData ? JSON.parse(localData) : [];
    } catch (error) {
      console.error("Error al cargar el carrito desde localStorage:", error);
      return [];
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem('cartItems', JSON.stringify(cartItems));
    } catch (error) {
      console.error("Error al guardar el carrito en localStorage:", error);
    }
  }, [cartItems]);

  const addItem = (product, quantity = 1) => {
    setCartItems(prevItems => {
      const existingItem = prevItems.find(item => item.id === product.id);
      if (existingItem) {
        return prevItems.map(item =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + quantity }
            : item
        );
      } else {
        // Asegúrate de que el producto tenga las propiedades necesarias
        const newItem = {
          id: product.id,
          nombre_producto: product.nombre_producto || "Producto sin nombre",
          precio: product.precio || 0,
          imagen_url: product.imagen_url || '',
          quantity
        };
        return [...prevItems, newItem];
      }
    });
    // toast.success(`${product.nombre_producto || 'Producto'} añadido al carrito!`); // Opcional
    console.log(`${product.nombre_producto || 'Producto'} añadido al carrito`);
  };

  const removeItem = (productId) => {
    setCartItems(prevItems => prevItems.filter(item => item.id !== productId));
  };

  const updateQuantity = (productId, quantity) => {
    if (quantity <= 0) {
      removeItem(productId);
    } else {
      setCartItems(prevItems =>
        prevItems.map(item =>
          item.id === productId ? { ...item, quantity: parseInt(quantity, 10) } : item
        )
      );
    }
  };

  const clearCart = () => {
    setCartItems([]);
  };

  const getCartTotal = () => {
    return cartItems.reduce((total, item) => total + (parseFloat(item.precio) * item.quantity), 0);
  };

  const getCartItemCount = () => {
    return cartItems.reduce((count, item) => count + item.quantity, 0);
  };

  const value = { cartItems, addItem, removeItem, updateQuantity, clearCart, getCartTotal, getCartItemCount };

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
};