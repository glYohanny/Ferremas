from django.contrib import admin
from .models import Rol, Usuario, Personal, Cliente, BitacoraActividad

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre_usuario', 'rol', 'is_active', 'is_staff')
    search_fields = ('nombre_usuario',)
    list_filter = ('is_active', 'is_staff', 'rol')

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre_rol',)
    search_fields = ('nombre_rol',)


@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ('get_usuario_nombre_completo', 'rut', 'get_usuario_email', 'sucursal')
    search_fields = ('usuario__nombre_usuario', 'usuario__first_name', 'usuario__last_name', 'rut', 'usuario__email')
    list_filter = ('sucursal',) # Añadida la coma para que sea una tupla

    @admin.display(description='Nombre Completo (Usuario)', ordering='usuario__first_name')
    def get_usuario_nombre_completo(self, obj):
        name_parts = [obj.usuario.first_name, obj.usuario.last_name]
        full_name = " ".join(part for part in name_parts if part)
        return full_name.strip() or obj.usuario.nombre_usuario

    @admin.display(description='Email (Usuario)', ordering='usuario__email')
    def get_usuario_email(self, obj):
        return obj.usuario.email

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('get_usuario_nombre_completo', 'get_usuario_email', 'telefono', 'comuna')
    search_fields = ('usuario__nombre_usuario', 'usuario__first_name', 'usuario__last_name', 'usuario__email', 'telefono')
    list_filter = ('comuna',)

    @admin.display(description='Nombre Completo (Usuario)', ordering='usuario__first_name')
    def get_usuario_nombre_completo(self, obj):
        name_parts = [obj.usuario.first_name, obj.usuario.last_name]
        full_name = " ".join(part for part in name_parts if part)
        return full_name.strip() or obj.usuario.nombre_usuario

    @admin.display(description='Email (Usuario)', ordering='usuario__email')
    def get_usuario_email(self, obj):
        return obj.usuario.email

# Registrar BitacoraActividad sin personalización
admin.site.register(BitacoraActividad)