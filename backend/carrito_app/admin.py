from django.contrib import admin
from .models import Carrito, CarritoProducto

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fecha_creacion', 'fecha_actualizacion')
    search_fields = ('cliente__nombre_completo',)
    list_filter = ('fecha_creacion', 'fecha_actualizacion')
    date_hierarchy = 'fecha_creacion'

@admin.register(CarritoProducto)
class CarritoProductoAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'producto', 'cantidad', 'fecha_agregado')
    search_fields = ('carrito__cliente__nombre_completo', 'producto__nombre_producto')
    list_filter = ('fecha_agregado',)
    date_hierarchy = 'fecha_agregado'