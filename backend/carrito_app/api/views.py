from rest_framework import viewsets, permissions
from carrito_app.models import Carrito, CarritoProducto
from .serializers import CarritoSerializer, CarritoProductoSerializer

# ---------------------------
# CARRITO DE COMPRAS
# ---------------------------
class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer
    permission_classes = [permissions.IsAuthenticated] # Solo el dueño del carrito

class CarritoProductoViewSet(viewsets.ModelViewSet):
    queryset = CarritoProducto.objects.all()
    serializer_class = CarritoProductoSerializer
    permission_classes = [permissions.IsAuthenticated] # Solo el dueño del carrito