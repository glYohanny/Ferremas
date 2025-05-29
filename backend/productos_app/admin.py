from django.contrib import admin
from .models import Categoria, Producto, Marca # Importar Marca

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre_producto', 'codigo_producto', 'precio', 'display_stock_total', 'categoria', 'marca')
    search_fields = ('nombre_producto', 'codigo_producto', 'marca__nombre_marca') # Permitir búsqueda por nombre de marca
    list_filter = ('categoria', 'marca')

    def display_stock_total(self, obj):
        return obj.stock_total
    display_stock_total.short_description = 'Stock Total' # Esto define el nombre de la columna en el admin

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre_categoria',)
    search_fields = ('nombre_categoria',)

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre_marca',)
    search_fields = ('nombre_marca',)