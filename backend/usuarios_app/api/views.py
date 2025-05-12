from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status, generics
from rest_framework.views import APIView
from usuarios_app.models import Rol, Usuario, TipoPersonal, Personal, Cliente, BitacoraActividad # Asegúrate que Cliente esté importado
from .serializers import (
    RolSerializer, UsuarioSerializer, TipoPersonalSerializer,
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
        
        # La siguiente validación 'if not email:' ya no es estrictamente necesaria
        # porque el serializador se encarga de que el email sea requerido.
        if not email:
            return Response({'error': 'Email es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({'message': 'Tu contraseña ha sido restablecida exitosamente.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'El enlace de restablecimiento es inválido o ha expirado.'}, status=status.HTTP_400_BAD_REQUEST)