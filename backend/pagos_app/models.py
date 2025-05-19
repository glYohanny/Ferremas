from django.db import models

class TarjetaCliente(models.Model):
    # NUNCA ALMACENAR CVV. Considerar tokenización para el número de tarjeta.
    numero_tarjeta_ultimos_digitos = models.CharField(max_length=4, verbose_name="Últimos 4 dígitos")
    marca_tarjeta = models.CharField(max_length=50, blank=True, null=True, verbose_name="Marca de tarjeta")
    fecha_expiracion = models.DateField()
    cliente = models.ForeignKey('usuarios_app.Cliente', on_delete=models.CASCADE)
    token_pasarela = models.CharField(max_length=255, blank=True, null=True, unique=True, verbose_name="Token de pasarela")

    class Meta:
        db_table = 'tarjeta_cliente'
        verbose_name = 'Tarjeta de Cliente (Referencia)'
        verbose_name_plural = 'Tarjetas de Clientes (Referencias)'

    def __str__(self):
        return f"Tarjeta terminada en {self.numero_tarjeta_ultimos_digitos} de {self.cliente.nombre_completo_display}"

class EstadoTransaccion(models.Model):
    nombre_estado = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'estado_transaccion'
        verbose_name = 'Estado de Transacción'
        verbose_name_plural = 'Estados de Transacciones'

    def __str__(self):
        return self.nombre_estado

class MetodoPago(models.Model):
    descripcion_pago = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'metodo_pago'
        verbose_name = 'Método de Pago'
        verbose_name_plural = 'Métodos de Pago'

    def __str__(self):
        return self.descripcion_pago

class TransaccionTarjetaCliente(models.Model):
    tarjeta_cliente_referencia = models.ForeignKey(TarjetaCliente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Referencia Tarjeta")
    id_transaccion_pasarela = models.CharField(max_length=255, unique=True, null=True, blank=True, verbose_name="ID Transacción Pasarela")
    cliente = models.ForeignKey('usuarios_app.Cliente', on_delete=models.PROTECT)
    monto_total = models.DecimalField(max_digits=10, decimal_places=0)
    estado = models.ForeignKey(EstadoTransaccion, on_delete=models.PROTECT)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.PROTECT)
    fecha_transaccion = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'transacciones_tarjeta_cliente'
        verbose_name = 'Transacción de Tarjeta Cliente'
        verbose_name_plural = 'Transacciones de Tarjeta Cliente'
        indexes = [
            models.Index(fields=['fecha_transaccion']),
            models.Index(fields=['cliente', 'fecha_transaccion']),
        ]

    def __str__(self):
        return f"Transacción {self.id_transaccion_pasarela or self.id} - {self.cliente.nombre_completo_display} - {self.monto_total}"

class RegistroContable(models.Model):
    transaccion_origen = models.ForeignKey(TransaccionTarjetaCliente, on_delete=models.SET_NULL, null=True, blank=True)
    # pedido_origen = models.ForeignKey('pedidos_app.Pedido', on_delete=models.SET_NULL, null=True, blank=True)
    descripcion = models.TextField()
    monto = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True) # Permitir null y blank
    # cuenta_contable_debito = models.CharField(max_length=100, blank=True, null=True)
    # cuenta_contable_credito = models.CharField(max_length=100, blank=True, null=True)
    fecha_contable = models.DateField(help_text="Fecha del asiento contable")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    registrado_por = models.ForeignKey('usuarios_app.Usuario', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Si el monto no se ha establecido y hay una transacción de origen,
        # tomar el monto de la transacción.
        if self.monto is None and self.transaccion_origen:
            self.monto = self.transaccion_origen.monto_total
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'registro_contable'
        verbose_name = 'Registro Contable'
        verbose_name_plural = 'Registros Contables'
        ordering = ['-fecha_contable', '-fecha_registro']
        indexes = [
            models.Index(fields=['fecha_contable']),
        ]

    def __str__(self):
        return f"Registro {self.pk} - {self.descripcion[:30]}... - {self.monto} ({self.fecha_contable})"