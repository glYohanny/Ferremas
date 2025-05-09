from rest_framework import serializers
from pedidos_app.models import EstadoPedido, TipoEntrega, Pedido, DetallePedido, PedidoProcesadoPor

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

class PedidoSerializer(serializers.ModelSerializer):
    # Aquí podrías añadir campos anidados si quieres mostrar detalles
    # de Cliente, EstadoPedido, TipoEntrega, etc.
    # Ejemplo:
    # cliente = ClienteSerializer(read_only=True) # Asumiendo que tienes ClienteSerializer importado
    # estado = EstadoPedidoSerializer(read_only=True)
    class Meta:
        model = Pedido
        fields = '__all__'

class DetallePedidoSerializer(serializers.ModelSerializer):
    # Ejemplo:
    # producto = ProductoSerializer(read_only=True) # Asumiendo que tienes ProductoSerializer importado
    class Meta:
        model = DetallePedido
        fields = '__all__'

class PedidoProcesadoPorSerializer(serializers.ModelSerializer):
    # Ejemplo:
    # pedido = PedidoSerializer(read_only=True)
    # personal = PersonalSerializer(read_only=True) # Asumiendo que tienes PersonalSerializer importado
    class Meta:
        model = PedidoProcesadoPor
        fields = '__all__'