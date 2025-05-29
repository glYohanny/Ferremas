from django.db import models

class Sucursal(models.Model):
    nombre_sucursal = models.CharField(max_length=100, unique=True)
    direccion = models.TextField()
    comuna = models.ForeignKey('geografia_app.Comuna', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'sucursal'
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'

    def __str__(self):
        return self.nombre_sucursal

class Bodega(models.Model):
    nombre_bodega = models.CharField(max_length=100)
    sucursal = models.ForeignKey(Sucursal, related_name='bodegas', on_delete=models.CASCADE)
    direccion = models.TextField(blank=True, null=True, help_text="Dirección específica de la bodega, si es diferente a la sucursal.")

    # --- NUEVO CAMPO PARA TIPO DE BODEGA ---
    TIPO_BODEGA_TIENDA = 'TIENDA'
    TIPO_BODEGA_ALMACEN = 'ALMACEN'
    # Podrías añadir más tipos si los necesitas, ej: 'TRANSITO', 'DEFECTUOSO'
    
    TIPO_BODEGA_CHOICES = [
        (TIPO_BODEGA_TIENDA, 'Bodega de Tienda / Punto de Venta'),
        (TIPO_BODEGA_ALMACEN, 'Bodega de Almacén Principal'),
    ]

    tipo_bodega = models.CharField(
        max_length=15, 
        choices=TIPO_BODEGA_CHOICES,
        default=TIPO_BODEGA_ALMACEN, 
        help_text="Define si esta ubicación es para venta directa al cliente o almacenamiento."
    )
    # --- FIN NUEVO CAMPO ---

    class Meta:
        db_table = 'bodega'
        verbose_name = 'Bodega'
        verbose_name_plural = 'Bodegas'
        unique_together = ('nombre_bodega', 'sucursal')
    def __str__(self):
        return f"{self.nombre_bodega} ({self.get_tipo_bodega_display()}) - {self.sucursal.nombre_sucursal}"