from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ( # Cambiado a importación relativa
    RolViewSet, UsuarioViewSet, TipoPersonalViewSet,
    PersonalViewSet, ClienteViewSet, BitacoraActividadViewSet
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
]