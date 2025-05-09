from django.contrib import admin
from .models import Region, Comuna

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('nombre_region',)
    search_fields = ('nombre_region',)

@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
    list_display = ('nombre_comuna', 'region')
    search_fields = ('nombre_comuna',)
    list_filter = ('region',)