from django.db import models

class Inventario(models.Model):
    """Representa la cantidad de un producto específico en una bodega determinada."""
    producto = models.ForeignKey('productos_app.Producto', on_delete=models.CASCADE)
    bodega = models.ForeignKey('sucursales_app.Bodega', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inventario'
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        unique_together = ('producto', 'bodega')
        indexes = [
            models.Index(fields=['fecha_actualizacion']),
        ]

    def __str__(self):
        return f"{self.producto.nombre_producto} en {self.bodega.nombre_bodega}: {self.cantidad}"

class HistorialStock(models.Model):
    """Registra los cambios en el stock de productos, como entradas o salidas."""
    producto = models.ForeignKey('productos_app.Producto', on_delete=models.CASCADE)
    bodega = models.ForeignKey('sucursales_app.Bodega', on_delete=models.CASCADE, null=True, blank=True)
    cantidad_cambiada = models.IntegerField(help_text="Positivo para entrada, negativo para salida")
    motivo = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    # usuario_responsable = models.ForeignKey('usuarios_app.Usuario', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'historial_stock'
        verbose_name = 'Historial de Stock'
        verbose_name_plural = 'Historiales de Stock'
        ordering = ['-fecha']
        indexes = [
            models.Index(fields=['fecha']),
            models.Index(fields=['producto', 'bodega', 'fecha']),
        ]

    def __str__(self):
        bodega_nombre = self.bodega.nombre_bodega if self.bodega else "N/A"
        return f"Cambio stock: {self.producto.nombre_producto} ({self.cantidad_cambiada}) en {bodega_nombre}"