from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventarioViewSet, HistorialStockViewSet

# Crear router para ViewSets
router = DefaultRouter()
router.register(r'inventarios', InventarioViewSet)
router.register(r'historial-stock', HistorialStockViewSet)

# URLs de la aplicación
urlpatterns = [
    path('', include(router.urls)),
    # Rutas adicionales específicas no manejadas por el router
]