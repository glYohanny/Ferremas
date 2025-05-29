
from pathlib import Path
import os
from decouple import config # Importar config de python-decouple
from datetime import timedelta # Para la configuración de Simple JWT

from datetime import timedelta
# Define la ruta base del proyecto. __file__ es este archivo (settings.py), .parent es la carpeta 'backend', y .parent.parent es la raíz del proyecto.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# Leer SECRET_KEY y DEBUG desde el archivo .env
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

# ADVERTENCIA DE SEGURIDAD: ¡no ejecutes con debug activado en producción!

# Lista de hosts/dominios permitidos para servir esta aplicación Django.
ALLOWED_HOSTS = ['localhost', '127.0.0.1','192.168.242.231']


# Application definition

INSTALLED_APPS = [
    # Aplicaciones por defecto de Django
    'django.contrib.admin',             # Interfaz de administración
    'django.contrib.auth',              # Sistema de autenticación
    'django.contrib.contenttypes',      # Framework para tipos de contenido
    'django.contrib.sessions',          # Framework para sesiones
    'django.contrib.messages',          # Framework para mensajes (notificaciones)
    'django.contrib.staticfiles',       # Framework para manejar archivos estáticos (CSS, JS, imágenes)
    
    # Tus aplicaciones personalizadas
    'finanzas_app',
    'geografia_app',
    'integraciones_app',
    'inventario_app',
    'marketing_app',
    'pagos_app',
    'pedidos_app',
    'productos_app',
    'sucursales_app',
    'usuarios_app',
    'informes_app',   
    
    # Aplicaciones de terceros
    'rest_framework',                   # Django REST framework para construir APIs
    'rest_framework_simplejwt',         # Para autenticación con JSON Web Tokens (JWT)
    'django_filters',                   # Para filtrado fácil en Django REST framework
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Módulo Python donde se definen las URLs raíz del proyecto.
ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates', # Motor de plantillas por defecto de Django
        'DIRS': [], # Directorios adicionales donde buscar plantillas
        'APP_DIRS': True, # Buscar plantillas dentro de los directorios 'templates' de las apps instaladas
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Interfaz de servidor web para aplicaciones Python (WSGI).
WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Motor de base de datos (SQLite3 para desarrollo)
        'NAME': BASE_DIR / 'db.sqlite3',        # Nombre o ruta al archivo de la base de datos
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
# Validadores de contraseñas.
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
# Internacionalización (i18n) y localización (l10n).
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es-cl' # Código de idioma por defecto (Cambiado a español de Chile)

TIME_ZONE = 'America/Santiago' # Zona horaria por defecto (Cambiado a Santiago)

USE_I18N = True # Habilita el sistema de traducción de Django

USE_TZ = True # Habilita el soporte para zonas horarias


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# Configuración de archivos estáticos (CSS, JavaScript, Imágenes).
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = 'static/' # URL base para servir archivos estáticos

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
# Tipo de campo de clave primaria por defecto para los modelos.
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField' # Usa BigAutoField para IDs autoincrementales

# Configuración explícita de Caché (para asegurar que no se use caché activa)
# Configuración explícita de Caché (para asegurar que no se use caché activa en desarrollo).
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache', # Backend de caché que no hace nada (útil para desarrollo/pruebas)
    }
}

# Modelo de Usuario Personalizado
# Especifica el modelo de usuario personalizado que Django debe usar.
AUTH_USER_MODEL = 'usuarios_app.Usuario'

# CORS
# Configuración de Cross-Origin Resource Sharing (CORS).
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",     
]

# Redirección después del login
# URL a la que se redirige al usuario después de un inicio de sesión exitoso (usado por django.contrib.auth).
LOGIN_REDIRECT_URL = '/' # Puedes cambiar esto a '/api/' o cualquier otra ruta válida

# Configuración específica para Django REST framework.
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ( # Clases de autenticación por defecto para las vistas de API
        'rest_framework_simplejwt.authentication.JWTAuthentication', # Autenticación basada en JWT
        'rest_framework.authentication.SessionAuthentication', # Autenticación basada en sesión (útil para la API Navegable de DRF)

    ),
    'DEFAULT_PERMISSION_CLASSES': [ # Permisos por defecto para las vistas de API
        'rest_framework.permissions.IsAuthenticated', # Por defecto, requiere autenticación
    ]
}
# Configuración de JWT (JSON Web Tokens)
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30), # Duración del token de acceso
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),    # Duración del token de refresco
    'ROTATE_REFRESH_TOKENS': True, # Si es True, cada vez que se usa un token de refresco, se emite uno nuevo
    'BLACKLIST_AFTER_ROTATION': True, # Pone en lista negra el token de refresco antiguo después de la rotación
    'UPDATE_LAST_LOGIN': True, # Actualiza el campo last_login del usuario al obtener un token

    'ALGORITHM': 'HS256', # Algoritmo de firma
    'SIGNING_KEY': SECRET_KEY, # Clave de firma (usa la SECRET_KEY de Django por defecto)
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',), # Tipos de encabezado de autenticación (ej. "Bearer <token>")
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION', # Nombre del encabezado HTTP
    'USER_ID_FIELD': 'id', # Campo del modelo de usuario que se usará como identificador
    'USER_ID_CLAIM': 'user_id', # Nombre del claim en el JWT para el ID de usuario
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5), # No relevante si no usas sliding tokens
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1), # No relevante si no usas sliding tokens
}







# Configuración para archivos multimedia (MEDIA)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')




# Configuración de Email (Ejemplo para desarrollo - los emails se muestran en la consola).
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Dirección de email por defecto que se usará como remitente en los correos enviados por el sistema.
DEFAULT_FROM_EMAIL = 'pedritotorresvillegas92@gmail.com' # El email "desde" que verán los usuarios
