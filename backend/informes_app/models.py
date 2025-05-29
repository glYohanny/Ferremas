from django.db import models
from django.conf import settings
from django.utils import timezone
from productos_app.models import Producto
from marketing_app.models import Promocion


class Venta(models.Model):
    """Representa una transacción de venta realizada en una sucursal."""
    sucursal = models.ForeignKey('sucursales_app.Sucursal', on_delete=models.PROTECT, related_name='ventas_realizadas')
    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='ventas_como_vendedor', limit_choices_to={'is_staff': True})
    fecha_venta = models.DateTimeField(default=timezone.now)
    total_venta = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fecha_venta']

    def __str__(self):
        return f"Venta #{self.id} - {self.fecha_venta.strftime('%Y-%m-%d %H:%M')}"

class VentaDetalle(models.Model):
    """Representa un ítem individual dentro de una transacción de venta."""
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey('productos_app.Producto', on_delete=models.PROTECT, related_name='items_vendidos_en_informes')
    cantidad = models.PositiveIntegerField()
    precio_unitario_en_venta = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio del producto al momento de la venta, puede incluir descuentos específicos del ítem.")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    promocion_aplicada_item = models.ForeignKey('marketing_app.Promocion', on_delete=models.SET_NULL, null=True, blank=True, related_name='items_vendidos_con_esta_promocion')

    class Meta:
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Venta"

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario_en_venta
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Venta #{self.venta.id})"
