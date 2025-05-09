from rest_framework import serializers
from inventario_app.models import Inventario, HistorialStock

# ---------------------------
# INVENTARIO Y HISTORIAL
# ---------------------------
class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields = '__all__'

class HistorialStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialStock
        fields = '__all__'