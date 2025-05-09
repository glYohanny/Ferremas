from rest_framework import viewsets, permissions
from pedidos_app.models import EstadoPedido, TipoEntrega, Pedido, DetallePedido, PedidoProcesadoPor
from .serializers import (
    EstadoPedidoSerializer, TipoEntregaSerializer, PedidoSerializer, 
    DetallePedidoSerializer, PedidoProcesadoPorSerializer
)

# ---------------------------
# PEDIDOS
# ---------------------------
class EstadoPedidoViewSet(viewsets.ModelViewSet):
    queryset = EstadoPedido.objects.all()
    serializer_class = EstadoPedidoSerializer
    permission_classes = [permissions.IsAdminUser] # Generalmente administrado

class TipoEntregaViewSet(viewsets.ModelViewSet):
    queryset = TipoEntrega.objects.all()
    serializer_class = TipoEntregaSerializer
    permission_classes = [permissions.IsAdminUser] # Generalmente administrado

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated] # Cliente ve sus pedidos, admin ve todos

class DetallePedidoViewSet(viewsets.ModelViewSet):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer
    permission_classes = [permissions.IsAuthenticated]

class PedidoProcesadoPorViewSet(viewsets.ModelViewSet):
    queryset = PedidoProcesadoPor.objects.all()
    serializer_class = PedidoProcesadoPorSerializer
    permission_classes = [permissions.IsAuthenticated] # Personal autorizado