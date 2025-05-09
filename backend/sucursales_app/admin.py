from django.contrib import admin
from .models import Sucursal, Bodega

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre_sucursal', 'direccion', 'comuna')
    search_fields = ('nombre_sucursal', 'direccion')
    list_filter = ('comuna',)

@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ('nombre_bodega', 'sucursal')
    search_fields = ('nombre_bodega',)
    list_filter = ('sucursal',)