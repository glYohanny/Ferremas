from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SucursalViewSet, BodegaViewSet

# Crear router para ViewSets
router = DefaultRouter()
router.register(r'sucursal', SucursalViewSet)
router.register(r'bodegas', BodegaViewSet)

# URLs de la aplicación
urlpatterns = [
    path('', include(router.urls)),
    # Rutas adicionales específicas no manejadas por el router
]