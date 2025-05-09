from django.db import models

class Region(models.Model):
    nombre_region = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'region'
        verbose_name = 'Región'
        verbose_name_plural = 'Regiones'

    def __str__(self):
        return self.nombre_region

class Comuna(models.Model):
    nombre_comuna = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta:
        db_table = 'comuna'
        verbose_name = 'Comuna'
        verbose_name_plural = 'Comunas'
        unique_together = ('nombre_comuna', 'region')

    def __str__(self):
        return f"{self.nombre_comuna} ({self.region.nombre_region})"