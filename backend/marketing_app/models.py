from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Define las promociones aplicables a productos o compras.
class Promocion(models.Model):
    TIPO_DESCUENTO_CHOICES = [
        ('PORCENTAJE', '%'),
        ('MONTO_FIJO', '$'),
    ]
    TIPO_APLICACION_CHOICES = [
        ('PRODUCTO_ESPECIFICO', 'Producto Específico'), # Aplicable a productos individuales listados en PromocionCondicion
        ('CATEGORIA', 'Categoría Completa'),       # Aplicable a todos los productos de categorías listadas en PromocionCondicion
        ('MARCA', 'Marca Completa'),             # Aplicable a todos los productos de marcas listadas en PromocionCondicion
        ('CARRITO', 'Total del Carrito'),        # Aplicable al monto total del carrito (condiciones en PromocionRestriccion)
    ]

    nombre = models.CharField(max_length=255, help_text="Nombre descriptivo de la promoción", default="Promoción sin nombre")
    descripcion = models.TextField()
    tipo_descuento = models.CharField(max_length=20, choices=TIPO_DESCUENTO_CHOICES, default='PORCENTAJE')
    valor_descuento = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valor del descuento (porcentaje o monto fijo)", default=0.00)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    activo = models.BooleanField(default=True, help_text="Booleano para activar/desactivar la promoción")
    prioridad = models.IntegerField(default=0, help_text="Orden de aplicación si hay múltiples promociones aplicables (menor número = mayor prioridad)")
    tipo_aplicacion = models.CharField(max_length=30, choices=TIPO_APLICACION_CHOICES, default='PRODUCTO_ESPECIFICO')
    
    # Campo 'cantidad_minima_productos' movido a PromocionCondicion o PromocionRestriccion si es más específico.
    # Por ahora, lo comentamos aquí ya que su aplicabilidad depende del contexto.
    # cantidad_minima_productos_en_condicion = models.PositiveIntegerField(default=1, help_text="Cantidad mínima de un producto/categoría/marca en condición para aplicar la promo")

    # codigo_promocion = models.CharField(max_length=50, unique=True, blank=True, null=True, help_text="Código de cupón opcional")

    class Meta:
        db_table = 'promocion'
        verbose_name = 'Promoción'
        verbose_name_plural = 'Promociones'
        ordering = ['prioridad', '-fecha_inicio']
        indexes = [
            models.Index(fields=['fecha_inicio', 'fecha_fin']),
            models.Index(fields=['activo', 'fecha_inicio', 'fecha_fin']),
            models.Index(fields=['tipo_aplicacion']),
        ]

    def __str__(self):
        return self.nombre

    def clean(self):
        super().clean()
        if self.fecha_inicio >= self.fecha_fin:
            raise ValidationError(_("La fecha de inicio debe ser anterior a la fecha de fin."))
        if self.tipo_descuento == 'PORCENTAJE' and (self.valor_descuento <= 0 or self.valor_descuento > 100):
            raise ValidationError(_("El porcentaje de descuento debe estar entre 0.01 y 100."))
        if self.tipo_descuento == 'MONTO_FIJO' and self.valor_descuento <= 0:
            raise ValidationError(_("El monto fijo de descuento debe ser un valor positivo."))

# Vincula un producto específico a una promoción.
class ProductoPromocion(models.Model):
    producto = models.ForeignKey('productos_app.Producto', on_delete=models.CASCADE)
    promocion = models.ForeignKey(Promocion, on_delete=models.CASCADE)
    # precio_con_descuento_fijo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Si el descuento es un precio fijo en lugar de porcentaje")

    class Meta:
        db_table = 'producto_promocion'
        unique_together = ('producto', 'promocion')
        verbose_name = 'Producto en Promoción'
        verbose_name_plural = 'Productos en Promoción'

    def __str__(self):
        return f"{self.producto.nombre_producto} en promoción ({self.promocion.descripcion[:20]}...)"


# Tabla de condiciones para aplicar una promoción
class PromocionCondicion(models.Model):
    TIPO_OBJETIVO_CHOICES = [
        ('PRODUCTO', 'Producto Específico'),
        ('CATEGORIA', 'Categoría de Productos'),
        ('MARCA', 'Marca de Productos'),
    ]
    promocion = models.ForeignKey(Promocion, related_name='condiciones', on_delete=models.CASCADE)
    tipo_objetivo = models.CharField(max_length=20, choices=TIPO_OBJETIVO_CHOICES)
    
    # Usamos FKs separadas y permitimos null. La lógica de validación asegurará que solo uno esté lleno.
    producto_objetivo = models.ForeignKey('productos_app.Producto', on_delete=models.CASCADE, null=True, blank=True, help_text="Producto específico al que aplica la condición.")
    categoria_objetivo = models.ForeignKey('productos_app.Categoria', on_delete=models.CASCADE, null=True, blank=True, help_text="Categoría de productos a la que aplica la condición.") # Asume que tienes Categoria en productos_app
    marca_objetivo = models.ForeignKey('productos_app.Marca', on_delete=models.CASCADE, null=True, blank=True, help_text="Marca de productos a la que aplica la condición.") # Asume que tienes Marca en productos_app

    cantidad_minima_aplicable = models.PositiveIntegerField(default=1, help_text="Cantidad mínima del objetivo (producto/categoría/marca) para que esta condición se cumpla.")

    class Meta:
        db_table = 'promocion_condicion'
        verbose_name = 'Condición de Promoción'
        verbose_name_plural = 'Condiciones de Promoción'
        # unique_together = [['promocion', 'tipo_objetivo', 'producto_objetivo', 'categoria_objetivo', 'marca_objetivo']] # Puede ser muy restrictivo

    def __str__(self):
        if self.tipo_objetivo == 'PRODUCTO' and self.producto_objetivo:
            return f"Condición para {self.promocion.nombre}: Producto {self.producto_objetivo.nombre_producto}"
        elif self.tipo_objetivo == 'CATEGORIA' and self.categoria_objetivo:
            return f"Condición para {self.promocion.nombre}: Categoría {self.categoria_objetivo.nombre}"
        elif self.tipo_objetivo == 'MARCA' and self.marca_objetivo:
            return f"Condición para {self.promocion.nombre}: Marca {self.marca_objetivo.nombre}"
        return f"Condición para {self.promocion.nombre} ({self.tipo_objetivo})"

    def clean(self):
        super().clean()
        objetivos_definidos = sum([
            1 if self.producto_objetivo else 0,
            1 if self.categoria_objetivo else 0,
            1 if self.marca_objetivo else 0
        ])
        if objetivos_definidos == 0 and self.promocion.tipo_aplicacion != 'CARRITO':
            raise ValidationError(_("Debe especificar un objetivo (producto, categoría o marca) para este tipo de condición."))
        if objetivos_definidos > 1:
            raise ValidationError(_("Solo puede especificar un tipo de objetivo (producto, categoría o marca) por condición."))
        
        if self.tipo_objetivo == 'PRODUCTO' and not self.producto_objetivo:
            raise ValidationError({'producto_objetivo': _("Debe seleccionar un producto para el tipo de objetivo 'Producto'.")})
        if self.tipo_objetivo == 'CATEGORIA' and not self.categoria_objetivo:
            raise ValidationError({'categoria_objetivo': _("Debe seleccionar una categoría para el tipo de objetivo 'Categoría'.")})
        if self.tipo_objetivo == 'MARCA' and not self.marca_objetivo:
            raise ValidationError({'marca_objetivo': _("Debe seleccionar una marca para el tipo de objetivo 'Marca'.")})

        if self.promocion.tipo_aplicacion == 'CARRITO' and objetivos_definidos > 0:
            raise ValidationError(_("Las promociones de tipo 'CARRITO' no deben tener condiciones de producto, categoría o marca específicas."))

# Representa una notificación genérica que puede ser enviada.
class Notificacion(models.Model):
    # TIPO_NOTIFICACION_CHOICES = [ ('PEDIDO', 'Pedido'), ('STOCK', 'Stock'), ('PROMOCION', 'Promoción'), ('GENERAL', 'General'), ]
    # tipo_notificacion = models.CharField(max_length=20, choices=TIPO_NOTIFICACION_CHOICES, default='GENERAL')
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    # url_destino = models.URLField(blank=True, null=True, help_text="URL a la que redirigir al hacer clic")

    class Meta:
        db_table = 'notificacion'
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-fecha_envio']
        indexes = [
            models.Index(fields=['fecha_envio']),
        ]

    def __str__(self):
        return self.titulo

# Registra si un cliente específico ha leído una notificación.
class ClienteNotificacion(models.Model):
    cliente = models.ForeignKey('usuarios_app.Cliente', on_delete=models.CASCADE)
    notificacion = models.ForeignKey(Notificacion, on_delete=models.CASCADE)
    leido = models.BooleanField(default=False)
    fecha_lectura = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'cliente_notificacion'
        unique_together = ('cliente', 'notificacion')
        verbose_name = 'Notificación de Cliente'
        verbose_name_plural = 'Notificaciones de Clientes'

    def save(self, *args, **kwargs):
        if self.leido and not self.fecha_lectura:
            self.fecha_lectura = timezone.now()
        elif not self.leido:
            self.fecha_lectura = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Notif: '{self.notificacion.titulo[:20]}' para {self.cliente.nombre_completo} (Leído: {self.leido})"


# Tabla de restricciones adicionales para una promoción
class PromocionRestriccion(models.Model):
    TIPO_RESTRICCION_CHOICES = [
        ('MONTO_MINIMO_COMPRA', 'Monto Mínimo de Compra Total'),
        ('MAX_USOS_POR_CLIENTE', 'Máximo de Usos por Cliente'),
        ('MAX_USOS_TOTALES', 'Máximo de Usos Totales de la Promoción'),
        # ('METODOS_PAGO_VALIDOS', 'Métodos de Pago Válidos'), # Requeriría un modelo MetodoPago o lista de strings
        # ('CLIENTES_ESPECIFICOS', 'Clientes Específicos'), # Requeriría ManyToMany a Cliente
    ]
    promocion = models.ForeignKey(Promocion, related_name='restricciones', on_delete=models.CASCADE)
    tipo_restriccion = models.CharField(max_length=30, choices=TIPO_RESTRICCION_CHOICES)
    
    valor_monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Valor para MONTO_MINIMO_COMPRA.")
    valor_entero = models.PositiveIntegerField(null=True, blank=True, help_text="Valor para MAX_USOS.")
    # valor_texto = models.TextField(null=True, blank=True, help_text="Valor para METODOS_PAGO_VALIDOS (ej: 'WEBPAY,TRANSFERENCIA')")

    class Meta:
        db_table = 'promocion_restriccion'
        verbose_name = 'Restricción de Promoción'
        verbose_name_plural = 'Restricciones de Promoción'
        unique_together = [['promocion', 'tipo_restriccion']] # Generalmente una promo tiene un solo tipo de restricción de este estilo

    def __str__(self):
        return f"Restricción para {self.promocion.nombre}: {self.get_tipo_restriccion_display()}"

    def clean(self):
        super().clean()
        if self.tipo_restriccion == 'MONTO_MINIMO_COMPRA' and self.valor_monto is None:
            raise ValidationError({'valor_monto': _("Debe especificar un valor para el monto mínimo de compra.")})
        if self.tipo_restriccion in ['MAX_USOS_POR_CLIENTE', 'MAX_USOS_TOTALES'] and self.valor_entero is None:
            raise ValidationError({'valor_entero': _("Debe especificar un valor para el máximo de usos.")})
        # Añadir más validaciones si se agregan más tipos de valor_