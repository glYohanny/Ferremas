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

class ConversionDivisa(models.Model):
    """
    Registra una conversión de divisa realizada.
    """
    monto_origen = models.DecimalField(max_digits=18, decimal_places=2)
    moneda_origen = models.CharField(max_length=3, help_text="Código ISO de la moneda de origen (ej. USD, CLP)")
    monto_destino = models.DecimalField(max_digits=18, decimal_places=2)
    moneda_destino = models.CharField(max_length=3, help_text="Código ISO de la moneda de destino (ej. USD, CLP)")
    tipo_cambio_aplicado = models.ForeignKey(
        TipoCambio,
        on_delete=models.SET_NULL, # Si se elimina el tipo de cambio, la conversión permanece pero sin la referencia directa
        null=True,
        blank=True,
        help_text="Tipo de cambio utilizado para esta conversión, si aplica."
    )
    tasa_conversion_manual = models.DecimalField(
        max_digits=18, decimal_places=6, null=True, blank=True,
        help_text="Tasa de conversión utilizada si no se usó un TipoCambio predefinido."
    )
    fecha_conversion = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora en que se registró la conversión.")
    descripcion = models.TextField(blank=True, null=True, help_text="Descripción o nota adicional sobre la conversión.")

    class Meta:
        db_table = 'conversion_divisa'
        verbose_name = 'Conversión de Divisa'
        verbose_name_plural = 'Conversiones de Divisas'
        ordering = ['-fecha_conversion']
        indexes = [
            models.Index(fields=['fecha_conversion']),
            models.Index(fields=['moneda_origen', 'moneda_destino']),
        ]

    def __str__(self):
        return f"Conversión: {self.monto_origen} {self.moneda_origen} a {self.monto_destino} {self.moneda_destino} ({self.fecha_conversion.strftime('%Y-%m-%d')})"