from rest_framework import serializers
from pagos_app.models import TarjetaCliente, EstadoTransaccion, MetodoPago, TransaccionTarjetaCliente, RegistroContable

# ---------------------------
# PAGOS Y TRANSACCIONES
# ---------------------------
class TarjetaClienteSerializer(serializers.ModelSerializer):
    """Serializador para gestionar las referencias de tarjetas de clientes."""
    class Meta:
        model = TarjetaCliente
        fields = [
            'id',
            'numero_tarjeta_ultimos_digitos',
            'marca_tarjeta',
            'fecha_expiracion',
            'cliente',
            'token_pasarela'
        ]
        read_only_fields = ['id', 'cliente'] # cliente se asigna en la vista

class EstadoTransaccionSerializer(serializers.ModelSerializer):
    """Serializador para los estados de las transacciones."""
    class Meta:
        model = EstadoTransaccion
        fields = ['id', 'nombre_estado']
        read_only_fields = ['id']

class MetodoPagoSerializer(serializers.ModelSerializer):
    """Serializador para los métodos de pago."""
    class Meta:
        model = MetodoPago
        fields = ['id', 'descripcion_pago']
        read_only_fields = ['id']

class TransaccionTarjetaClienteSerializer(serializers.ModelSerializer):
    """Serializador para las transacciones de pago de los clientes."""
    # Ejemplo:
    # tarjeta = TarjetaClienteSerializer(read_only=True)
    # estado_transaccion = EstadoTransaccionSerializer(read_only=True)
    # metodo_pago = MetodoPagoSerializer(read_only=True)
    class Meta:
        model = TransaccionTarjetaCliente
        fields = [
            'id',
            'tarjeta_cliente_referencia',
            'id_transaccion_pasarela',
            'cliente',
            'monto_total',
            'estado',
            'metodo_pago',
            'fecha_transaccion',
            'descripcion',
            'pedido',
            'codigo_autorizacion_pasarela',
            'ultimos_digitos_tarjeta'
        ]
        read_only_fields = ['id', 'fecha_transaccion', 'cliente'] # cliente se asigna en la vista

class RegistroContableSerializer(serializers.ModelSerializer):
    """Serializador para los registros contables."""
    # Ejemplo:
    # transaccion = TransaccionTarjetaClienteSerializer(read_only=True)
    # pedido = PedidoSerializer(read_only=True) # Asumiendo que tienes PedidoSerializer importado
    monto = serializers.DecimalField(max_digits=12, decimal_places=0, required=False, allow_null=True)
    class Meta:
        model = RegistroContable
        fields = [
            'id',
            'transaccion_origen',
            'descripcion',
            'monto',
            'fecha_contable',
            'fecha_registro',
            'registrado_por'
        ]
        read_only_fields = ['id', 'fecha_registro']