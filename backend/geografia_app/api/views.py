from rest_framework import viewsets, permissions
from geografia_app.models import Region, Comuna
from .serializers import RegionSerializer, ComunaSerializer

# ---------------------------
# REGIÓN Y COMUNA
# ---------------------------
class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Permitir lectura, requerir auth para escritura

class ComunaViewSet(viewsets.ModelViewSet):
    queryset = Comuna.objects.all()
    serializer_class = ComunaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]