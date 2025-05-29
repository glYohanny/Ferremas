from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db import transaction
from pedidos_app.models import (
    EstadoPedido, TipoEntrega, Pedido, DetallePedido, PedidoProcesadoPor
)
from productos_app.models import Producto # Necesario para acceder al stock
from geografia_app.models import Comuna # Para validar la comuna
from usuarios_app.models import Cliente # Para asignar el cliente al pedido
# --- INICIO: Importaciones para manejo de stock ---
from inventario_app.models import Inventario, HistorialStock
from sucursales_app.models import Bodega
# --- FIN: Importaciones para manejo de stock ---
from .serializers import (
    EstadoPedidoSerializer, TipoEntregaSerializer, PedidoSerializer,
    DetallePedidoOutputSerializer, PedidoProcesadoPorSerializer # Cambiado DetallePedidoSerializer a DetallePedidoOutputSerializer
)
# ---------------------------
# PEDIDOS
# ---------------------------
class EstadoPedidoViewSet(viewsets.ModelViewSet):
    """ViewSet para visualizar y editar los estados de los pedidos."""
    queryset = EstadoPedido.objects.all()
    serializer_class = EstadoPedidoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Permitir lectura a autenticados, escritura a admins

class TipoEntregaViewSet(viewsets.ModelViewSet):
    """ViewSet para visualizar y editar los tipos de entrega."""
    queryset = TipoEntrega.objects.all()
    serializer_class = TipoEntregaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Permitir lectura a autenticados, escritura a admins

class PedidoViewSet(viewsets.ModelViewSet):
    """ViewSet para la gestión completa de pedidos, incluyendo creación y manejo de stock."""
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Pedido.objects.none()

        common_prefetch = ['detalles__producto', 'cliente', 'estado_pedido',
                           'tipo_entrega', 'metodo_pago', 'comuna_envio', 'sucursal']

        if user.is_staff:
            return Pedido.objects.all().prefetch_related(*common_prefetch)

        return Pedido.objects.filter(cliente=user).prefetch_related(*common_prefetch)


    @transaction.atomic # Asegura que todas las operaciones de BD se completen o ninguna
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        items_data = serializer.validated_data.pop('items_input', [])
        if not items_data:
            return Response({"detail": "El pedido debe contener al menos un ítem."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Cliente.objects.get(usuario=request.user) 
        except Cliente.DoesNotExist:
            return Response({"detail": "El usuario actual no tiene un perfil de cliente asociado."}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener el estado de pedido "En Proceso" por defecto
        try:
            estado_en_proceso = EstadoPedido.objects.get(nombre_estado="En Proceso")
        except EstadoPedido.DoesNotExist:
            return Response(
                {"detail": "El estado de pedido 'En Proceso' no existe. Contacte a administración."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR 
            )

        pedido = serializer.save(cliente=request.user, estado_pedido=estado_en_proceso)

        # Identificar la bodega de la sucursal para el manejo de stock
        if not pedido.sucursal:
            transaction.set_rollback(True)
            return Response(
                {"detail": "El pedido debe estar asociado a una sucursal para procesar el stock."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            # --- ¡¡¡IMPORTANTE: Ajusta 'TIENDA' al tipo de bodega de venta directa en tu sistema!!! ---
            bodega_venta_directa = Bodega.objects.get(sucursal=pedido.sucursal, tipo_bodega='TIENDA')
        except Bodega.DoesNotExist:
            transaction.set_rollback(True)
            return Response({"detail": f"No se encontró una bodega de tipo 'TIENDA' para la sucursal {pedido.sucursal.nombre_sucursal}. No se puede procesar el pedido."}, status=status.HTTP_400_BAD_REQUEST)
        except Bodega.MultipleObjectsReturned:
            transaction.set_rollback(True)
            return Response({"detail": f"Múltiples bodegas de tipo 'TIENDA' encontradas para la sucursal {pedido.sucursal.nombre_sucursal}. Contacte a administración."}, status=status.HTTP_400_BAD_REQUEST)

        total_pedido_calculado = 0

        for item_data in items_data:
            producto_id = item_data.get('producto_id')
            cantidad = item_data.get('cantidad')

            try:
                producto = Producto.objects.select_for_update().get(id=producto_id) # Bloquear para actualizar stock
                
                # Verificar y descontar stock del Inventario de la bodega específica
                try:
                    inventario_item, created = Inventario.objects.select_for_update().get_or_create(
                        producto=producto,
                        bodega=bodega_venta_directa,
                        defaults={'cantidad': 0} # Si no existe, se crea con 0 stock
                    )
                except Exception as e: # Captura errores más genéricos durante get_or_create
                    transaction.set_rollback(True)
                    return Response({"detail": f"Error al acceder al inventario para {producto.nombre_producto} en {bodega_venta_directa.nombre_bodega}: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                if inventario_item.cantidad < cantidad:
                    transaction.set_rollback(True)
                    return Response(
                        {"detail": f"Stock insuficiente para el producto: {producto.nombre_producto} en la bodega {bodega_venta_directa.nombre_bodega}. "
                                   f"Disponible: {inventario_item.cantidad}, Solicitado: {cantidad}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                detalle = DetallePedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio # Usar el precio actual del producto
                )
                total_pedido_calculado += detalle.subtotal

                # Reducir el stock del inventario_item
                inventario_item.cantidad -= cantidad
                inventario_item.save(update_fields=['cantidad'])

                HistorialStock.objects.create(
                    producto=producto,
                    bodega=bodega_venta_directa,
                    cantidad_cambiada=-cantidad, # Negativo para salida
                    motivo=f"Venta - Pedido #{pedido.id}"
                )

            except Producto.DoesNotExist:
                transaction.set_rollback(True)
                return Response({"detail": f"Producto con ID {producto_id} no encontrado."}, status=status.HTTP_400_BAD_REQUEST)
        
        # El total del pedido se actualiza mediante la señal post_save/post_delete de DetallePedido.

        headers = self.get_success_headers(serializer.data)
        response_serializer = self.get_serializer(pedido)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class DetallePedidoViewSet(viewsets.ModelViewSet):
    """ViewSet para visualizar y (potencialmente) editar los detalles de un pedido."""
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoOutputSerializer # Usar el serializador de salida definido
    permission_classes = [permissions.IsAuthenticated]

class PedidoProcesadoPorViewSet(viewsets.ModelViewSet):
    """ViewSet para registrar y visualizar qué personal procesó un pedido."""
    queryset = PedidoProcesadoPor.objects.all()
    serializer_class = PedidoProcesadoPorSerializer
    permission_classes = [permissions.IsAuthenticated] # Personal autorizado