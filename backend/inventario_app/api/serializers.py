from rest_framework import serializers
from inventario_app.models import Inventario, HistorialStock
from productos_app.api.serializers import ProductoSerializer
from sucursales_app.api.serializers import BodegaSerializer

# ---------------------------
# INVENTARIO Y HISTORIAL
# ---------------------------
class InventarioSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Inventario, permite ver detalles y gestionar mediante IDs."""
    producto = ProductoSerializer(read_only=True)
    bodega = BodegaSerializer(read_only=True)

    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductoSerializer.Meta.model.objects.all(), source='producto', write_only=True
    )
    bodega_id = serializers.PrimaryKeyRelatedField(
        queryset=BodegaSerializer.Meta.model.objects.all(), source='bodega', write_only=True
    )
    class Meta:
        model = Inventario
        fields = ['id', 'producto', 'bodega', 'cantidad', 'producto_id', 'bodega_id']

class HistorialStockSerializer(serializers.ModelSerializer):
    """Serializador para el modelo HistorialStock, proporciona una vista detallada de los cambios de stock."""
    producto = ProductoSerializer(read_only=True)
    bodega = BodegaSerializer(read_only=True)

    class Meta:
        model = HistorialStock
        fields = ['id', 'producto', 'bodega', 'cantidad_cambiada', 'motivo', 'fecha']

class AgregarStockSerializer(serializers.Serializer):
    """Serializador para la acción de agregar stock a un inventario existente."""
    cantidad_a_agregar = serializers.IntegerField(min_value=1)
    motivo = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=255)

    def validate_cantidad_a_agregar(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad a agregar debe ser un número positivo.")
        return value