from rest_framework import serializers
from pagos_app.models import TarjetaCliente, EstadoTransaccion, MetodoPago, TransaccionTarjetaCliente, RegistroContable

# ---------------------------
# PAGOS Y TRANSACCIONES
# ---------------------------
class TarjetaClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarjetaCliente
        fields = '__all__'

class EstadoTransaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoTransaccion
        fields = '__all__'

class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPago
        fields = '__all__'

class TransaccionTarjetaClienteSerializer(serializers.ModelSerializer):
    # Ejemplo:
    # tarjeta = TarjetaClienteSerializer(read_only=True)
    # estado_transaccion = EstadoTransaccionSerializer(read_only=True)
    # metodo_pago = MetodoPagoSerializer(read_only=True)
    class Meta:
        model = TransaccionTarjetaCliente
        fields = '__all__'

class RegistroContableSerializer(serializers.ModelSerializer):
    # Ejemplo:
    # transaccion = TransaccionTarjetaClienteSerializer(read_only=True)
    # pedido = PedidoSerializer(read_only=True) # Asumiendo que tienes PedidoSerializer importado
    monto = serializers.DecimalField(max_digits=12, decimal_places=0, required=False, allow_null=True)
    class Meta:
        model = RegistroContable
        fields = '__all__'