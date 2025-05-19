from django.contrib import admin
from .models import Venta, VentaDetalle
# Promocion, CategoriaProducto y Producto se administran desde sus respectivas apps.

# Si quisieras personalizar la administración de Promocion para los informes (ej. un readonly para ciertos campos),
# podrías registrarla aquí también, pero generalmente bastará con administrarla desde marketing_app.
# from marketing_app.models import Promocion
# @admin.register(Promocion)
# class PromocionAdmin(admin.ModelAdmin):
#     pass # O tus personalizaciones

class VentaDetalleInline(admin.TabularInline): # O admin.StackedInline
    model = VentaDetalle
    extra = 1 # Número de formularios extra para detalles
    autocomplete_fields = ['producto'] # Esto funcionará si Producto está correctamente referenciado
    # Podrías añadir campos readonly si algunos se calculan automáticamente
    # readonly_fields = ('subtotal',)

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'sucursal', 'vendedor', 'fecha_venta', 'total_venta')
    list_filter = ('fecha_venta', 'sucursal', 'vendedor')
    search_fields = ('id', 'sucursal__nombre_sucursal', 'vendedor__username') # Ajusta 'vendedor__username' según tu modelo User
    date_hierarchy = 'fecha_venta'
    inlines = [VentaDetalleInline]
    autocomplete_fields = ['sucursal', 'vendedor']
    # readonly_fields = ('total_venta',) # Si total_venta se calcula automáticamente y no quieres que se edite aquí

    def get_queryset(self, request):
        # Optimizar consultas
        return super().get_queryset(request).select_related('sucursal', 'vendedor')

# No es necesario registrar VentaDetalle por separado si se usa como inline,
# pero si quieres acceder directamente a VentaDetalle desde el admin, puedes hacerlo:
# @admin.register(VentaDetalle)
# class VentaDetalleAdmin(admin.ModelAdmin):
#     list_display = ('venta', 'producto', 'cantidad', 'precio_unitario_en_venta', 'subtotal')
#     autocomplete_fields = ['venta', 'producto']
