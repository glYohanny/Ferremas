from django.contrib import admin
from .models import EstadoPedido, TipoEntrega, Pedido, DetallePedido, PedidoProcesadoPor

@admin.register(EstadoPedido)
class EstadoPedidoAdmin(admin.ModelAdmin):
    list_display = ('nombre_estado',)
    search_fields = ('nombre_estado',)

@admin.register(TipoEntrega)
class TipoEntregaAdmin(admin.ModelAdmin):
    list_display = ('descripcion_entrega',)
    search_fields = ('descripcion_entrega',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha', 'estado_pedido', 'tipo_entrega', 'total')
    search_fields = ('id', 'cliente__nombre_completo')
    list_filter = ('estado_pedido', 'tipo_entrega', 'fecha')
    date_hierarchy = 'fecha'

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'precio_unitario', 'subtotal')
    search_fields = ('pedido__id', 'producto__nombre_producto')
    list_filter = ('pedido__estado_pedido',)

@admin.register(PedidoProcesadoPor)
class PedidoProcesadoPorAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'vendedor', 'bodeguero')
    search_fields = ('pedido__id', 'vendedor__nombre_completo', 'bodeguero__nombre_completo')
    # No hay campos de fecha directa para date_hierarchy o list_filter aquí a menos que los añadas al modelo
    # list_filter = ('accion', 'fecha_accion')
    # date_hierarchy = 'fecha_accion'