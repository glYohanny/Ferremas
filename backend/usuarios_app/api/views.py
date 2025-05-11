from rest_framework.decorators import action
from rest_framework.response import Response


from rest_framework import viewsets, permissions
from usuarios_app.models import Rol, Usuario, TipoPersonal, Personal, Cliente, BitacoraActividad # Asegúrate que Cliente esté importado
from .serializers import (
    RolSerializer, UsuarioSerializer, TipoPersonalSerializer,
    ClienteRegistroSerializer,PersonalSerializer, 
    ClienteSerializer, BitacoraActividadSerializer,
    ClienteSerializer,
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

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user) # Ahora usará UsuarioSerializer
        return Response(serializer.data)
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

# ---------------------------
# VISTA PARA REGISTRO DE CLIENTES
# ---------------------------
class ClienteRegistroView(viewsets.generics.CreateAPIView): # Usar generics.CreateAPIView para una vista de solo creación
    queryset = Usuario.objects.all() # Aunque es CreateAPIView, necesita un queryset base
    serializer_class = ClienteRegistroSerializer
    permission_classes = [permissions.AllowAny] # Cualquiera puede acceder para registrarse

    # Opcional: puedes sobrescribir el método post si necesitas lógica adicional
    # después de que el usuario y el cliente son creados por el serializador.