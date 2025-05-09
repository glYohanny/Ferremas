from rest_framework import viewsets, permissions
from sucursales_app.models import Sucursal, Bodega
from .serializers import SucursalSerializer, BodegaSerializer

# ---------------------------
# SUCURSAL Y BODEGA
# ---------------------------
class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer
    permission_classes = [permissions.IsAuthenticated]

class BodegaViewSet(viewsets.ModelViewSet):
    queryset = Bodega.objects.all()
    serializer_class = BodegaSerializer
    permission_classes = [permissions.IsAuthenticated]