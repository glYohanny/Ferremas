from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TarjetaClienteViewSet, EstadoTransaccionViewSet, MetodoPagoViewSet,
    TransaccionTarjetaClienteViewSet, RegistroContableViewSet
)

# Crear router para ViewSets
router = DefaultRouter()
router.register(r'tarjetas', TarjetaClienteViewSet, basename='tarjetacliente')
router.register(r'estados-transaccion', EstadoTransaccionViewSet)
router.register(r'metodos-pago', MetodoPagoViewSet)
router.register(r'transacciones', TransaccionTarjetaClienteViewSet, basename='transacciontarjetacliente')
router.register(r'registros-contables', RegistroContableViewSet)

# URLs de la aplicación
urlpatterns = [
    path('', include(router.urls)),
    # Rutas adicionales específicas no manejadas por el router
]