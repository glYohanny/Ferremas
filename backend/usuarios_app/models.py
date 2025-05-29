from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _



# --- Gestor para el modelo de Usuario Personalizado ---
class UsuarioManager(BaseUserManager):
    def create_user(self, nombre_usuario, email, password=None, **extra_fields):

        if not nombre_usuario:
            raise ValueError('El nombre de usuario debe ser establecido')
        if not email:
            raise ValueError('El email debe ser establecido')

        # Normalizar el nombre de usuario
        nombre_usuario = nombre_usuario.strip()
        email = self.normalize_email(email)

        # Crear una nueva instancia del modelo
        user = self.model(nombre_usuario=nombre_usuario, email=email, **extra_fields)

        # Establecer la contraseña de forma segura
        if password:
            user.set_password(password)
        else:
            user.set_password(None)

        # Guardar el usuario
        user.save(using=self._db)
        return user
    def create_superuser(self, nombre_usuario, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('cambio_password_pendiente', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(nombre_usuario, email, password, **extra_fields)

class Rol(models.Model):
    nombre_rol = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.nombre_rol

class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre_usuario = models.CharField(max_length=100, unique=True)
    email = models.EmailField(_('email address'), unique=True) # Temporarily allow null
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    cambio_password_pendiente = models.BooleanField(default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    is_active = models.BooleanField(default=True, verbose_name='activo')
    is_staff = models.BooleanField(default=False, verbose_name='es staff')
    # is_superuser es heredado de PermissionsMixin

    objects = UsuarioManager()

    USERNAME_FIELD = 'nombre_usuario'
    REQUIRED_FIELDS = ['email'] # Campos requeridos al crear un superusuario, además del USERNAME_FIELD y password

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="api_usuario_groups",
        related_query_name="usuario",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="api_usuario_permissions",
        related_query_name="usuario",
    )

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.nombre_usuario

class Personal(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    rut = models.CharField(max_length=12, unique=True)
    # nombre_completo = models.CharField(max_length=100) # Eliminado: se deriva de Usuario
    # email = models.EmailField(unique=True) # Eliminado: se usa el de Usuario. Si se necesita un email de contacto laboral diferente, se puede mantener.
    sucursal = models.ForeignKey('sucursales_app.Sucursal', on_delete=models.SET_NULL, null=True, blank=True)
    bodega_asignada = models.ForeignKey('sucursales_app.Bodega', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Bodega Asignada")

    class Meta:
        db_table = 'personal'
        verbose_name = 'Personal'
        verbose_name_plural = 'Personal'

    def __str__(self):
        name_parts = [self.usuario.first_name, self.usuario.last_name]
        full_name = " ".join(part for part in name_parts if part)
        return full_name.strip() or self.usuario.nombre_usuario

    @property
    def email_contacto(self):
        # Devuelve el email del usuario asociado.
        # Si necesitaras un email de contacto laboral *diferente* al del usuario,
        # entonces mantendrías un campo 'email' en este modelo Personal.
        return self.usuario.email

    @property
    def nombre_completo_display(self):
        name_parts = [self.usuario.first_name, self.usuario.last_name]
        full_name = " ".join(part for part in name_parts if part)
        return full_name.strip()

    def clean(self):
        super().clean()
        # Validar que la bodega asignada pertenezca a la sucursal del personal (si ambas están definidas)
        if self.bodega_asignada and self.sucursal:
            if self.bodega_asignada.sucursal != self.sucursal:
                from django.core.exceptions import ValidationError
                raise ValidationError({'bodega_asignada': _('La bodega asignada debe pertenecer a la sucursal del personal.')})

class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    direccion_detallada = models.TextField()
    telefono = models.CharField(max_length=15, blank=True, null=True)
    comuna = models.ForeignKey('geografia_app.Comuna', on_delete=models.PROTECT)

    class Meta:
        db_table = 'clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        name_parts = [self.usuario.first_name, self.usuario.last_name]
        full_name = " ".join(part for part in name_parts if part)
        return full_name.strip() or self.usuario.nombre_usuario

    @property
    def email_display(self):
        return self.usuario.email

    @property
    def nombre_completo_display(self):
        name_parts = [self.usuario.first_name, self.usuario.last_name]
        full_name = " ".join(part for part in name_parts if part)
        return full_name.strip()

class BitacoraActividad(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, help_text="Usuario que realizó la acción, o nulo si es del sistema")
    accion = models.TextField(help_text="Descripción de la acción realizada")
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bitacora_actividad'
        verbose_name = 'Bitácora de Actividad'
        verbose_name_plural = 'Bitácoras de Actividad'
        ordering = ['-fecha']
        indexes = [
            models.Index(fields=['fecha']),
            models.Index(fields=['usuario', 'fecha']),
        ]

    def __str__(self):
        user_str = self.usuario.nombre_usuario if self.usuario else "Sistema"
        return f"{user_str} - {self.accion[:50]}... - {self.fecha.strftime('%Y-%m-%d %H:%M')}"