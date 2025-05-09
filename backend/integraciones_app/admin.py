from django.contrib import admin
from .models import ApiIntegrationLog, ApiConfig

@admin.register(ApiIntegrationLog)
class ApiIntegrationLogAdmin(admin.ModelAdmin):
    list_display = ('api_config_nombre', 'endpoint', 'fecha_hora_llamada', 'codigo_estado', 'success')
    search_fields = ('api_config__nombre_api', 'endpoint', 'request_data', 'response_data')
    list_filter = ('api_config__nombre_api', 'success', 'fecha_hora_llamada')
    date_hierarchy = 'fecha_hora_llamada'

    def api_config_nombre(self, obj):
        return obj.api_config.nombre_api if obj.api_config else None
    api_config_nombre.short_description = 'API Config'

@admin.register(ApiConfig)
class ApiConfigAdmin(admin.ModelAdmin):
    list_display = ('nombre_api', 'endpoint_url', 'activo')
    search_fields = ('nombre_api',)
    list_filter = ('activo',)