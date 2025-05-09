from rest_framework import viewsets, permissions
from inventario_app.models import Inventario, HistorialStock
from .serializers import InventarioSerializer, HistorialStockSerializer

# ---------------------------
# INVENTARIO Y HISTORIAL
# ---------------------------
class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer
    permission_classes = [permissions.IsAuthenticated] # Personal autorizado

class HistorialStockViewSet(viewsets.ModelViewSet):
    queryset = HistorialStock.objects.all()
    serializer_class = HistorialStockSerializer
    permission_classes = [permissions.IsAuthenticated] # Personal autorizado