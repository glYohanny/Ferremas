from rest_framework import viewsets, permissions
from marketing_app.models import Promocion, ProductoPromocion, Notificacion, ClienteNotificacion
from .serializers import (
    PromocionSerializer, ProductoPromocionSerializer, 
    NotificacionSerializer, ClienteNotificacionSerializer
)

# ---------------------------
# PROMOCIONES
# ---------------------------
class PromocionViewSet(viewsets.ModelViewSet):
    queryset = Promocion.objects.all()
    serializer_class = PromocionSerializer
    permission_classes = [permissions.IsAdminUser] # Administradores crean promociones

class ProductoPromocionViewSet(viewsets.ModelViewSet):
    queryset = ProductoPromocion.objects.all()
    serializer_class = ProductoPromocionSerializer
    permission_classes = [permissions.IsAdminUser]

# ---------------------------
# NOTIFICACIONES
# ---------------------------
class NotificacionViewSet(viewsets.ModelViewSet):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer
    permission_classes = [permissions.IsAdminUser]

class ClienteNotificacionViewSet(viewsets.ModelViewSet):
    queryset = ClienteNotificacion.objects.all()
    serializer_class = ClienteNotificacionSerializer
    permission_classes = [permissions.IsAuthenticated] # Cliente ve sus notificaciones