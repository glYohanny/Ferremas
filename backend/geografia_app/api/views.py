from rest_framework import viewsets, permissions, filters
from geografia_app.models import Region, Comuna
from .serializers import RegionSerializer, ComunaSerializer
from django_filters.rest_framework import DjangoFilterBackend

# ---------------------------
# REGIÓN Y COMUNA
# ---------------------------
class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all().order_by('nombre_region')  # Ordenar por nombre
    serializer_class = RegionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Permitir lectura, requerir auth para escritura
    filter_backends = [filters.OrderingFilter]  # Habilitar ordenamiento
    ordering_fields = ['nombre_region']  # Permitir ordenar por nombre

class ComunaViewSet(viewsets.ModelViewSet):
    queryset = Comuna.objects.all().order_by('nombre_comuna')  # Ordenar por nombre
    serializer_class = ComunaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter] # Añadir DjangoFilterBackend
    filterset_fields = ['region']  # Permitir filtrar por el campo 'region'
    ordering_fields = ['nombre_comuna']  # Permitir ordenar por nombre
    
    def get_queryset(self):
        # Ordenar por nombre de región y luego por nombre de comuna
        return super().get_queryset().order_by('region__nombre_region', 'nombre_comuna')