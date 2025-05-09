from rest_framework import serializers
from productos_app.models import Categoria, Producto

# ---------------------------
# PRODUCTOS Y CATEGORÍAS
# ---------------------------
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'