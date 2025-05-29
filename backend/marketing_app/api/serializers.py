from rest_framework import serializers
from marketing_app.models import (
    Promocion, ProductoPromocion, Notificacion, ClienteNotificacion,
    PromocionCondicion, PromocionRestriccion
)
# Asumiendo que tienes estos serializadores en productos_app
# from productos_app.api.serializers import ProductoSerializer, CategoriaSerializer, MarcaSerializer

# ---------------------------
# PROMOCIONES
# ---------------------------

class PromocionCondicionSerializer(serializers.ModelSerializer):
    # Opcional: mostrar representación de string para los FKs en lectura
    # producto_objetivo_detalle = ProductoSerializer(source='producto_objetivo', read_only=True)
    # categoria_objetivo_detalle = CategoriaSerializer(source='categoria_objetivo', read_only=True)
    # marca_objetivo_detalle = MarcaSerializer(source='marca_objetivo', read_only=True)

    class Meta:
        model = PromocionCondicion
        fields = [
            'id',
            'promocion', # Se enviará el ID al crear/actualizar
            'tipo_objetivo',
            'producto_objetivo',    # FK a Producto (ID)
            'categoria_objetivo',   # FK a Categoria (ID)
            'marca_objetivo',       # FK a Marca (ID)
            'cantidad_minima_aplicable',
            # 'producto_objetivo_detalle', 
            # 'categoria_objetivo_detalle',
            # 'marca_objetivo_detalle',
        ]
        read_only_fields = ['id']

    def validate(self, data):
        # La validación a nivel de modelo (clean) se ejecutará, pero podemos añadir más aquí si es necesario.
        # Por ejemplo, asegurar que el tipo_objetivo coincida con el campo de objetivo rellenado.
        tipo_objetivo = data.get('tipo_objetivo')
        producto = data.get('producto_objetivo')
        categoria = data.get('categoria_objetivo')
        marca = data.get('marca_objetivo')

        if tipo_objetivo == 'PRODUCTO' and not producto:
            raise serializers.ValidationError({"producto_objetivo": "Debe especificar un producto para este tipo de objetivo."})
        if tipo_objetivo == 'CATEGORIA' and not categoria:
            raise serializers.ValidationError({"categoria_objetivo": "Debe especificar una categoría para este tipo de objetivo."})
        if tipo_objetivo == 'MARCA' and not marca:
            raise serializers.ValidationError({"marca_objetivo": "Debe especificar una marca para este tipo de objetivo."})
        return data

class PromocionRestriccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromocionRestriccion
        fields = [
            'id',
            'promocion',
            'tipo_restriccion',
            'valor_monto',
            'valor_entero',
            # 'valor_texto',
        ]
        read_only_fields = ['id']

class PromocionSerializer(serializers.ModelSerializer):
    """Serializador para gestionar los datos de las promociones."""
    condiciones = PromocionCondicionSerializer(many=True, read_only=True) # Para ver condiciones al leer una promoción
    restricciones = PromocionRestriccionSerializer(many=True, read_only=True) # Para ver restricciones

    class Meta:
        model = Promocion
        fields = [
            'id',
            'nombre',
            'descripcion',
            'tipo_descuento',
            'valor_descuento',
            'fecha_inicio',
            'fecha_fin',
            'activo',
            'prioridad',
            'tipo_aplicacion',
            'condiciones', # Campo de solo lectura para anidamiento
            'restricciones', # Campo de solo lectura para anidamiento
        ]
        read_only_fields = ['id']

class ProductoPromocionSerializer(serializers.ModelSerializer):
    """Serializador para vincular productos con promociones."""
    class Meta:
        model = ProductoPromocion
        fields = [
            'id',
            'producto',
            'promocion',
        ]
        read_only_fields = ['id']

# ---------------------------
# NOTIFICACIONES
# ---------------------------
class NotificacionSerializer(serializers.ModelSerializer):
    """Serializador para gestionar los datos de las notificaciones generales."""
    class Meta:
        model = Notificacion
        fields = [
            'id',
            'titulo',
            'contenido',
            'fecha_envio',
        ]
        read_only_fields = ['id', 'fecha_envio']

class ClienteNotificacionSerializer(serializers.ModelSerializer):
    """Serializador para gestionar el estado de las notificaciones por cliente."""
    class Meta:
        model = ClienteNotificacion
        fields = [
            'id',
            'cliente',
            'notificacion',
            'leido',
            'fecha_lectura',
        ]
        read_only_fields = ['id', 'fecha_lectura']