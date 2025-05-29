from rest_framework import permissions
from usuarios_app.models import Personal # Importa el modelo Personal para verificar roles y asignaciones

class CanManageInventarioSucursalBodega(permissions.BasePermission):
    """Permiso personalizado para controlar el acceso al inventario según roles y asignaciones de sucursal/bodega.
    Esta clase determina si un usuario tiene permiso para realizar una acción (ver, crear, editar, eliminar)
    sobre los datos del inventario.
    - Admins (is_staff): acceso total.
    - Personal:
        - Ver (list, retrieve): Cualquiera autenticado que tenga un perfil de Personal.
        - Modificar/Eliminar (update, partial_update, destroy):
            - Si tiene bodega_asignada: Solo inventario de su bodega asignada.
            - Si no tiene bodega_asignada pero sí sucursal: Solo inventario de cualquier bodega de su sucursal.
        - Crear (create):
            - Si tiene bodega_asignada: Solo en su bodega asignada.
            - Si no tiene bodega_asignada pero sí sucursal: Solo en bodegas de su sucursal.
    """

    def has_permission(self, request, view):
        # Este método se llama para todas las solicitudes a nivel de vista (lista o creación).
        # No tiene acceso al objeto específico todavía (por ejemplo, al crear o listar).

        # 1. Comprobación básica de autenticación:
        if not request.user or not request.user.is_authenticated:
            return False

        # 2. Permiso para administradores:
        if request.user.is_staff:
            return True

        # 3. Permisos para personal no administrador:
        if view.action in ['list', 'retrieve']:
            # Se permite si el usuario tiene un perfil de 'Personal' asociado.
            return hasattr(request.user, 'personal')

        # Para la acción de crear ('create'):
        if view.action == 'create':
            # Se permite si el usuario tiene un perfil de 'Personal' Y ese perfil de personal tiene una sucursal asignada.
            return hasattr(request.user, 'personal') and request.user.personal.sucursal is not None

        # Para otras acciones como 'update', 'partial_update', 'destroy':
        # Si el usuario es personal, se permite pasar a la siguiente fase de verificación
        return hasattr(request.user, 'personal')

    def has_object_permission(self, request, view, obj):
        # Este método se llama solo para acciones que operan sobre un objeto específico
        # 1. Comprobación básica de autenticación:
        if not request.user or not request.user.is_authenticated:
            return False

        # 2. Permiso para administradores:
        # Si el usuario es un administrador, tiene permiso sobre cualquier objeto.
        if request.user.is_staff:
            return True

        # 3. Permisos para personal no administrador sobre un objeto específico:
        # Esto aplica para acciones como 'update', 'partial_update', 'destroy'.
        if view.action in ['update', 'partial_update', 'destroy', 'agregar_stock']: # Añadimos 'agregar_stock'
            try:
                # Intenta obtener el perfil de 'Personal' del usuario.
                personal = request.user.personal
            except Personal.DoesNotExist:
                return False 
            if personal.bodega_asignada: # Si el personal tiene una bodega específica asignada:
                # Solo puede modificar el inventario si pertenece a su bodega asignada.
                return obj.bodega == personal.bodega_asignada
            elif personal.sucursal: # Si el personal tiene una sucursal asignada (pero no una bodega específica):
                # Puede modificar el inventario de cualquier bodega que pertenezca a su sucursal.
                return obj.bodega.sucursal == personal.sucursal
            return False # Si no tiene ni bodega asignada ni sucursal, no puede modificar.

        # 4. Denegar por defecto:
        # Si ninguna de las condiciones anteriores se cumple (por ejemplo, una acción no contemplada), se deniega el permiso para usuarios no administradores.
        return False