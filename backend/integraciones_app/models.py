from django.db import models
from django.utils import timezone

class ApiIntegrationLog(models.Model):
    """
    Registro de llamadas a APIs externas.
    """
    api_config = models.ForeignKey(
        'ApiConfig',
        on_delete=models.SET_NULL, # O models.CASCADE si prefieres eliminar logs si se elimina la config
        null=True,
        blank=True,
        related_name='logs',
        help_text="Configuración de API utilizada para esta llamada"
    )
    endpoint = models.CharField(max_length=500, help_text="Endpoint específico llamado")
    metodo_http = models.CharField(max_length=10, help_text="Método HTTP (GET, POST, etc.)")
    fecha_hora_llamada = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora de la llamada")
    duracion_ms = models.IntegerField(null=True, blank=True, help_text="Duración de la llamada en milisegundos")
    codigo_estado = models.IntegerField(null=True, blank=True, help_text="Código de estado HTTP de la respuesta")
    request_data = models.JSONField(null=True, blank=True, help_text="Datos enviados en la solicitud (si aplica)")
    response_data = models.JSONField(null=True, blank=True, help_text="Datos recibidos en la respuesta")
    error_message = models.TextField(null=True, blank=True, help_text="Mensaje de error si la llamada falló")
    success = models.BooleanField(default=False, help_text="Indica si la llamada fue exitosa")

    class Meta:
        db_table = 'api_integration_log'
        verbose_name = 'Registro de Integración API'
        verbose_name_plural = 'Registros de Integraciones API'

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