from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ( # Cambiado a importación relativa
    RolViewSet, UsuarioViewSet,
    PersonalViewSet, ClienteViewSet, BitacoraActividadViewSet, 
    ClienteRegistroView, PasswordResetRequestView,PasswordResetConfirmView,
    CustomTokenObtainPairView, LogoutView # Importar LogoutView
)

# Crear router para ViewSets
router = DefaultRouter()
router.register(r'roles', RolViewSet)
router.register(r'usuario', UsuarioViewSet, basename='usuario') # 'usuario' es el basename
router.register(r'personal', PersonalViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'bitacora', BitacoraActividadViewSet)

# URLs de la aplicación
urlpatterns = [
    path('', include(router.urls)),
    # Rutas adicionales específicas no manejadas por el router
    path('registro/cliente/', ClienteRegistroView.as_view(), name='app-cliente-registro'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='app-password-reset-request'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='app-password-reset-confirm'),
    # Rutas para login (obtención de token) y logout
    # path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'), # Comentado: Se define globalmente en backend/urls.py
    path('logout/', LogoutView.as_view(), name='app_logout'),
]