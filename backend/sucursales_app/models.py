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
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

    class Meta:
        db_table = 'bodega'
        verbose_name = 'Bodega'
        verbose_name_plural = 'Bodegas'
        unique_together = ('nombre_bodega', 'sucursal')

    def __str__(self):
        return f"{self.nombre_bodega} ({self.sucursal.nombre_sucursal})"