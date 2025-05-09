from rest_framework import viewsets, permissions
from finanzas_app.models import TipoCambio, ConversionDivisa
from .serializers import TipoCambioSerializer, ConversionDivisaSerializer

# ---------------------------
# TIPOS DE CAMBIO Y CONVERSIONES
# ---------------------------
class TipoCambioViewSet(viewsets.ModelViewSet):
    queryset = TipoCambio.objects.all()
    serializer_class = TipoCambioSerializer
    permission_classes = [permissions.IsAdminUser]

class ConversionDivisaViewSet(viewsets.ModelViewSet):
    queryset = ConversionDivisa.objects.all()
    serializer_class = ConversionDivisaSerializer
    permission_classes = [permissions.IsAdminUser]