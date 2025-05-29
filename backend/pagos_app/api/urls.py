"""Define las rutas URL para la API de la aplicación de pagos."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TarjetaClienteViewSet, EstadoTransaccionViewSet, MetodoPagoViewSet,
    TransaccionTarjetaClienteViewSet, RegistroContableViewSet, WebpayCreateTransactionView,
    WebpayCommitTransactionView
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
    # Rutas para Webpay
    path('webpay/crear-transaccion/', WebpayCreateTransactionView.as_view(), name='webpay-crear-transaccion'),
    path('webpay/retorno/', WebpayCommitTransactionView.as_view(), name='webpay-retorno'), # Esta es tu return_url
]