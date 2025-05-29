from rest_framework import viewsets, permissions, views, response, status
from integraciones_app.models import ApiIntegrationLog, ApiConfig
from .serializers import ApiIntegrationLogSerializer, ApiConfigSerializer
import requests # Necesitarás instalar requests: pip install requests
from django.utils import timezone
# import json # No se usa directamente, response.json() de requests es suficiente
from finanzas_app.models import TipoCambio # Importar el modelo TipoCambio


# ---------------------------
# INTEGRACIONES Y CONFIG API
# ---------------------------
class ApiIntegrationLogViewSet(viewsets.ModelViewSet):
    queryset = ApiIntegrationLog.objects.all()
    serializer_class = ApiIntegrationLogSerializer
    permission_classes = [permissions.IsAdminUser]

class ApiConfigViewSet(viewsets.ModelViewSet):
    queryset = ApiConfig.objects.all()
    serializer_class = ApiConfigSerializer
    permission_classes = [permissions.IsAdminUser]

# ---------------------------
# VISTA PARA INDICADORES ECONÓMICOS (MINDICADOR.CL)
# ---------------------------
class IndicadoresEconomicosView(views.APIView):
    """
    Vista para obtener indicadores económicos desde mindicador.cl.
    El backend actúa como proxy para evitar llamadas directas desde el frontend
    y para poder registrar las interacciones.
    """
    permission_classes = [permissions.AllowAny] # O ajusta los permisos según necesites

    def get(self, request, *args, **kwargs):
        api_config = None
        try:
            # Intenta obtener o crear una configuración para mindicador.cl para el logging
            api_config, created = ApiConfig.objects.get_or_create(
                nombre_api="mindicador.cl",
                defaults={
                    'endpoint_url': 'https://mindicador.cl/api',
                    'metodo_http': 'GET',
                    'activo': True,
                    'descripcion': 'API pública para indicadores económicos chilenos (dólar, UF, etc.).'
                }
            )
        except Exception as e:
            # Loggear error al obtener/crear config, pero continuar si es posible
            print(f"Advertencia: Error al obtener/crear ApiConfig para mindicador.cl: {e}")


        start_time = timezone.now()
        log_entry_data = {
            "api_config": api_config,
            "endpoint": "https://mindicador.cl/api",
            "metodo_http": "GET",
            "request_data": None,
        }

        try:
            mindicador_response = requests.get('https://mindicador.cl/api', timeout=10)
            mindicador_response.raise_for_status()
            
            data = mindicador_response.json()

            # --- INICIO: Actualizar/Crear registros en TipoCambio ---
            if data: # Solo si obtuvimos datos de mindicador
                monedas_a_actualizar = {
                    'USD': data.get('dolar'),
                    'EUR': data.get('euro')
                    # Puedes añadir más si mindicador los provee y te interesan (ej. 'utm', 'uf')
                }

                for codigo_moneda, info_moneda in monedas_a_actualizar.items():
                    if info_moneda and info_moneda.get('valor'):
                        try:
                            fecha_validez_str = info_moneda.get('fecha')
                            fecha_validez_dt = None
                            if fecha_validez_str:
                                try:
                                    fecha_validez_dt = timezone.datetime.fromisoformat(fecha_validez_str.replace('Z', '+00:00')).date()
                                except ValueError:
                                    print(f"Advertencia: No se pudo parsear la fecha '{fecha_validez_str}' para {codigo_moneda} desde mindicador. Usando fecha actual.")
                                    fecha_validez_dt = timezone.now().date()
                            else:
                                fecha_validez_dt = timezone.now().date()

                            obj, created = TipoCambio.objects.update_or_create(
                                moneda_origen='CLP', # Moneda base de tus precios
                                moneda_destino=codigo_moneda,
                                fecha_validez=fecha_validez_dt, # Usar la fecha parseada o la actual
                                fuente='mindicador.cl', # Para saber de dónde vino la tasa
                                defaults={'tasa': info_moneda['valor']}
                            )
                            print(f"Tipo de cambio CLP a {codigo_moneda} {'creado' if created else 'actualizado'}: {obj.tasa} (Válido hasta: {obj.fecha_validez})")
                        except Exception as e:
                            print(f"Error al actualizar/crear TipoCambio para {codigo_moneda}: {e}")
            # --- FIN: Actualizar/Crear registros en TipoCambio ---

            end_time = timezone.now()
            log_entry_data.update({
                "duracion_ms": int((end_time - start_time).total_seconds() * 1000),
                "codigo_estado": mindicador_response.status_code,
                "response_data": data,
                "success": True,
            })
            ApiIntegrationLog.objects.create(**log_entry_data)
            
            return response.Response(data, status=status.HTTP_200_OK)

        except requests.exceptions.HTTPError as http_err:
            error_message = f"Error HTTP al conectar con mindicador.cl: {http_err}"
            status_code_error = http_err.response.status_code if http_err.response else status.HTTP_500_INTERNAL_SERVER_ERROR
            response_text = http_err.response.text if http_err.response else None
        except requests.exceptions.ConnectionError as conn_err:
            error_message = f"Error de conexión con mindicador.cl: {conn_err}"
            status_code_error = status.HTTP_503_SERVICE_UNAVAILABLE
            response_text = None
        except requests.exceptions.Timeout as timeout_err:
            error_message = f"Timeout al conectar con mindicador.cl: {timeout_err}"
            status_code_error = status.HTTP_504_GATEWAY_TIMEOUT
            response_text = None
        except requests.exceptions.RequestException as req_err: # Captura genérica para otros errores de requests
            error_message = f"Error en la solicitud a mindicador.cl: {req_err}"
            status_code_error = status.HTTP_500_INTERNAL_SERVER_ERROR
            response_text = None
        except ValueError as json_err: # Si response.json() falla
            error_message = f"Error al parsear JSON de mindicador.cl: {json_err}"
            status_code_error = status.HTTP_500_INTERNAL_SERVER_ERROR
            response_text = "Respuesta no válida de la API externa."

        end_time = timezone.now()
        log_entry_data.update({
            "duracion_ms": int((end_time - start_time).total_seconds() * 1000),
            "codigo_estado": status_code_error,
            "response_data": {"error_detail": response_text} if response_text else None,
            "error_message": error_message,
            "success": False,
        })
        ApiIntegrationLog.objects.create(**log_entry_data)
        
        return response.Response({"error": error_message, "detail": response_text}, status=status_code_error)
    