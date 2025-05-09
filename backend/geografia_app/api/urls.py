from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegionViewSet, ComunaViewSet

# Crear router para ViewSets
router = DefaultRouter()
router.register(r'regiones', RegionViewSet)
router.register(r'comunas', ComunaViewSet)

# URLs de la aplicación
urlpatterns = [
    path('', include(router.urls)),
    # Rutas adicionales específicas no manejadas por el router
]