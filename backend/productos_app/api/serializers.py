from rest_framework import serializers
from productos_app.models import Categoria, Producto, Marca # Importar Marca

# ---------------------------
# PRODUCTOS Y CATEGORÍAS
# ---------------------------
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__' # Esto incluirá 'id' y 'nombre_marca'

class ProductoSerializer(serializers.ModelSerializer):
    # Para mostrar los detalles de la categoría en las respuestas (lectura)
    categoria = CategoriaSerializer(read_only=True)
    # Para aceptar un ID de categoría al crear/actualizar un producto (escritura)
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), source='categoria', write_only=True, allow_null=True, required=False
    )
    # Para mostrar los detalles de la marca en las respuestas (lectura)
    marca = MarcaSerializer(read_only=True)
    # Para aceptar un ID de marca al crear/actualizar un producto (escritura)
    marca_id = serializers.PrimaryKeyRelatedField(
        queryset=Marca.objects.all(), source='marca', write_only=True, allow_null=True, required=False
    )
    imagen_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Producto
        fields = [
            'id',
            'nombre_producto',# Debe coincidir con el campo en tu modelo Producto
            'descripcion',
            'precio',         # Debe coincidir con el campo en tu modelo Producto
            'stock',          # Debe coincidir con el campo en tu modelo Producto
            'marca',          # Objeto marca para lectura (usará MarcaSerializer)
            'marca_id',       # ID de marca para escritura
            'codigo_producto',# Coincide con el modelo Producto
            'categoria',    # Objeto categoría para lectura
            'categoria_id', # ID para escritura
            'imagen',       # Para subir/actualizar la imagen (DRF maneja la subida de archivos)
            'imagen_url',   # Para obtener la URL de la imagen en lectura
            # Añade otros campos de tu modelo Producto que quieras exponer
            # 'fecha_creacion',
            # 'fecha_actualizacion',
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