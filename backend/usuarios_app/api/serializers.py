from rest_framework import serializers
from usuarios_app.models import Rol, Usuario,  Personal, Cliente, BitacoraActividad
from geografia_app.models import Region, Comuna
from django.db import transaction # Para transacciones atómicas
from sucursales_app.models import Sucursal

# ---------------------------
# ROLES Y USUARIOS
# ---------------------------
class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    # Para mostrar detalles del Rol en la lectura y aceptar ID en la escritura
    rol = RolSerializer(read_only=True)
    rol_id = serializers.PrimaryKeyRelatedField(
        queryset=Rol.objects.all(), source='rol', write_only=True, allow_null=True, required=False
    )
        # Campos para la creación de perfiles (opcionales y solo para escritura)
    # Para Personal
    rut_personal = serializers.CharField(write_only=True, required=False, allow_blank=True, max_length=12)
    sucursal_id_personal = serializers.PrimaryKeyRelatedField(
        queryset=Sucursal.objects.all(), source='sucursal_personal', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Usuario
        fields = [
            'id', 'nombre_usuario', 'email', # Añadido email para que sea visible y editable por admin
            'first_name', 'last_name', # Añadidos para que sean visibles y editables por admin
            'rol',          # Para lectura (objeto Rol serializado)
            'rol_id',       # Para escritura (ID del Rol)
            'cambio_password_pendiente',
            'is_active', 'is_staff', 'is_superuser', 'last_login',
            'groups',       # ManyToManyField, se espera una lista de IDs para escritura
            'user_permissions', # ManyToManyField, se espera una lista de IDs para escritura
            'password',
            # Campos para perfiles
            'rut_personal', 'sucursal_id_personal',
            # 'direccion_detallada_cliente', 'telefono_cliente', 'comuna_id_cliente',
        ]
        extra_kwargs = {
            'password': {
                'write_only': True,  # No enviar la contraseña en la respuesta
                'style': {'input_type': 'password'} # Para la API Navegable
            },
            'last_login': {'read_only': True},
            'is_superuser': {'read_only': True}, # Generalmente manejado por createsuperuser
            'email': {'required': False}, # Admin podría crear usuario sin email inicialmente, o actualizarlo
            'first_name': {'required': False},
            'last_name': {'required': False},
        }
        
    @transaction.atomic
    def create(self, validated_data):
        groups_data = validated_data.pop('groups', None)
        user_permissions_data = validated_data.pop('user_permissions', None)

        # Extraer datos de perfiles si existen, ANTES de pasarlos a create_user
        rut_personal_data = validated_data.pop('rut_personal', None)
        # 'sucursal_personal' es el nombre que tendrá en validated_data debido al 'source' en el campo del serializador
        sucursal_personal_data = validated_data.pop('sucursal_personal', None) 

        # 'rol' ya será una instancia de Rol si 'rol_id' fue provisto, gracias a source='rol'
        # El método create_user de UsuarioManager maneja el hashing de la contraseña.
        user = Usuario.objects.create_user(**validated_data)

        if groups_data:
            user.groups.set(groups_data)
        if user_permissions_data:
            user.user_permissions.set(user_permissions_data)

        # Crear perfil de Personal si el rol lo indica y se proporcionaron datos
        if user.rol: # Asegurarse que el usuario tiene un rol asignado
           # Ajusta los nombres de roles según tu sistema exactamente como están en la BD
           roles_que_requieren_personal = ['Administrador', 'Vendedor', 'Bodeguero', 'Contador'] # Ejemplo
           if user.rol.nombre_rol in roles_que_requieren_personal and rut_personal_data:
               Personal.objects.create(
                   usuario=user,
                   rut=rut_personal_data,
                   sucursal=sucursal_personal_data # Puede ser None si no se proporcionó y el modelo lo permite
               )

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        groups_data = validated_data.pop('groups', None)
        user_permissions_data = validated_data.pop('user_permissions', None)
        rut_personal_data = validated_data.pop('rut_personal', None)
        sucursal_personal_data = validated_data.pop('sucursal_personal', None)

        # Actualizar otros campos
        # 'rol' ya será una instancia de Rol si 'rol_id' fue provisto
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save() # Guardar la instancia después de establecer atributos y contraseña

        # Actualizar campos ManyToMany después de guardar la instancia
        if groups_data is not None: # Permite limpiar grupos con una lista vacía
            instance.groups.set(groups_data)
        if user_permissions_data is not None: # Permite limpiar permisos
            instance.user_permissions.set(user_permissions_data)

        # Actualizar o crear perfil de Personal si es necesario y se proporcionaron datos
        if instance.rol:
            roles_que_requieren_personal = ['Administrador', 'Vendedor', 'Bodeguero', 'Contador'] # Ejemplo
            if instance.rol.nombre_rol in roles_que_requieren_personal and rut_personal_data:
                personal_profile, created = Personal.objects.update_or_create(
                    usuario=instance,
                    defaults={
                        'rut': rut_personal_data,
                        'sucursal': sucursal_personal_data
                    }
                )
            elif hasattr(instance, 'personal') and instance.rol.nombre_rol not in roles_que_requieren_personal:
                # Opcional: si el rol cambia a uno que no requiere personal, podrías eliminar el perfil Personal
                instance.personal.delete()

        return instance

# ---------------------------
# PERSONAL
# ---------------------------

class PersonalSerializer(serializers.ModelSerializer):
    # 'usuario' es la clave primaria (OneToOneField). DRF lo manejará como un campo de ID.
    # Para mostrar detalles del usuario, sucursal, tipo en lectura:
    # usuario_detalle = UsuarioSerializer(source='usuario', read_only=True) # Renombrar para evitar conflicto con el campo 'usuario' (ID)
    # sucursal = SucursalSerializer(read_only=True)
    # tipo = TipoPersonalSerializer(read_only=True)
    class Meta:
        model = Personal
        fields = '__all__'

# ---------------------------
# CLIENTES
# ---------------------------
class ClienteSerializer(serializers.ModelSerializer):
    # 'usuario' es la clave primaria (OneToOneField).
    class Meta:
        model = Cliente
        fields = '__all__'

# ---------------------------
# BITÁCORA
# ---------------------------
class BitacoraActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitacoraActividad
        fields = '__all__'

# ---------------------------
# SERIALIZER PARA REGISTRO DE CLIENTES
# ---------------------------
class ClienteRegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8 # Opcional: añade una validación de longitud mínima
    )
    # Puedes añadir campos específicos del modelo Cliente aquí si quieres capturarlos durante el registro.
    # Por ejemplo, si Cliente tiene un campo 'telefono':
    # telefono_cliente = serializers.CharField(required=False, allow_blank=True, write_only=True)
    direccion_detallada = serializers.CharField(write_only=True, required=True)
    telefono = serializers.CharField(write_only=True, required=False, allow_blank=True, max_length=15)
    comuna_id = serializers.PrimaryKeyRelatedField(
        queryset=Comuna.objects.all(), write_only=True, source='comuna' # source='comuna' si el campo en Cliente es 'comuna'
    )
    class Meta:
        model = Usuario # El registro crea un Usuario
        fields = (
            'id', 'nombre_usuario', 'email', 'password', 
            'first_name', 'last_name', # Para el Usuario y para derivar nombre_completo del Cliente
            'direccion_detallada', 'telefono', 'comuna_id' # Campos para el Cliente
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}, # Hacer el email obligatorio para el registro
            'first_name': {'required': True}, # Requerido para nombre_completo
            'last_name': {'required': True},  # Requerido para nombre_completo
        }

    @transaction.atomic
    def create(self, validated_data):
        # Extraer campos específicos del cliente y otros que no van directamente a Usuario.objects.create_user
        direccion_cliente_data = validated_data.pop('direccion_detallada')
        telefono_cliente_data = validated_data.pop('telefono', None)
        comuna_cliente_data = validated_data.pop('comuna') # 'comuna' por el source='comuna'

        # Los campos restantes en validated_data (nombre_usuario, email, password, first_name, last_name)
        # son para el modelo Usuario.

        # Crear el Usuario
        # Primero, obtenemos el rol de "Cliente"
        try:
            rol_cliente = Rol.objects.get(nombre_rol='Cliente') # Asegúrate que el nombre_rol sea exacto
        except Rol.DoesNotExist:
            # Manejar el caso donde el rol "Cliente" no existe.
            # Podrías crearlo aquí o lanzar un error más específico.
            # Por ahora, lanzaremos un error genérico para que sepas que falta.
            raise serializers.ValidationError("El rol 'Cliente' no está configurado en el sistema.")
        
        # El método create_user de tu UsuarioManager se encargará del hashing de la contraseña
        # y ahora espera 'email'.
        validated_data['rol'] = rol_cliente # Asignamos el rol al diccionario de datos validados
        user = Usuario.objects.create_user(**validated_data)

        # Crear el perfil de Cliente asociado
        Cliente.objects.create(
            usuario=user,
            direccion_detallada=direccion_cliente_data,
            telefono=telefono_cliente_data,
            comuna=comuna_cliente_data
        )
        return user

# ---------------------------
# SERIALIZER PARA SOLICITUD DE RESETEO DE CONTRASEÑA
# ---------------------------
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    # No necesitamos métodos create() o update() aquí ya que solo es para la entrada.

# ---------------------------
# SERIALIZER PARA CONFIRMAR EL RESETEO DE CONTRASEÑA
# ---------------------------
class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8 # Puedes ajustar o añadir más validadores de contraseña aquí
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Las contraseñas no coinciden."})
        # Aquí podrías añadir más validaciones de complejidad de contraseña si lo deseas
        return attrs