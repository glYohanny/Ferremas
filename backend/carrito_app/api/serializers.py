from rest_framework import serializers
from carrito_app.models import Carrito, CarritoProducto

# ---------------------------
# CARRITO DE COMPRAS
# ---------------------------
class CarritoProductoSerializer(serializers.ModelSerializer): # Definir antes de CarritoSerializer si se anida
    class Meta:
        model = CarritoProducto
        fields = '__all__'

class CarritoSerializer(serializers.ModelSerializer):
    items = CarritoProductoSerializer(many=True, read_only=True)
    class Meta:
        model = Carrito
        fields = ['id', 'cliente', 'fecha_creacion', 'fecha_actualizacion', 'items']