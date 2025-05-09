from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PromocionViewSet, ProductoPromocionViewSet,
    NotificacionViewSet, ClienteNotificacionViewSet
)

# Crear router para ViewSets
router = DefaultRouter()
router.register(r'promociones', PromocionViewSet)
router.register(r'productos-promocion', ProductoPromocionViewSet)
router.register(r'notificaciones', NotificacionViewSet)
router.register(r'clientes-notificacion', ClienteNotificacionViewSet)

# URLs de la aplicación
urlpatterns = [
    path('', include(router.urls)),
    # Rutas adicionales específicas no manejadas por el router
]