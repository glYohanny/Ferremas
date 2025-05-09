from django.db import models
from django.utils import timezone

class Promocion(models.Model):
    descripcion = models.TextField()
    porcentaje_descuento = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    cantidad_minima_productos = models.PositiveIntegerField(default=1, help_text="Cantidad mínima de un producto para aplicar la promo")
    # monto_minimo_compra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    activa = models.BooleanField(default=True)
    # codigo_promocion = models.CharField(max_length=50, unique=True, blank=True, null=True, help_text="Código de cupón opcional")

    class Meta:
        db_table = 'promocion'
        verbose_name = 'Promoción'
        verbose_name_plural = 'Promociones'
        indexes = [
            models.Index(fields=['fecha_inicio', 'fecha_fin']),
            models.Index(fields=['activa', 'fecha_inicio', 'fecha_fin']),
        ]

    def __str__(self):
        return self.descripcion[:50] + "..." if len(self.descripcion) > 50 else self.descripcion

class ProductoPromocion(models.Model):
    producto = models.ForeignKey('productos_app.Producto', on_delete=models.CASCADE)
    promocion = models.ForeignKey(Promocion, on_delete=models.CASCADE)
    # precio_con_descuento_fijo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Si el descuento es un precio fijo en lugar de porcentaje")

    class Meta:
        db_table = 'producto_promocion'
        unique_together = ('producto', 'promocion')
        verbose_name = 'Producto en Promoción'
        verbose_name_plural = 'Productos en Promoción'

    def __str__(self):
        return f"{self.producto.nombre_producto} en promoción ({self.promocion.descripcion[:20]}...)"

class Notificacion(models.Model):
    # TIPO_NOTIFICACION_CHOICES = [ ('PEDIDO', 'Pedido'), ('STOCK', 'Stock'), ('PROMOCION', 'Promoción'), ('GENERAL', 'General'), ]
    # tipo_notificacion = models.CharField(max_length=20, choices=TIPO_NOTIFICACION_CHOICES, default='GENERAL')
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    # url_destino = models.URLField(blank=True, null=True, help_text="URL a la que redirigir al hacer clic")

    class Meta:
        db_table = 'notificacion'
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-fecha_envio']
        indexes = [
            models.Index(fields=['fecha_envio']),
        ]

    def __str__(self):
        return self.titulo

class ClienteNotificacion(models.Model):
    cliente = models.ForeignKey('usuarios_app.Cliente', on_delete=models.CASCADE)
    notificacion = models.ForeignKey(Notificacion, on_delete=models.CASCADE)
    leido = models.BooleanField(default=False)
    fecha_lectura = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'cliente_notificacion'
        unique_together = ('cliente', 'notificacion')
        verbose_name = 'Notificación de Cliente'
        verbose_name_plural = 'Notificaciones de Clientes'

    def save(self, *args, **kwargs):
        if self.leido and not self.fecha_lectura:
            self.fecha_lectura = timezone.now()
        elif not self.leido:
            self.fecha_lectura = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Notif: '{self.notificacion.titulo[:20]}' para {self.cliente.nombre_completo} (Leído: {self.leido})"