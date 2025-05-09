from rest_framework import serializers
from sucursales_app.models import Sucursal, Bodega

# ---------------------------
# SUCURSAL Y BODEGA
# ---------------------------
class SucursalSerializer(serializers.ModelSerializer):
    # Para mostrar detalles de Comuna en lectura:
    # comuna = ComunaSerializer(read_only=True)
    # comuna_id = serializers.PrimaryKeyRelatedField(queryset=Comuna.objects.all(), source='comuna', write_only=True, allow_null=True)
    class Meta:
        model = Sucursal
        fields = '__all__' # 'comuna' será un ID por defecto

class BodegaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bodega
        fields = '__all__'