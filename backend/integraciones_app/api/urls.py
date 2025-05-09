from django.urls import path, include
from rest_framework.routers import DefaultRouter
from integraciones_app.api.views import ApiIntegrationLogViewSet, ApiConfigViewSet

# Crear router para ViewSets
router = DefaultRouter()
router.register(r'logs', ApiIntegrationLogViewSet)
router.register(r'configuraciones', ApiConfigViewSet)

# URLs de la aplicación
urlpatterns = [
    path('', include(router.urls)),
    # Rutas adicionales específicas no manejadas por el router
]