from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from inventario_app.models import Inventario, HistorialStock
from usuarios_app.models import Personal # Para la validación en perform_create
from .serializers import InventarioSerializer, HistorialStockSerializer, AgregarStockSerializer # Añadir AgregarStockSerializer
from .permissions import CanManageInventarioSucursalBodega

# ---------------------------
# INVENTARIO Y HISTORIAL
# ---------------------------

class InventarioViewSet(viewsets.ModelViewSet):
    """Gestiona el inventario de productos por bodega, incluyendo la creación de historial de stock."""
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer
    permission_classes = [CanManageInventarioSucursalBodega]

    def perform_create(self, serializer):
        # Validación adicional de permisos para creación por personal no-staff,
        # basada en la bodega seleccionada en los datos de la solicitud.
        user = self.request.user
        if not user.is_staff:
            try:
                personal = user.personal
                bodega_seleccionada_id = self.request.data.get('bodega_id') # ID de la bodega desde el request payload
                if not bodega_seleccionada_id:
                    raise PermissionDenied("Debe seleccionar una bodega.")

                if personal.bodega_asignada:
                    if str(personal.bodega_asignada.id) != str(bodega_seleccionada_id): # Comparar como strings por si acaso
                        raise PermissionDenied("Solo puedes crear inventario en tu bodega asignada.")
                elif personal.sucursal:
                    if not personal.sucursal.bodegas.filter(id=bodega_seleccionada_id).exists():
                        raise PermissionDenied("Solo puedes crear inventario en bodegas de tu sucursal.")
                else:
                    raise PermissionDenied("No tienes una sucursal o bodega asignada para gestionar inventario.")
            except Personal.DoesNotExist:
                raise PermissionDenied("No tienes perfil de personal para gestionar inventario.")
        inventario = serializer.save()
        motivo_creacion = self.request.data.get('motivo_ajuste', f"Creación inicial de stock en bodega {inventario.bodega.nombre_bodega}.")

        HistorialStock.objects.create(
            producto=inventario.producto,
            bodega=inventario.bodega,
            cantidad_cambiada=inventario.cantidad,
            motivo=motivo_creacion,
            # Si tu modelo HistorialStock tiene 'usuario_responsable':
            # usuario_responsable=self.request.user if self.request.user.is_authenticated else None
        )

    def perform_update(self, serializer):
        # Obtener la instancia antes de la actualización para comparar la cantidad
        inventario_antes = serializer.instance
        cantidad_antes = inventario_antes.cantidad

        inventario_despues = serializer.save()
        cantidad_despues = inventario_despues.cantidad

        cambio_cantidad = cantidad_despues - cantidad_antes

        if cambio_cantidad != 0:
            motivo_actualizacion = self.request.data.get('motivo_ajuste', f"Ajuste de stock en bodega {inventario_despues.bodega.nombre_bodega}.")
            if not self.request.data.get('motivo_ajuste') and cambio_cantidad > 0:
                 motivo_actualizacion = f"Entrada de stock en bodega {inventario_despues.bodega.nombre_bodega}."
            elif not self.request.data.get('motivo_ajuste') and cambio_cantidad < 0:
                motivo_actualizacion = f"Salida de stock en bodega {inventario_despues.bodega.nombre_bodega}."

            HistorialStock.objects.create(
                producto=inventario_despues.producto,
                bodega=inventario_despues.bodega,
                cantidad_cambiada=cambio_cantidad,
                motivo=motivo_actualizacion,
                # Si tu modelo HistorialStock tiene 'usuario_responsable':
                # usuario_responsable=self.request.user if self.request.user.is_authenticated else None
            )

    @action(detail=True, methods=['post'], serializer_class=AgregarStockSerializer, permission_classes=[CanManageInventarioSucursalBodega])
    def agregar_stock(self, request, pk=None):
        """
        Agrega una cantidad específica al stock de un inventario existente.
        """
        inventario = self.get_object() # Obtiene la instancia de Inventario. Los permisos de objeto ya se verifican aquí.

        serializer = self.get_serializer(data=request.data) # Usa AgregarStockSerializer
        serializer.is_valid(raise_exception=True)

        cantidad_a_agregar = serializer.validated_data['cantidad_a_agregar']
        motivo_proporcionado = serializer.validated_data.get('motivo')

        motivo_final = motivo_proporcionado if motivo_proporcionado else f"Entrada de stock manual en bodega {inventario.bodega.nombre_bodega}."

        # Actualizar la cantidad en el inventario
        inventario.cantidad += cantidad_a_agregar
        inventario.save(update_fields=['cantidad', 'fecha_actualizacion'])

        # Crear registro en el historial de stock
        HistorialStock.objects.create(
            producto=inventario.producto,
            bodega=inventario.bodega,
            cantidad_cambiada=cantidad_a_agregar, # Positivo para entrada
            motivo=motivo_final
            # Si tienes 'usuario_responsable' en HistorialStock:
            # usuario_responsable=request.user if request.user.is_authenticated else None
        )

        return Response(InventarioSerializer(inventario).data, status=status.HTTP_200_OK)

class HistorialStockViewSet(viewsets.ReadOnlyModelViewSet):
    """Proporciona acceso de solo lectura al historial de cambios de stock."""
    queryset = HistorialStock.objects.all()
    serializer_class = HistorialStockSerializer
    permission_classes = [CanManageInventarioSucursalBodega]