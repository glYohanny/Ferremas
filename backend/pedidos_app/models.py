from django.db import models

class EstadoPedido(models.Model):
    nombre_estado = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'estado_pedido'
        verbose_name = 'Estado de Pedido'
        verbose_name_plural = 'Estados de Pedidos'

    def __str__(self):
        return self.nombre_estado

class TipoEntrega(models.Model):
    descripcion_entrega = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'tipo_entrega'
        verbose_name = 'Tipo de Entrega'
        verbose_name_plural = 'Tipos de Entrega'

    def __str__(self):
        return self.descripcion_entrega

class Pedido(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # Considerar UUID
    cliente = models.ForeignKey('usuarios_app.Cliente', on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    estado_pedido = models.ForeignKey(EstadoPedido, on_delete=models.PROTECT)
    tipo_entrega = models.ForeignKey(TipoEntrega, on_delete=models.PROTECT)
    metodo_pago = models.ForeignKey('pagos_app.MetodoPago', on_delete=models.PROTECT)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # direccion_envio_json = models.JSONField(null=True, blank=True, help_text="Copia de la dirección de envío al momento del pedido")
    # transaccion_asociada = models.ForeignKey('pagos_app.TransaccionTarjetaCliente', on_delete=models.SET_NULL, null=True, blank=True)

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
        return f"Pedido {self.pk} - {self.cliente.nombre_completo} - {self.fecha.strftime('%Y-%m-%d')}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey('productos_app.Producto', on_delete=models.PROTECT, verbose_name="Producto")
    # nombre_producto_historico = models.CharField(max_length=100, help_text="Nombre del producto al momento de la compra")
    # codigo_producto_historico = models.CharField(max_length=50, help_text="Código del producto al momento de la compra")
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
        # Considerar una señal o método en el modelo Pedido para recalcular el total del pedido

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre_producto} para Pedido {self.pedido.pk}"

class PedidoProcesadoPor(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, primary_key=True)
    vendedor = models.ForeignKey('usuarios_app.Personal', on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos_vendidos')
    bodeguero = models.ForeignKey('usuarios_app.Personal', on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos_preparados')
    # fecha_asignacion_vendedor = models.DateTimeField(null=True, blank=True)
    # fecha_asignacion_bodeguero = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'pedido_procesado_por'
        verbose_name = 'Pedido Procesado Por'
        verbose_name_plural = 'Pedidos Procesados Por'

    def __str__(self):
        return f"Procesamiento Pedido {self.pedido.pk}"