from rest_framework import viewsets, permissions
from pagos_app.models import TarjetaCliente, EstadoTransaccion, MetodoPago, TransaccionTarjetaCliente, RegistroContable
from .serializers import (
    TarjetaClienteSerializer, EstadoTransaccionSerializer, MetodoPagoSerializer, 
    TransaccionTarjetaClienteSerializer, RegistroContableSerializer
)
from usuarios_app.models import Cliente # Import your Cliente model
from rest_framework.exceptions import ValidationError # For perform_create error handling

# ---------------------------
# TARJETAS Y TRANSACCIONES
# ---------------------------
class TarjetaClienteViewSet(viewsets.ModelViewSet):
    # queryset = TarjetaCliente.objects.all() # Se define en get_queryset
    serializer_class = TarjetaClienteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Este viewset solo debe devolver las tarjetas del usuario autenticado.
        Asumimos que Cliente tiene un campo 'user' que es OneToOneField/ForeignKey a settings.AUTH_USER_MODEL.
        """
        user = self.request.user
        if not user.is_authenticated:
            return TarjetaCliente.objects.none()
        try:
            cliente_profile = Cliente.objects.get(usuario=user) # Cambiado 'user' por 'usuario'
            return TarjetaCliente.objects.filter(cliente=cliente_profile)
        except Cliente.DoesNotExist:
            return TarjetaCliente.objects.none()
        except AttributeError: # Catch if Cliente.objects.get(user=user) fails due to model structure
            # Log this error appropriately in a real application
            return TarjetaCliente.objects.none()

    def perform_create(self, serializer):
        """Asocia la nueva tarjeta con el perfil de Cliente del usuario autenticado."""
        user = self.request.user
        try:
            cliente_profile = Cliente.objects.get(usuario=user) # Cambiado 'user' por 'usuario'
            serializer.save(cliente=cliente_profile)
        except Cliente.DoesNotExist:
            raise ValidationError("El usuario actual no tiene un perfil de cliente asociado.")

class EstadoTransaccionViewSet(viewsets.ModelViewSet):
    queryset = EstadoTransaccion.objects.all()
    serializer_class = EstadoTransaccionSerializer
    permission_classes = [permissions.IsAdminUser] # Generalmente administrado

class MetodoPagoViewSet(viewsets.ModelViewSet):
    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Permitir lectura a autenticados, escritura a admins

class TransaccionTarjetaClienteViewSet(viewsets.ModelViewSet):
    # queryset = TransaccionTarjetaCliente.objects.all() # Se define en get_queryset
    serializer_class = TransaccionTarjetaClienteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Este viewset solo debe devolver las transacciones del usuario autenticado.
        Asumimos que Cliente tiene un campo 'user' que es OneToOneField/ForeignKey a settings.AUTH_USER_MODEL.
        """
        user = self.request.user
        if not user.is_authenticated:
            return TransaccionTarjetaCliente.objects.none()
        try:
            cliente_profile = Cliente.objects.get(usuario=user) # Cambiado 'user' por 'usuario'
            return TransaccionTarjetaCliente.objects.filter(cliente=cliente_profile)
        except Cliente.DoesNotExist:
            return TransaccionTarjetaCliente.objects.none()
        except AttributeError:
            return TransaccionTarjetaCliente.objects.none()

    def perform_create(self, serializer):
        """Asocia la nueva transacción con el perfil de Cliente del usuario autenticado."""
        user = self.request.user
        try:
            cliente_profile = Cliente.objects.get(usuario=user) # Cambiado 'user' por 'usuario'
            serializer.save(cliente=cliente_profile)
        except Cliente.DoesNotExist:
            raise ValidationError("El usuario actual no tiene un perfil de cliente asociado.")



# ---------------------------
# REGISTROS CONTABLES
# ---------------------------
class RegistroContableViewSet(viewsets.ModelViewSet):
    queryset = RegistroContable.objects.all()
    serializer_class = RegistroContableSerializer
    permission_classes = [permissions.IsAdminUser] # O personal de contabilidad