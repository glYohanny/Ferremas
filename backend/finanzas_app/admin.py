from django.contrib import admin
from .models import TipoCambio, ConversionDivisa

@admin.register(TipoCambio)
class TipoCambioAdmin(admin.ModelAdmin):
    list_display = ('moneda_origen', 'moneda_destino', 'tasa', 'fecha_validez', 'fecha_registro')
    search_fields = ('moneda_origen', 'moneda_destino')
    list_filter = ('moneda_origen', 'moneda_destino', 'fecha_validez')
    date_hierarchy = 'fecha_validez'

@admin.register(ConversionDivisa)
class ConversionDivisaAdmin(admin.ModelAdmin):
    list_display = ('fecha_conversion', 'moneda_origen', 'moneda_destino', 'monto_origen', 'monto_destino', 'tipo_cambio_aplicado')
    search_fields = ('moneda_origen', 'moneda_destino')
    list_filter = ('moneda_origen', 'moneda_destino', 'fecha_conversion')
    date_hierarchy = 'fecha_conversion'