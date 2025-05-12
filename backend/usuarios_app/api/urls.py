from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ( # Cambiado a importación relativa
    RolViewSet, UsuarioViewSet, TipoPersonalViewSet,
    PersonalViewSet, ClienteViewSet, BitacoraActividadViewSet, 
    ClienteRegistroView, PasswordResetRequestView,PasswordResetConfirmView # Asegúrate de importar las vistas
)

# Crear router para ViewSets
router = DefaultRouter()
router.register(r'roles', RolViewSet)
router.register(r'usuario', UsuarioViewSet, basename='usuario') # 'usuario' es el basename
router.register(r'tipos-personal', TipoPersonalViewSet)
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
]