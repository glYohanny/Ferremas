from django.db import models

class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=100, unique=True)
    # slug = models.SlugField(unique=True, blank=True, help_text="Versión amigable para URL de la categoría")

    class Meta:
        db_table = 'categorias'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.nombre_categoria)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre_categoria

class Producto(models.Model):
    nombre_producto = models.CharField(max_length=100)
    # slug = models.SlugField(unique=True, blank=True, help_text="Versión amigable para URL del producto")
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    marca = models.CharField(max_length=50, blank=True, null=True)
    codigo_producto = models.CharField(max_length=50, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, null=True, blank=True)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True, verbose_name="Imagen del producto")

    class Meta:
        db_table = 'productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        indexes = [
            models.Index(fields=['nombre_producto']),
            models.Index(fields=['marca']),
            models.Index(fields=['codigo_producto']),
            # models.Index(fields=['slug']),
        ]

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(f"{self.nombre_producto}-{self.codigo_producto}")
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre_producto} ({self.codigo_producto})"