from django.contrib import admin
from .models import Rol, Usuario, TipoPersonal, Personal, Cliente, BitacoraActividad

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre_usuario', 'rol', 'is_active', 'is_staff')
    search_fields = ('nombre_usuario',)
    list_filter = ('is_active', 'is_staff', 'rol')

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre_rol',)
    search_fields = ('nombre_rol',)

@admin.register(TipoPersonal)
class TipoPersonalAdmin(admin.ModelAdmin):
    list_display = ('nombre_tipo',)
    search_fields = ('nombre_tipo',)

@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'rut', 'email', 'sucursal', 'tipo')
    search_fields = ('nombre_completo', 'rut', 'email')
    list_filter = ('sucursal', 'tipo')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'email', 'telefono', 'comuna')
    search_fields = ('nombre_completo', 'email', 'telefono')
    list_filter = ('comuna',)

# Registrar BitacoraActividad sin personalización
admin.site.register(BitacoraActividad)