from rest_framework import serializers
from productos_app.models import Categoria, Producto, Marca # Importar Marca
from inventario_app.models import Inventario # Importar Inventario para consultar stock
from finanzas_app.models import TipoCambio # Importar el modelo TipoCambio
from django.utils import timezone
from django.db.models import Sum 

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
    precios_convertidos = serializers.SerializerMethodField(read_only=True)
    stock_sucursal_seleccionada = serializers.SerializerMethodField() # Campo para stock de sucursal

    class Meta:
        model = Producto
        fields = [
            'id',
            'nombre_producto',# Debe coincidir con el campo en tu modelo Producto
            'descripcion',
            'precio',
            'stock_total',    # Nuevo campo de solo lectura para el stock total
            'marca',          # Objeto marca para lectura (usará MarcaSerializer)
            'marca_id',       # ID de marca para escritura
            'codigo_producto',# Coincide con el modelo Producto
            'categoria',      # Objeto categoría para lectura
            'categoria_id',   # ID para escritura
            'imagen',       # Para subir/actualizar la imagen (DRF maneja la subida de archivos)
            'imagen_url',   # Para obtener la URL de la imagen en lectura
            'stock_sucursal_seleccionada', # Incluir el nuevo campo
            'precios_convertidos', # Nuevo campo para precios en otras divisas
            # Añade otros campos de tu modelo Producto que quieras exponer
            # 'fecha_creacion',
            # 'fecha_actualizacion',
        ]
        # Si quieres que el campo 'imagen' no sea obligatorio al crear/actualizar vía API:
        read_only_fields = ['stock_total'] # Aseguramos que stock_total sea de solo lectura
        extra_kwargs = {
            'imagen': {'required': False, 'allow_null': True}
        }

    def get_imagen_url(self, obj):
        request = self.context.get('request')
        if obj.imagen and request:
            return request.build_absolute_uri(obj.imagen.url)
        return None

    def get_precios_convertidos(self, obj):
        """
        Calcula y devuelve los precios del producto en diferentes divisas.
        Asume que obj.precio es el precio base en CLP.
        """
        precios = {}
        # Lista de monedas a las que quieres convertir (puedes hacer esto configurable)
        monedas_destino_codigos = ['USD', 'EUR'] # Ejemplo
        precio_base_clp = obj.precio

        if precio_base_clp is None:
            return None # O un diccionario vacío {} si prefieres

        for codigo_destino in monedas_destino_codigos:
            try:
                # Buscar la tasa de cambio más reciente y válida para CLP a la moneda destino
                tipo_cambio = TipoCambio.objects.filter(
                    moneda_origen='CLP',  # Moneda base de tus precios de producto
                    moneda_destino=codigo_destino,
                    fecha_validez__lte=timezone.now().date() # Tasa válida hasta hoy
                ).order_by('-fecha_validez', '-fecha_registro').first() # La más reciente válida

                if tipo_cambio and tipo_cambio.tasa and tipo_cambio.tasa != 0: # Asegurarse que la tasa no sea None o 0
                    precios[codigo_destino] = round(precio_base_clp / tipo_cambio.tasa, 2)
                else:
                    precios[codigo_destino] = None # No se encontró tasa o la tasa es cero/None
            except Exception as e:
                # Loggear el error si es necesario
                print(f"Error al convertir a {codigo_destino} para producto {obj.id}: {e}")
                precios[codigo_destino] = None
        
        return precios

    def get_stock_sucursal_seleccionada(self, obj):
        """
        Calcula y devuelve el stock del producto para una sucursal específica.
        La sucursal_id se espera en el contexto del serializador.
        """
        sucursal_id = self.context.get('sucursal_id')
        # print(f"ProductoSerializer: Calculando stock para producto ID {obj.id} en sucursal_id {sucursal_id}") # DEBUG
        if sucursal_id:
            try:
                # ADAPTA ESTA CONSULTA A TUS MODELOS:
                # Asume que Inventario tiene FK a Producto y FK a Bodega, y Bodega tiene FK a Sucursal.
                # O que Inventario tiene FK directa a Sucursal.
                inventario_entry = Inventario.objects.filter(
                    producto=obj, 
                    bodega__sucursal_id=sucursal_id # Ajusta 'bodega__sucursal_id' según tu modelo
                ).aggregate(total_stock_sucursal=Sum('cantidad'))
                
                stock_en_sucursal = inventario_entry.get('total_stock_sucursal')
                # print(f"Serializer: Producto ID {obj.id}, Sucursal ID {sucursal_id}, Stock encontrado: {stock_en_sucursal}") # DEBUG
                return stock_en_sucursal if stock_en_sucursal is not None else 0
            except Exception as e:
                print(f"Serializer: Producto ID {obj.id}, Sucursal ID {sucursal_id}, Error obteniendo stock: {e}") # DEBUG
                return 0 # Devolver 0 si hay un error o no se encuentra
        # print(f"Serializer: Producto ID {obj.id}, No se proporcionó sucursal_id en el contexto.") # DEBUG
        return None # Devolver None si no se proporciona sucursal_id en el contexto