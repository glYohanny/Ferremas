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
    # Para mostrar los detalles de la categoría en las respuestas (lectura)
    categoria = CategoriaSerializer(read_only=True)
    # Para aceptar un ID de categoría al crear/actualizar un producto (escritura)
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), source='categoria', write_only=True, allow_null=True, required=False
    )
    imagen_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Producto
        fields = [
            'id', 'nombre_producto', 'descripcion', 'precio', 'stock',
            'marca', 'codigo_producto',
            'categoria',    # Objeto categoría para lectura
            'categoria_id', # ID para escritura
            'imagen',       # Para subir/actualizar la imagen (DRF maneja la subida de archivos)
            'imagen_url',   # Para obtener la URL de la imagen en lectura
        ]
        # Si quieres que el campo 'imagen' no sea obligatorio al crear/actualizar vía API:
        extra_kwargs = {
            'imagen': {'required': False, 'allow_null': True}
        }

    def get_imagen_url(self, obj):
        request = self.context.get('request')
        if obj.imagen and request:
            return request.build_absolute_uri(obj.imagen.url)
        return None