from django.contrib import admin
from .models import Promocion, ProductoPromocion, Notificacion, ClienteNotificacion

@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = ('descripcion_corta', 'fecha_inicio', 'fecha_fin', 'activa', 'porcentaje_descuento')
    search_fields = ('descripcion',)
    list_filter = ('activa', 'fecha_inicio', 'fecha_fin')
    date_hierarchy = 'fecha_inicio'

    def descripcion_corta(self, obj):
        return obj.descripcion[:50] + "..." if len(obj.descripcion) > 50 else obj.descripcion
    descripcion_corta.short_description = 'Descripción'

@admin.register(ProductoPromocion)
class ProductoPromocionAdmin(admin.ModelAdmin):
    list_display = ('producto', 'promocion')
    search_fields = ('producto__nombre_producto', 'promocion__nombre')
    list_filter = ('promocion',)

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_envio')
    search_fields = ('titulo', 'contenido')
    list_filter = ('fecha_envio',)
    date_hierarchy = 'fecha_envio'

@admin.register(ClienteNotificacion)
class ClienteNotificacionAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'notificacion', 'leido', 'fecha_lectura')
    search_fields = ('cliente__nombre_completo', 'notificacion__titulo')
    list_filter = ('leido', 'fecha_lectura')
    date_hierarchy = 'fecha_lectura' # O notificacion__fecha_envio si prefieres