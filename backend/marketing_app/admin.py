from django.contrib import admin
from .models import (
    Promocion, ProductoPromocion, Notificacion, ClienteNotificacion,
    PromocionCondicion, PromocionRestriccion
)

@admin.register(Promocion)
# Configuración de la interfaz de administración para el modelo Promocion.
class PromocionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_descuento', 'valor_descuento', 'fecha_inicio', 'fecha_fin', 'activo', 'prioridad', 'tipo_aplicacion')
    search_fields = ('nombre', 'descripcion',)
    list_filter = ('activo', 'tipo_descuento', 'tipo_aplicacion', 'fecha_inicio', 'fecha_fin')
    date_hierarchy = 'fecha_inicio'
    ordering = ('prioridad', '-fecha_inicio')

    # def descripcion_corta(self, obj):
    #     return obj.descripcion[:50] + "..." if len(obj.descripcion) > 50 else obj.descripcion
    # descripcion_corta.short_description = 'Descripción'

@admin.register(ProductoPromocion)
# Configuración de la interfaz de administración para el modelo ProductoPromocion.
class ProductoPromocionAdmin(admin.ModelAdmin):
    list_display = ('producto', 'promocion')
    search_fields = ('producto__nombre_producto', 'promocion__nombre')
    list_filter = ('promocion',)

@admin.register(PromocionCondicion)
class PromocionCondicionAdmin(admin.ModelAdmin):
    list_display = ('promocion', 'tipo_objetivo', 'producto_objetivo', 'categoria_objetivo', 'marca_objetivo', 'cantidad_minima_aplicable')
    list_filter = ('tipo_objetivo', 'promocion')
    search_fields = ('promocion__nombre', 'producto_objetivo__nombre_producto', 'categoria_objetivo__nombre', 'marca_objetivo__nombre')
    autocomplete_fields = ['promocion', 'producto_objetivo', 'categoria_objetivo', 'marca_objetivo']

@admin.register(PromocionRestriccion)
class PromocionRestriccionAdmin(admin.ModelAdmin):
    list_display = ('promocion', 'tipo_restriccion', 'valor_monto', 'valor_entero')
    list_filter = ('tipo_restriccion', 'promocion')
    search_fields = ('promocion__nombre',)
    autocomplete_fields = ['promocion']

@admin.register(Notificacion)
# Configuración de la interfaz de administración para el modelo Notificacion.
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_envio')
    search_fields = ('titulo', 'contenido')
    list_filter = ('fecha_envio',)
    date_hierarchy = 'fecha_envio'

@admin.register(ClienteNotificacion)
# Configuración de la interfaz de administración para el modelo ClienteNotificacion.
class ClienteNotificacionAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'notificacion', 'leido', 'fecha_lectura')
    search_fields = ('cliente__nombre_completo', 'notificacion__titulo')
    list_filter = ('leido', 'fecha_lectura')
    date_hierarchy = 'fecha_lectura' # O notificacion__fecha_envio si prefieres