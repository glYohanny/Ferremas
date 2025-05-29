from django.contrib import admin
from .models import EstadoPedido, TipoEntrega, Pedido, DetallePedido, PedidoProcesadoPor

# Configuración de la interfaz de administración para EstadoPedido.
@admin.register(EstadoPedido)
class EstadoPedidoAdmin(admin.ModelAdmin):
    list_display = ('nombre_estado',)
    search_fields = ('nombre_estado',)

# Configuración de la interfaz de administración para TipoEntrega.
@admin.register(TipoEntrega)
class TipoEntregaAdmin(admin.ModelAdmin):
    list_display = ('descripcion_entrega',)
    search_fields = ('descripcion_entrega',)

# Configuración de la interfaz de administración para Pedido.
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha', 'estado_pedido', 'tipo_entrega', 'total')
    search_fields = ('id', 'cliente__nombre_completo')
    list_filter = ('estado_pedido', 'tipo_entrega', 'fecha')
    date_hierarchy = 'fecha'

# Configuración de la interfaz de administración para DetallePedido.
@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'precio_unitario', 'subtotal')
    search_fields = ('pedido__id', 'producto__nombre_producto')
    list_filter = ('pedido__estado_pedido',)

# Configuración de la interfaz de administración para PedidoProcesadoPor.
@admin.register(PedidoProcesadoPor)
class PedidoProcesadoPorAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'vendedor', 'bodeguero')
    search_fields = ('pedido__id', 'vendedor__nombre_completo', 'bodeguero__nombre_completo')