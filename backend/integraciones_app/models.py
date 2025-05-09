from django.db import models
from django.utils import timezone

class ApiConfig(models.Model):
    nombre_api = models.CharField(max_length=100, unique=True)
    endpoint_url = models.URLField(max_length=500)
    metodo_http = models.CharField(max_length=10, default='GET', help_text="GET, POST, PUT, DELETE, etc.")
    headers_json = models.JSONField(blank=True, null=True, help_text="Cabeceras HTTP como objeto JSON")
    autenticacion_tipo = models.CharField(max_length=50, blank=True, null=True, help_text="Ej: Bearer, Basic, API_KEY")
    autenticacion_credenciales_json = models.JSONField(blank=True, null=True, help_text="Credenciales de autenticación (manejar con cuidado)")
    tipo_api = models.CharField(max_length=50, blank=True, null=True, help_text="Ej: REST, SOAP, GraphQL")
    descripcion = models.TextField(null=True, blank=True)
    activo = models.BooleanField(default=True, help_text="Indica si la configuración de API está activa")
    fecha_registro = models.DateTimeField(default=timezone.now, editable=False, help_text="Fecha de creación del registro")

    class Meta:
        db_table = 'api_config'
        verbose_name = 'Configuración de API Externa'
        verbose_name_plural = 'Configuraciones de APIs Externas'
        indexes = [
            models.Index(fields=['fecha_registro']),
            models.Index(fields=['activo', 'tipo_api']),
        ]

    def __str__(self):
        return self.nombre_api