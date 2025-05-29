"""Define las rutas URL para la API de la aplicación de marketing."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PromocionViewSet, ProductoPromocionViewSet, 
    PromocionCondicionViewSet, PromocionRestriccionViewSet,
    NotificacionViewSet, ClienteNotificacionViewSet
)

# Crear router para ViewSets
router = DefaultRouter()
router.register(r'promociones', PromocionViewSet)
router.register(r'productos-promocion', ProductoPromocionViewSet)
router.register(r'promocion-condiciones', PromocionCondicionViewSet)
router.register(r'promocion-restricciones', PromocionRestriccionViewSet)
router.register(r'notificaciones', NotificacionViewSet)
router.register(r'clientes-notificacion', ClienteNotificacionViewSet)

# URLs de la aplicación
urlpatterns = [
    path('', include(router.urls)),
]