from django.contrib import admin
from .models import Inventario, HistorialStock

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'bodega', 'cantidad', 'fecha_actualizacion')
    search_fields = ('producto__nombre_producto', 'bodega__nombre_bodega')
    list_filter = ('bodega',)

@admin.register(HistorialStock)
class HistorialStockAdmin(admin.ModelAdmin):
    list_display = ('producto', 'bodega', 'cantidad_cambiada', 'motivo', 'fecha')
    search_fields = ('producto__nombre_producto',)
    list_filter = ('bodega', 'fecha')