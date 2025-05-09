from rest_framework import viewsets, permissions
from usuarios_app.models import Rol, Usuario, TipoPersonal, Personal, Cliente, BitacoraActividad
from .serializers import (
    RolSerializer, UsuarioSerializer, TipoPersonalSerializer, 
    PersonalSerializer, ClienteSerializer, BitacoraActividadSerializer
)

# ---------------------------
# ROLES Y USUARIOS
# ---------------------------
class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [permissions.IsAdminUser] # Generalmente los roles los maneja un admin

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAdminUser] # O permisos más granulares

# ---------------------------
# PERSONAL
# ---------------------------
class TipoPersonalViewSet(viewsets.ModelViewSet):
    queryset = TipoPersonal.objects.all()
    serializer_class = TipoPersonalSerializer
    permission_classes = [permissions.IsAdminUser]

class PersonalViewSet(viewsets.ModelViewSet):
    queryset = Personal.objects.all()
    serializer_class = PersonalSerializer
    permission_classes = [permissions.IsAdminUser] # O permisos basados en roles

# ---------------------------
# CLIENTES
# ---------------------------
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated] # Un cliente podría ver/editar su propio perfil

# ---------------------------
# BITÁCORA DE ACTIVIDAD
# ---------------------------
class BitacoraActividadViewSet(viewsets.ModelViewSet):
    queryset = BitacoraActividad.objects.all()
    serializer_class = BitacoraActividadSerializer
    permission_classes = [permissions.IsAdminUser]