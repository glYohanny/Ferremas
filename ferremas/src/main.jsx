import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import LoginForm from './views/secion/inicio_secion.jsx' 
import RegistroForm from './views/secion/registro_cliente.jsx'; // Importa RegistroForm

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App /> {/* Generalmente, aquí se renderiza el componente principal App */}
  </StrictMode>,
)
