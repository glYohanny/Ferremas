from rest_framework import viewsets, permissions
from integraciones_app.models import ApiIntegrationLog, ApiConfig
from .serializers import ApiIntegrationLogSerializer, ApiConfigSerializer

# ---------------------------
# INTEGRACIONES Y CONFIG API
# ---------------------------
class ApiIntegrationLogViewSet(viewsets.ModelViewSet):
    queryset = ApiIntegrationLog.objects.all()
    serializer_class = ApiIntegrationLogSerializer
    permission_classes = [permissions.IsAdminUser]

class ApiConfigViewSet(viewsets.ModelViewSet):
    queryset = ApiConfig.objects.all()
    serializer_class = ApiConfigSerializer
    permission_classes = [permissions.IsAdminUser]