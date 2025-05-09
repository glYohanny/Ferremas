from django.contrib import admin
from .models import Categoria, Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre_producto', 'codigo_producto', 'precio', 'stock', 'categoria')
    search_fields = ('nombre_producto', 'codigo_producto')
    list_filter = ('categoria', 'marca')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre_categoria',)
    search_fields = ('nombre_categoria',)