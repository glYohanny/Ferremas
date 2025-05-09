from django.db import models

class TipoCambio(models.Model):
    moneda_origen = models.CharField(max_length=3)
    moneda_destino = models.CharField(max_length=3)
    tasa = models.DecimalField(max_digits=18, decimal_places=6)
    fecha_validez = models.DateField()
    fuente = models.CharField(max_length=100, default='No especificada')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tipo_cambio'
        verbose_name = 'Tipo de Cambio'
        verbose_name_plural = 'Tipos de Cambio'
        unique_together = ('moneda_origen', 'moneda_destino', 'fecha_validez', 'fuente')
        ordering = ['-fecha_validez', 'moneda_origen', 'moneda_destino']
        indexes = [
            models.Index(fields=['fecha_validez']),
            models.Index(fields=['moneda_origen', 'moneda_destino', 'fecha_validez']),
        ]

    def __str__(self):
        return f"{self.moneda_origen} a {self.moneda_destino}: {self.tasa} ({self.fecha_validez})"