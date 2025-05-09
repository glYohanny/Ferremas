from django.db import models

class Carrito(models.Model):
    cliente = models.OneToOneField('usuarios_app.Cliente', on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carrito'
        verbose_name = 'Carrito de Compras'
        verbose_name_plural = 'Carritos de Compras'
        indexes = [
            models.Index(fields=['fecha_actualizacion']),
        ]

    def __str__(self):
        return f"Carrito de {self.cliente.nombre_completo}"

class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey('productos_app.Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'carrito_producto'
        unique_together = ('carrito', 'producto')
        verbose_name = 'Producto en Carrito'
        verbose_name_plural = 'Productos en Carrito'

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre_producto} en Carrito de {self.carrito.cliente.nombre_completo}"