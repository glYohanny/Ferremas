from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
# Define los posibles estados en los que se puede encontrar un pedido.

class EstadoPedido(models.Model):
    nombre_estado = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'estado_pedido'
        verbose_name = 'Estado de Pedido'
        verbose_name_plural = 'Estados de Pedidos'

    def __str__(self):
        return self.nombre_estado

# Define los diferentes tipos de entrega disponibles para un pedido.
class TipoEntrega(models.Model):
    descripcion_entrega = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'tipo_entrega'
        verbose_name = 'Tipo de Entrega'
        verbose_name_plural = 'Tipos de Entrega'

    def __str__(self):
        return self.descripcion_entrega

# Representa un pedido realizado por un cliente.
class Pedido(models.Model):
    cliente = models.ForeignKey('usuarios_app.Usuario', on_delete=models.PROTECT, related_name='pedidos')
    fecha = models.DateTimeField(auto_now_add=True)
    estado_pedido = models.ForeignKey(EstadoPedido, on_delete=models.PROTECT)
    tipo_entrega = models.ForeignKey(TipoEntrega, on_delete=models.PROTECT)
    metodo_pago = models.ForeignKey('pagos_app.MetodoPago', on_delete=models.PROTECT)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sucursal = models.ForeignKey(
        'sucursales_app.Sucursal', 
        on_delete=models.SET_NULL, # O models.PROTECT si una sucursal no puede ser eliminada si tiene pedidos
        null=True, blank=True, # Permite pedidos sin sucursal asignada, o hazlo no nulo si siempre debe tener una.
        related_name='pedidos_originados_en_sucursal',
        help_text="Sucursal a la que se asocia este pedido (para ventas, gestión, etc.)"
    )

    nombre_completo_contacto = models.CharField(max_length=255, help_text="Nombre completo para el contacto del pedido", null=True, blank=True)
    email_contacto = models.EmailField(help_text="Email de contacto para el pedido", null=True, blank=True)
    telefono_contacto = models.CharField(max_length=20, help_text="Teléfono de contacto para el pedido", null=True, blank=True)
    direccion_envio = models.CharField(max_length=255, help_text="Dirección de envío completa", null=True, blank=True)
    comuna_envio = models.ForeignKey('geografia_app.Comuna', on_delete=models.PROTECT, related_name='pedidos_enviados_aqui', help_text="Comuna de envío", null=True, blank=True)
    webpay_token = models.CharField(max_length=255, null=True, blank=True, help_text="Token de la transacción de Webpay")

    class Meta:
        db_table = 'pedidos'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-fecha']
        indexes = [
            models.Index(fields=['fecha']),
            models.Index(fields=['cliente', 'fecha']),
            models.Index(fields=['estado_pedido']),
        ]

    def __str__(self):
        return f"Pedido {self.pk} - {self.cliente.nombre_usuario if self.cliente else self.email_contacto} - {self.fecha.strftime('%Y-%m-%d')}"

# Representa un ítem individual (producto) dentro de un pedido.
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey('productos_app.Producto', on_delete=models.PROTECT, verbose_name="Producto")
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio unitario al momento de la compra")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detalle_pedido'
        verbose_name = 'Detalle de Pedido'
        verbose_name_plural = 'Detalles de Pedidos'
        unique_together = ('pedido', 'producto')

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre_producto} para Pedido {self.pedido.pk}"

# Registra qué personal (vendedor, bodeguero) procesó un pedido.
class PedidoProcesadoPor(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, primary_key=True)
    vendedor = models.ForeignKey('usuarios_app.Personal', on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos_vendidos')
    bodeguero = models.ForeignKey('usuarios_app.Personal', on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos_preparados')

    class Meta:
        db_table = 'pedido_procesado_por'
        verbose_name = 'Pedido Procesado Por'
        verbose_name_plural = 'Pedidos Procesados Por'

    def __str__(self):
        return f"Procesamiento Pedido {self.pedido.pk}"

@receiver(post_save, sender=DetallePedido)
@receiver(post_delete, sender=DetallePedido)
def actualizar_total_pedido(sender, instance, **kwargs):
    """
    Actualiza el campo 'total' del Pedido asociado cada vez que
    un DetallePedido se guarda o se elimina.
    """
    pedido = instance.pedido
    # Calcula el nuevo total sumando los subtotales de todos los detalles del pedido.
    # Si no hay detalles, el total será 0.00.
    nuevo_total = pedido.detalles.aggregate(
        total_calculado=Sum('subtotal')
    )['total_calculado'] or 0.00

    if pedido.total != nuevo_total:
        Pedido.objects.filter(pk=pedido.pk).update(total=nuevo_total)