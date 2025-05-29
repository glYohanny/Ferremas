from django.contrib import admin
from .models import TarjetaCliente, EstadoTransaccion, MetodoPago, TransaccionTarjetaCliente, RegistroContable

@admin.register(TarjetaCliente)
# Configuración de la interfaz de administración para TarjetaCliente.
class TarjetaClienteAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'numero_tarjeta_ultimos_digitos', 'marca_tarjeta', 'fecha_expiracion')
    search_fields = ('cliente__usuario__first_name', 'cliente__usuario__last_name', 'cliente__usuario__nombre_usuario')
    list_filter = ('marca_tarjeta', 'fecha_expiracion')

@admin.register(EstadoTransaccion)
# Configuración de la interfaz de administración para EstadoTransaccion.
class EstadoTransaccionAdmin(admin.ModelAdmin):
    list_display = ('nombre_estado',)
    search_fields = ('nombre_estado',)

@admin.register(MetodoPago)
# Configuración de la interfaz de administración para MetodoPago.
class MetodoPagoAdmin(admin.ModelAdmin):
    list_display = ('descripcion_pago',)
    search_fields = ('descripcion_pago',)

@admin.register(TransaccionTarjetaCliente)
# Configuración de la interfaz de administración para TransaccionTarjetaCliente.
class TransaccionTarjetaClienteAdmin(admin.ModelAdmin):
    list_display = ('tarjeta_cliente_referencia', 'cliente', 'monto_total', 'fecha_transaccion', 'estado')
    search_fields = ('cliente__usuario__first_name', 'cliente__usuario__last_name', 'cliente__usuario__nombre_usuario', 'id_transaccion_pasarela')
    list_filter = ('estado', 'fecha_transaccion')
    date_hierarchy = 'fecha_transaccion'

@admin.register(RegistroContable)
# Configuración de la interfaz de administración para RegistroContable.
class RegistroContableAdmin(admin.ModelAdmin):
    list_display = ('fecha_contable', 'monto', 'descripcion', 'transaccion_origen', 'registrado_por')
    search_fields = ('descripcion', 'transaccion_origen__id_transaccion_pasarela')
    list_filter = ('fecha_contable', 'registrado_por')
    date_hierarchy = 'fecha_contable'