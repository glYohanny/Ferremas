from rest_framework import serializers
from sucursales_app.models import Sucursal, Bodega
from geografia_app.api.serializers import ComunaSerializer # Asegúrate que este serializer exista y esté bien definido
from geografia_app.models import Comuna # Para el queryset de PrimaryKeyRelatedField

# ---------------------------
# SUCURSAL Y BODEGA
# ---------------------------
class SucursalSerializer(serializers.ModelSerializer):
    # Para mostrar detalles de Comuna en lectura (GET)
    comuna = ComunaSerializer(read_only=True)
    # Para permitir la asignación de Comuna por ID en escritura (POST, PUT)
    comuna_id = serializers.PrimaryKeyRelatedField(
        queryset=Comuna.objects.all(), 
        source='comuna', 
        write_only=True, 
        allow_null=True, # Permite que la comuna sea opcional si el modelo lo permite
        required=False   # Hace que el campo no sea obligatorio en la entrada si el modelo lo permite
    )

    class Meta:
        model = Sucursal
        fields = ['id', 'nombre_sucursal', 'direccion', 'comuna', 'comuna_id']

class BodegaSerializer(serializers.ModelSerializer):
    # Para mostrar detalles de Sucursal en lectura (GET)
    sucursal = SucursalSerializer(read_only=True)
    # Para permitir la asignación de Sucursal por ID en escritura (POST, PUT)
    sucursal_id = serializers.PrimaryKeyRelatedField(
        queryset=Sucursal.objects.all(), 
        source='sucursal', 
        write_only=True
    )

    class Meta:
        model = Bodega
        # Incluir todos los campos relevantes, incluyendo el nuevo 'tipo_bodega'
        # y los campos para manejar la relación con sucursal
        fields = ['id', 'nombre_bodega', 'direccion', 'sucursal', 'sucursal_id', 'tipo_bodega']