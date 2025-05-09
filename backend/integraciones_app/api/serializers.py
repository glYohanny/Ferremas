from rest_framework import serializers
from integraciones_app.models import ApiIntegrationLog, ApiConfig

# ---------------------------
# API LOGS
# ---------------------------
class ApiIntegrationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiIntegrationLog
        fields = '__all__'

# ---------------------------
# CONFIGURACIÓN DE APIS
# ---------------------------
class ApiConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiConfig
        fields = '__all__'