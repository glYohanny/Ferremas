"""Define las rutas URL para la API de la aplicación de pedidos."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EstadoPedidoViewSet, TipoEntregaViewSet, PedidoViewSet,
    DetallePedidoViewSet, PedidoProcesadoPorViewSet
)

# Crear router para ViewSets
router = DefaultRouter()
router.register(r'estados-pedido', EstadoPedidoViewSet)
router.register(r'tipos-entrega', TipoEntregaViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'detalles-pedido', DetallePedidoViewSet)
router.register(r'pedidos-procesados', PedidoProcesadoPorViewSet)

# URLs de la aplicación
urlpatterns = [
    path('', include(router.urls)),
    # Rutas adicionales específicas no manejadas por el router
]