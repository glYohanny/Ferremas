from rest_framework import serializers
from geografia_app.models import Region, Comuna

# ---------------------------
# REGIÓN Y COMUNA
# ---------------------------
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class ComunaSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    region_id = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all(), source='region', write_only=True)

    class Meta:
        model = Comuna
        fields = ['id', 'nombre_comuna', 'region', 'region_id']