from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db import transaction
from pedidos_app.models import (
    EstadoPedido, TipoEntrega, Pedido, DetallePedido, PedidoProcesadoPor
)
from productos_app.models import Producto # Necesario para acceder al stock
from geografia_app.models import Comuna # Para validar la comuna
from .serializers import (
    EstadoPedidoSerializer, TipoEntregaSerializer, PedidoSerializer,
    DetallePedidoOutputSerializer, PedidoProcesadoPorSerializer # Cambiado DetallePedidoSerializer a DetallePedidoOutputSerializer
)
# ---------------------------
# PEDIDOS
# ---------------------------
class EstadoPedidoViewSet(viewsets.ModelViewSet):
    queryset = EstadoPedido.objects.all()
    serializer_class = EstadoPedidoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Permitir lectura a autenticados, escritura a admins

class TipoEntregaViewSet(viewsets.ModelViewSet):
    queryset = TipoEntrega.objects.all()
    serializer_class = TipoEntregaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Permitir lectura a autenticados, escritura a admins

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff: # O una comprobación de rol más específica si tienes roles de admin
            return Pedido.objects.all().prefetch_related('detalles__producto', 'cliente', 'estado_pedido', 'tipo_entrega', 'metodo_pago', 'comuna_envio')
        return Pedido.objects.filter(cliente=user).prefetch_related('detalles__producto', 'cliente', 'estado_pedido', 'tipo_entrega', 'metodo_pago', 'comuna_envio')

    @transaction.atomic # Asegura que todas las operaciones de BD se completen o ninguna
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        items_data = serializer.validated_data.pop('items_input', [])
        if not items_data:
            return Response({"detail": "El pedido debe contener al menos un ítem."}, status=status.HTTP_400_BAD_REQUEST)

        # El frontend envía comuna_envio_id, que el serializer convierte a comuna_envio (objeto)
        # y estado_pedido_id, tipo_entrega_id, metodo_pago_id que se convierten a sus objetos.
        # El cliente se asigna automáticamente.
        
        # Crear el pedido principal
        # Los campos como nombre_completo_contacto, email_contacto, etc., vienen directamente del request.data
        # y son manejados por el serializer.
        pedido = serializer.save(cliente=request.user)

        total_pedido_calculado = 0

        for item_data in items_data:
            producto_id = item_data.get('producto_id')
            cantidad = item_data.get('cantidad')

            try:
                producto = Producto.objects.select_for_update().get(id=producto_id) # Bloquear para actualizar stock

                if producto.stock < cantidad:
                    # Si el stock es insuficiente, revertir la transacción
                    transaction.set_rollback(True)
                    return Response(
                        {"detail": f"Stock insuficiente para el producto: {producto.nombre_producto}. Disponible: {producto.stock}, Solicitado: {cantidad}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Crear el detalle del pedido
                detalle = DetallePedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio # Usar el precio actual del producto
                    # El subtotal se calcula automáticamente por el método save() de DetallePedido
                )
                total_pedido_calculado += detalle.subtotal

                # Reducir el stock del producto
                producto.stock -= cantidad
                producto.save(update_fields=['stock'])

            except Producto.DoesNotExist:
                transaction.set_rollback(True)
                return Response({"detail": f"Producto con ID {producto_id} no encontrado."}, status=status.HTTP_400_BAD_REQUEST)
        
        # El total del pedido se actualiza mediante la señal post_save/post_delete en DetallePedido.
        # No es necesario actualizarlo manualmente aquí si la señal está activa y funcionando.
        # Si quieres asegurar, puedes hacer: pedido.refresh_from_db() después del bucle.

        headers = self.get_success_headers(serializer.data) # serializer.data aquí es del pedido antes de items
        # Para devolver el pedido completo con items, serializamos el objeto 'pedido' que ya tiene los items
        response_serializer = self.get_serializer(pedido)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class DetallePedidoViewSet(viewsets.ModelViewSet):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoOutputSerializer # Usar el serializador de salida definido
    permission_classes = [permissions.IsAuthenticated]

class PedidoProcesadoPorViewSet(viewsets.ModelViewSet):
    queryset = PedidoProcesadoPor.objects.all()
    serializer_class = PedidoProcesadoPorSerializer
    permission_classes = [permissions.IsAuthenticated] # Personal autorizado