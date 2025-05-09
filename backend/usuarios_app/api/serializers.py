from rest_framework import serializers
from usuarios_app.models import Rol, Usuario, TipoPersonal, Personal, Cliente, BitacoraActividad

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

    class Meta:
        model = Usuario
        fields = [
            'id', 'nombre_usuario',
            'rol',          # Para lectura (objeto Rol serializado)
            'rol_id',       # Para escritura (ID del Rol)
            'cambio_password_pendiente',
            'is_active', 'is_staff', 'is_superuser', 'last_login',
            'groups',       # ManyToManyField, se espera una lista de IDs para escritura
            'user_permissions', # ManyToManyField, se espera una lista de IDs para escritura
            'password'
        ]
        extra_kwargs = {
            'password': {
                'write_only': True,  # No enviar la contraseña en la respuesta
                'style': {'input_type': 'password'} # Para la API Navegable
            },
            'last_login': {'read_only': True},
            'is_superuser': {'read_only': True}, # Generalmente manejado por createsuperuser
        }

    def create(self, validated_data):
        # El manager del modelo Usuario (UsuarioManager) tiene create_user
        # que maneja el hashing de la contraseña.
        groups_data = validated_data.pop('groups', None)
        user_permissions_data = validated_data.pop('user_permissions', None)

        # 'rol' ya será una instancia de Rol si 'rol_id' fue provisto, gracias a source='rol'
        user = Usuario.objects.create_user(**validated_data)

        if groups_data:
            user.groups.set(groups_data)
        if user_permissions_data:
            user.user_permissions.set(user_permissions_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        groups_data = validated_data.pop('groups', None)
        user_permissions_data = validated_data.pop('user_permissions', None)

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

        return instance

# ---------------------------
# PERSONAL
# ---------------------------
class TipoPersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPersonal
        fields = '__all__'

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