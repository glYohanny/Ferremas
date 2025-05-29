from rest_framework import viewsets, permissions
from marketing_app.models import (
    Promocion, ProductoPromocion, Notificacion, ClienteNotificacion,
    PromocionCondicion, PromocionRestriccion
)
from .serializers import (
    PromocionSerializer, ProductoPromocionSerializer, 
    NotificacionSerializer, ClienteNotificacionSerializer,
    PromocionCondicionSerializer, PromocionRestriccionSerializer
)

# ---------------------------
# PROMOCIONES
# ---------------------------
class PromocionViewSet(viewsets.ModelViewSet):
    """ViewSet para visualizar y editar promociones."""
    queryset = Promocion.objects.all()
    serializer_class = PromocionSerializer
    permission_classes = [permissions.IsAdminUser] # Administradores crean promociones

class ProductoPromocionViewSet(viewsets.ModelViewSet):
    """ViewSet para visualizar y editar la asignación de productos a promociones."""
    queryset = ProductoPromocion.objects.all()
    serializer_class = ProductoPromocionSerializer
    permission_classes = [permissions.IsAdminUser]

class PromocionCondicionViewSet(viewsets.ModelViewSet):
    """ViewSet para visualizar y editar las condiciones de las promociones."""
    queryset = PromocionCondicion.objects.all()
    serializer_class = PromocionCondicionSerializer
    permission_classes = [permissions.IsAdminUser]

class PromocionRestriccionViewSet(viewsets.ModelViewSet):
    """ViewSet para visualizar y editar las restricciones de las promociones."""
    queryset = PromocionRestriccion.objects.all()
    serializer_class = PromocionRestriccionSerializer
    permission_classes = [permissions.IsAdminUser]

# ---------------------------
# NOTIFICACIONES
# ---------------------------
class NotificacionViewSet(viewsets.ModelViewSet):
    """ViewSet para visualizar y editar notificaciones generales."""
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer
    permission_classes = [permissions.IsAdminUser]

class ClienteNotificacionViewSet(viewsets.ModelViewSet):
    """ViewSet para visualizar y editar el estado de las notificaciones de los clientes."""
    queryset = ClienteNotificacion.objects.all()
    serializer_class = ClienteNotificacionSerializer
    permission_classes = [permissions.IsAuthenticated] # Cliente ve sus notificaciones