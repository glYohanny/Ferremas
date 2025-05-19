from rest_framework import serializers
from pedidos_app.models import EstadoPedido, TipoEntrega, Pedido, DetallePedido, PedidoProcesadoPor
from productos_app.api.serializers import ProductoSerializer # Para mostrar info del producto en DetallePedido
from geografia_app.api.serializers import ComunaSerializer # Para mostrar info de la comuna en Pedido
from usuarios_app.api.serializers import UsuarioSerializer # Para mostrar info del cliente en Pedido
from pagos_app.api.serializers import MetodoPagoSerializer # Para mostrar info del método de pago
from pagos_app.models import MetodoPago # Importar el modelo MetodoPago
from geografia_app.models import Comuna # Importar el modelo Comuna
# Asegúrate de que los serializadores importados existan y estén correctamente definidos.
# ---------------------------
# PEDIDOS
# ---------------------------
class EstadoPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoPedido
        fields = '__all__'

class TipoEntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEntrega
        fields = '__all__'

class DetallePedidoInputSerializer(serializers.Serializer): # Para la entrada de items al crear pedido
    producto_id = serializers.IntegerField()
    cantidad = serializers.IntegerField(min_value=1)

class DetallePedidoOutputSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)

    class Meta:
        model = DetallePedido
        fields = ['id', 'producto', 'cantidad', 'precio_unitario', 'subtotal']

class PedidoSerializer(serializers.ModelSerializer):
    # Campos para lectura (representación anidada)
    cliente = UsuarioSerializer(read_only=True)
    estado_pedido = EstadoPedidoSerializer(read_only=True)
    tipo_entrega = TipoEntregaSerializer(read_only=True)
    metodo_pago = MetodoPagoSerializer(read_only=True)
    comuna_envio = ComunaSerializer(read_only=True)
    detalles = DetallePedidoOutputSerializer(many=True, read_only=True) # Renombrado de 'items' a 'detalles' para coincidir con related_name

    # Campos para escritura (IDs que vienen del frontend)
    estado_pedido_id = serializers.PrimaryKeyRelatedField(
        queryset=EstadoPedido.objects.all(), source='estado_pedido', write_only=True
    )
    tipo_entrega_id = serializers.PrimaryKeyRelatedField(
        queryset=TipoEntrega.objects.all(), source='tipo_entrega', write_only=True
    )
    metodo_pago_id = serializers.PrimaryKeyRelatedField(
        queryset=MetodoPago.objects.all(), source='metodo_pago', write_only=True
    )
    comuna_envio_id = serializers.PrimaryKeyRelatedField(
        queryset=Comuna.objects.all(), source='comuna_envio', write_only=True
    )
    items_input = DetallePedidoInputSerializer(many=True, write_only=True, help_text="Lista de productos con id y cantidad. Ej: [{'producto_id': 1, 'cantidad': 2}]")

    class Meta:
        model = Pedido
        fields = [
            'id', 'cliente', 'fecha', 'total',
            'estado_pedido', 'estado_pedido_id',
            'tipo_entrega', 'tipo_entrega_id',
            'metodo_pago', 'metodo_pago_id',
            'nombre_completo_contacto', 'email_contacto', 'telefono_contacto', 'direccion_envio',
            'comuna_envio', 'comuna_envio_id',
            'detalles', 'items_input' # 'items_input' es solo para la creación
        ]
        read_only_fields = ['id', 'cliente', 'fecha', 'total', 'detalles']

class PedidoProcesadoPorSerializer(serializers.ModelSerializer):
    # Ejemplo:
    # pedido = PedidoSerializer(read_only=True)
    # personal = PersonalSerializer(read_only=True) # Asumiendo que tienes PersonalSerializer importado
    class Meta:
        model = PedidoProcesadoPor
        fields = '__all__'