from rest_framework import viewsets, permissions
from pagos_app.models import TarjetaCliente, EstadoTransaccion, MetodoPago, TransaccionTarjetaCliente, RegistroContable
from .serializers import (
    TarjetaClienteSerializer, EstadoTransaccionSerializer, MetodoPagoSerializer, 
    TransaccionTarjetaClienteSerializer, RegistroContableSerializer
)

# ---------------------------
# TARJETAS Y TRANSACCIONES
# ---------------------------
class TarjetaClienteViewSet(viewsets.ModelViewSet):
    queryset = TarjetaCliente.objects.all()
    serializer_class = TarjetaClienteSerializer
    permission_classes = [permissions.IsAuthenticated] # Solo el dueño de la tarjeta

class EstadoTransaccionViewSet(viewsets.ModelViewSet):
    queryset = EstadoTransaccion.objects.all()
    serializer_class = EstadoTransaccionSerializer
    permission_classes = [permissions.IsAdminUser] # Generalmente administrado

class MetodoPagoViewSet(viewsets.ModelViewSet):
    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoSerializer
    permission_classes = [permissions.IsAdminUser] # Generalmente administrado

class TransaccionTarjetaClienteViewSet(viewsets.ModelViewSet):
    queryset = TransaccionTarjetaCliente.objects.all()
    serializer_class = TransaccionTarjetaClienteSerializer
    permission_classes = [permissions.IsAuthenticated] # El cliente podría ver sus transacciones

# ---------------------------
# REGISTROS CONTABLES
# ---------------------------
class RegistroContableViewSet(viewsets.ModelViewSet):
    queryset = RegistroContable.objects.all()
    serializer_class = RegistroContableSerializer
    permission_classes = [permissions.IsAdminUser] # O personal de contabilidad