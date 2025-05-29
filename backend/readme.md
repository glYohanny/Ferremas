--- /dev/null
+++ b/c:\Users\pedro\Desktop\ferremas2\backend\README.md
@@ -0,0 +1,163 @@
+# Ferremas - Backend
+
+Backend de la aplicación Ferremas, desarrollado con Django y Django REST framework. Este sistema gestiona la lógica de negocio, la base de datos y la API para la plataforma de ferretería.
+
+## Tabla de Contenidos
+
+- [Descripción General](#descripción-general)
+- [Tecnologías Utilizadas](#tecnologías-utilizadas)
+- [Estructura del Proyecto](#estructura-del-proyecto)
+- [Prerrequisitos](#prerrequisitos)
+- [Instalación](#instalación)
+- [Configuración de Variables de Entorno](#configuración-de-variables-de-entorno)
+- [Ejecución de la Aplicación](#ejecución-de-la-aplicación)
+- [Endpoints de la API](#endpoints-de-la-api)
+- [Población Inicial de Datos (Opcional)](#población-inicial-de-datos-opcional)
+
+## Descripción General
+
+Este backend proporciona una API RESTful para la gestión de:
+- Usuarios (clientes, personal) y autenticación.
+- Catálogo de productos, incluyendo categorías y marcas.
+- Inventario y stock por bodegas.
+- Procesamiento de pedidos y detalles.
+- Integración con sistemas de pago (ej. Webpay).
+- Gestión de promociones y notificaciones.
+- Datos geográficos y sucursales.
+- Bitácora de actividades y más.
+
+## Tecnologías Utilizadas
+
+- **Python** (v3.9+)
+- **Django** (v5.2.1, según tu `requirements.txt`)
+- **Django REST framework** (para la API)
+- **djangorestframework-simplejwt** (para autenticación con JWT)
+- **transbank-sdk** (para la integración con Webpay)
+
+## Estructura del Proyecto
+
+El proyecto está organizado en las siguientes aplicaciones Django:
+
+- `usuarios_app`: Gestión de usuarios (modelo `Usuario` personalizado), roles, perfiles (`Personal`, `Cliente`), autenticación y `BitacoraActividad`.
+- `geografia_app`: Manejo de datos geográficos como `Region`, `Provincia`, `Comuna`.
+- `sucursales_app`: Gestión de `Sucursal` y `Bodega`.
+- `productos_app`: Catálogo de `Producto`, `Categoria`, `Marca`.
+- `inventario_app`: Control de `Inventario` de productos en bodegas y `HistorialStock`.
+- `pedidos_app`: Procesamiento de `Pedido` de clientes y sus `DetallePedido`.
+- `pagos_app`: Integración con `MetodoPago` y lógica para transacciones (ej. Webpay).
+- `marketing_app`: Gestión de `Promocion` (con condiciones y restricciones) y `Notificacion`.
+- `integraciones_app`: integraciones con sistemas externos
+- `finanzas_app`: para módulos financieros
+- `informes_app`: para generación de informes
+
+## Prerrequisitos
+
+- Python 3.9 o superior.
+- Pip (gestor de paquetes de Python).
+- `virtualenv` (recomendado para aislar el entorno del proyecto).
+- Una base de datos compatible con Django (ej. PostgreSQL, MySQL, SQLite)
+- Git.
+
+## Instalación
+
+1.  **Clonar el repositorio:**
+    ```bash
+    git clone <URL_DEL_REPOSITORIO_AQUI> 
+    cd ferremas2/backend 
+    ```
+
+2.  **Crear y activar un entorno virtual:**
+    ```bash
+    python -m venv venv
+    # En Windows
+    .\venv\Scripts\activate
+    # En macOS/Linux
+    source venv/bin/activate
+    ```
+
+3.  **Instalar dependencias:**
+    ```bash
+    pip install -r requirements.txt
+    ```
+
+4.  **Configurar la base de datos:**
+    Abre `backend/settings.py` y configura la sección `DATABASES` según tu motor de base de datos. Para PostgreSQL, por ejemplo:
+    ```python
+    DATABASES = {
+        'default': {
+           'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3', # Esto crea un archivo db.sqlite3 en el directorio base del backend

+        }
+    }
+    ```
+
+5.  **Configurar variables de entorno (Recomendado):**
+    Crea un archivo `.env` en el directorio `c:\Users\pedro\Desktop\ferremas2\backend\` (junto a `manage.py`) para almacenar configuraciones sensibles. Ejemplo:
+    ```env
+    SECRET_KEY='tu_django_secret_key_aqui'
+    DEBUG=True 
+    DATABASE_URL='postgres://tu_usuario_db:tu_password_db@localhost:5432/ferremas_db' # Opcional si configuras DATABASES directamente
+    EMAIL_HOST_USER='tu_email_para_envios@example.com'
+    EMAIL_HOST_PASSWORD='tu_password_de_email'
+    FRONTEND_DOMAIN='http://localhost:5173' # Para reseteo de contraseña y retornos de Webpay
+    # Credenciales de Transbank (ambiente de prueba)
+    WEBPAY_PLUS_COMMERCE_CODE='597055555532' # Ejemplo, usa el tuyo de prueba
+    WEBPAY_PLUS_API_KEY='579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C' # Ejemplo, usa la tuya de prueba
+    ```
+    Asegúrate de que `backend/settings.py` esté configurado para leer estas variables (usando `python-decouple`, `django-environ` o `os.environ.get`). La variable `DATABASE_URL` no es necesaria si usas la configuración por defecto de SQLite3.
 
+
+6.  **Aplicar migraciones:**
+    ```bash
+    python manage.py makemigrations
+    python manage.py migrate
+    ```
+
+7.  **Crear un superusuario (administrador):**
+    ```bash
+    python manage.py createsuperuser
+    ```
+    Sigue las instrucciones para crear tu cuenta de administrador.
+
+## Ejecución de la Aplicación
+
+Para iniciar el servidor de desarrollo:
+```bash
+python manage.py runserver
+```
+Por defecto, la aplicación estará disponible en `http://127.0.0.1:8000/`.
+
+## Endpoints de la API
+
+La API sigue una estructura RESTful. Los principales endpoints están agrupados por aplicación:
+
+- `/api/usuarios/`: Endpoints para usuarios, roles, perfiles, etc.
+- `/api/productos/`: Endpoints para productos, categorías, marcas.
+- `/api/inventario/`: Endpoints para inventario y su historial.
+- `/api/pedidos/`: Endpoints para la gestión de pedidos.
+- `/api/pagos/`: Endpoints para métodos de pago e integración con Webpay.
+- `/api/marketing/`: Endpoints para promociones y notificaciones.
+- `/api/geografia/`: Endpoints para regiones, provincias, comunas.
+- `/api/sucursales/`: Endpoints para sucursales y bodegas.
+- `/api/token/`: Para obtener tokens JWT (login).
+- `/api/token/refresh/`: Para refrescar tokens JWT.
+
+Puedes explorar la API navegando a `/api-auth/login/` (si tienes `rest_framework.urls` incluidas en tu `backend/urls.py`) después de iniciar sesión con tu superusuario. Esto te dará acceso a la interfaz navegable de Django REST framework.
+
+## Población Inicial de Datos (Opcional)
+
+Si necesitas poblar la base de datos con datos iniciales (ej. roles, estados de pedido, tipos de entrega, comunas), puedes crear:
+- **Fixtures:** Archivos JSON o YAML que Django puede cargar.
+  ```bash
+  python manage.py loaddata nombre_del_fixture.json
+  ```
+- **Comandos de gestión personalizados:** Scripts de Python para crear datos programáticamente.
+  ```bash
+  python manage.py tu_comando_personalizado
+  ```
+
+---

