from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status, generics
from rest_framework.views import APIView
from usuarios_app.models import Rol, Usuario, Personal, Cliente, BitacoraActividad # Asegúrate que Cliente esté importado
from .serializers import (
    RolSerializer, UsuarioSerializer,
    ClienteRegistroSerializer,PersonalSerializer, 
    ClienteSerializer, BitacoraActividadSerializer, PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer 
)

# Para el reseteo de contraseña
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
import os

# Para personalizar la vista de obtención de tokens y registrar el login
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# Para LogoutView
from rest_framework_simplejwt.tokens import RefreshToken

# ---------------------------
# PERMISOS PERSONALIZADOS
# ---------------------------
class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a los propietarios de un objeto o administradores
    realizar acciones sobre ese objeto (ver detalle, editar, eliminar).
    """
    def has_object_permission(self, request, view, obj):
        # Para cualquier acción a nivel de objeto (retrieve, update, partial_update, destroy),
        # el usuario debe ser el propietario del objeto o un administrador (is_staff).
        # Asumimos que el 'obj' (Cliente, Personal, etc.) tiene un campo 'usuario'
        # que lo vincula directamente al modelo Usuario.
        if not hasattr(obj, 'usuario'):
            # Si el objeto no tiene un campo 'usuario', este permiso no puede determinar la propiedad.
            # Por seguridad, denegar el acceso.
            return False
        return obj.usuario == request.user or request.user.is_staff

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

    @action(detail=False, methods=['get', 'patch', 'put'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        elif request.method in ['PATCH', 'PUT']:
            # Para PATCH (actualización parcial), partial=True
            # Para PUT (actualización completa), partial=False
            # Usaremos UsuarioSerializer, pero el frontend solo debería enviar campos permitidos
            # como first_name, last_name. El serializer ya maneja qué campos son actualizables.
            partial_update = request.method == 'PATCH'
            serializer = self.get_serializer(user, data=request.data, partial=partial_update)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # Registrar en la bitácora
            BitacoraActividad.objects.create(
                usuario=user,
                accion=f"El usuario {user.nombre_usuario} actualizó su perfil."
            )
            return Response(serializer.data)
        # Por si acaso, aunque 'methods' lo limita
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
# ---------------------------
# PERSONAL
# ---------------------------
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
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin] 

    def get_queryset(self):
        """
        Esta vista debe devolver una lista de todos los clientes
        para los usuarios administradores, o solo el cliente asociado
        al usuario actual para usuarios no administradores.
        """
        user = self.request.user
        if user.is_staff: # O user.is_superuser o una comprobación de rol más específica
            return Cliente.objects.all()
        # Para usuarios no administradores, intentar obtener su propio perfil de cliente
        cliente = Cliente.objects.filter(usuario=user).first()
        if cliente:
            return Cliente.objects.filter(pk=cliente.pk) # Devuelve un queryset con solo ese cliente
        return Cliente.objects.none() # No devolver nada si no es admin y no tiene perfil de cliente

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
 
 
    
# ---------------------------
# VISTA PARA SOLICITAR RESETEO DE CONTRASEÑA
# ---------------------------
class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer # <--- AÑADIR ESTA LÍNEA
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) # Validará que el email esté presente y sea válido
        email = serializer.validated_data['email']
        
        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            # No revelar si el usuario existe o no por seguridad
            return Response({'message': 'Si tu correo está registrado, recibirás un email con instrucciones.'}, status=status.HTTP_200_OK)

        token_generator = PasswordResetTokenGenerator()
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        # Asegúrate de tener una variable de entorno o configuración para tu dominio de frontend
        frontend_domain = os.environ.get('FRONTEND_DOMAIN', 'http://localhost:5173') # Cambia localhost:5173 si tu frontend corre en otro puerto/dominio
        
        # La ruta en tu frontend para confirmar el reseteo. Ejemplo: /reset-password-confirm/:uidb64/:token/
        # Esta ruta la crearás en el frontend más adelante.
        reset_url = f"{frontend_domain}/reset-password-confirm/{uidb64}/{token}/"

        subject = 'Restablecimiento de Contraseña Solicitado'
        message_body = (
            f"Hola {user.nombre_usuario},\n\n"
            f"Hemos recibido una solicitud para restablecer tu contraseña. "
            f"Haz clic en el siguiente enlace para continuar:\n"
            f"{reset_url}\n\n"
            f"Si no solicitaste esto, por favor ignora este correo.\n\n"
            f"Gracias,\nEl equipo de Ferremas"
        )
        
        send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [user.email])

        return Response({'message': 'Si tu correo está registrado, recibirás un email con instrucciones.'}, status=status.HTTP_200_OK)


# ---------------------------
# VISTA PARA CONFIRMAR EL RESETEO DE CONTRASEÑA
# ---------------------------
class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uidb64 = serializer.validated_data['uidb64']
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        try:
            # smart_str es preferible para decodificar bytes a str
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = Usuario.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist, DjangoUnicodeDecodeError):
            user = None

        if user is not None and PasswordResetTokenGenerator().check_token(user, token):
            user.set_password(new_password)
            user.save()
            # Registrar en la bitácora
            BitacoraActividad.objects.create(
                usuario=user,
                accion=f"El usuario {user.nombre_usuario} restableció su contraseña."
            )
            return Response({'message': 'Tu contraseña ha sido restablecida exitosamente.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'El enlace de restablecimiento es inválido o ha expirado.'}, status=status.HTTP_400_BAD_REQUEST)

# ---------------------------
# VISTA PERSONALIZADA PARA OBTENER TOKENS (LOGIN) Y REGISTRAR EN BITÁCORA
# ---------------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Puedes añadir claims personalizados al token aquí si lo necesitas
        # Por ejemplo:
        # token['nombre_usuario'] = user.nombre_usuario
        # token['rol'] = user.rol.nombre_rol if user.rol else None
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # 'self.user' es establecido por TokenObtainPairSerializer después de una validación exitosa.
        # Este es el punto donde el usuario se ha autenticado correctamente.
        if self.user:
            BitacoraActividad.objects.create(
                usuario=self.user,
                accion=f"El usuario {self.user.nombre_usuario} inició sesión (vía token)."
            )
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vista personalizada para el login que utiliza el CustomTokenObtainPairSerializer
    para registrar el inicio de sesión en la bitácora.
    """
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True) # Mantenemos raise_exception para ver errores de validación estándar
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except Exception as e: # Capturamos cualquier excepción de is_valid(raise_exception=True)
            # Puedes añadir un log más formal aquí si lo deseas, en lugar de print
            raise # Re-lanzamos la excepción para que DRF la maneje como normalmente lo haría

# ---------------------------
# VISTA PARA LOGOUT (INVALIDAR REFRESH TOKEN)
# ---------------------------
# Tu LogoutView ya está definida y parece correcta para invalidar tokens
# y registrar en la bitácora.
class LogoutView(APIView):
    """
    Vista para el logout de usuarios. Invalida el refresh token.
    """
    permission_classes = (permissions.IsAuthenticated,) # Solo usuarios autenticados pueden hacer logout

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"detail": "Refresh token no proporcionado."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            # Registrar cierre de sesión en la bitácora
            # request.user debería estar disponible debido a IsAuthenticated
            BitacoraActividad.objects.create(
                usuario=request.user,
                accion=f"El usuario {request.user.nombre_usuario} cerró sesión (token invalidado)."
            )
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            # Puedes añadir un log más formal aquí si lo deseas, en lugar de print
            return Response({"detail": "Error al procesar el logout o token inválido."}, status=status.HTTP_400_BAD_REQUEST)