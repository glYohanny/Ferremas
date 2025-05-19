from django.db import models
from django.conf import settings # Para referenciar al User model
from django.utils import timezone

# Es recomendable que el modelo Sucursal esté en su propia app, por ejemplo 'sucursales_app'
# from sucursales_app.models import Sucursal
# Por ahora, si no tienes la app sucursales_app, puedes definir un placeholder o crearla.
# Para este ejemplo, asumiremos que Sucursal se importará de otra app.
# Si Sucursal también se define en este archivo, ajusta la importación.

from productos_app.models import Producto
from marketing_app.models import Promocion  # Importar Promocion


class Venta(models.Model):
    # Asumimos que Sucursal está definida en sucursales_app.models.Sucursal
    # from sucursales_app.models import Sucursal
    sucursal = models.ForeignKey('sucursales_app.Sucursal', on_delete=models.PROTECT, related_name='ventas_realizadas')
    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='ventas_como_vendedor', limit_choices_to={'is_staff': True}) # O un filtro por rol específico
    # cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='compras_como_cliente')
    fecha_venta = models.DateTimeField(default=timezone.now)
    total_venta = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    # promocion_aplicada_general = models.ForeignKey(Promocion, on_delete=models.SET_NULL, null=True, blank=True, related_name='ventas_con_esta_promocion')

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fecha_venta']

    def __str__(self):
        return f"Venta #{self.id} - {self.fecha_venta.strftime('%Y-%m-%d %H:%M')}"

class VentaDetalle(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey('productos_app.Producto', on_delete=models.PROTECT, related_name='items_vendidos_en_informes') # Referencia como string o importar directamente
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
        # Aquí podrías añadir lógica para recalcular el Venta.total_venta si es necesario,
        # aunque a menudo es mejor manejarlo con señales o en la lógica de la vista de creación de ventas.

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Venta #{self.venta.id})"
