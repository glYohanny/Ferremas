from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from django.shortcuts import redirect # Para redirigir al frontend
from rest_framework.response import Response
from pagos_app.models import TarjetaCliente, EstadoTransaccion, MetodoPago, TransaccionTarjetaCliente, RegistroContable
from .serializers import (
    TarjetaClienteSerializer, EstadoTransaccionSerializer, MetodoPagoSerializer, 
    TransaccionTarjetaClienteSerializer, RegistroContableSerializer
)
from usuarios_app.models import Cliente # Import your Cliente model
from rest_framework.exceptions import ValidationError # For perform_create error handling

# Para Webpay
from integraciones_app.models import ApiConfig, ApiIntegrationLog
from pedidos_app.models import Pedido, EstadoPedido, DetallePedido # Asumiendo que tienes estos modelos
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes # Para credenciales genéricas
from transbank.common.integration_api_keys import IntegrationApiKeys # Para credenciales genéricas
from transbank.common.integration_type import IntegrationType # Para configurar el entorno
from transbank.common.options import WebpayOptions
import datetime
import traceback # Importar para imprimir tracebacks completos
from inventario_app.models import Inventario, HistorialStock # Para reponer stock
from sucursales_app.models import Bodega # Para identificar la bodega del pedido

from django.conf import settings # Para obtener la URL base del frontend
from django.db import transaction # Para transacciones atómicas

FRONTEND_URL_BASE = getattr(settings, 'FRONTEND_URL_BASE', 'http://localhost:5173') # URL de tu frontend

# ---------------------------
# TARJETAS Y TRANSACCIONES
# ---------------------------
class TarjetaClienteViewSet(viewsets.ModelViewSet):
    """ViewSet para que los clientes gestionen sus tarjetas (referencias)."""
    serializer_class = TarjetaClienteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Devuelve solo las tarjetas del usuario autenticado.
        """
        user = self.request.user
        if not user.is_authenticated:
            return TarjetaCliente.objects.none()
        try:
            cliente_profile = Cliente.objects.get(usuario=user) # Cambiado 'user' por 'usuario'
            return TarjetaCliente.objects.filter(cliente=cliente_profile)
        except Cliente.DoesNotExist:
            return TarjetaCliente.objects.none()
        except AttributeError: # Catch if Cliente.objects.get(user=user) fails due to model structure
            # Log this error appropriately in a real application
            return TarjetaCliente.objects.none()

    def perform_create(self, serializer):
        """Asocia la nueva tarjeta con el perfil de Cliente del usuario autenticado."""
        user = self.request.user
        try:
            cliente_profile = Cliente.objects.get(usuario=user) # Cambiado 'user' por 'usuario'
            serializer.save(cliente=cliente_profile)
        except Cliente.DoesNotExist:
            raise ValidationError("El usuario actual no tiene un perfil de cliente asociado.")

class EstadoTransaccionViewSet(viewsets.ModelViewSet):
    """ViewSet para visualizar los posibles estados de una transacción."""
    queryset = EstadoTransaccion.objects.all()
    serializer_class = EstadoTransaccionSerializer
    permission_classes = [permissions.IsAuthenticated] # Permitir a cualquier usuario autenticado listar estados

class MetodoPagoViewSet(viewsets.ModelViewSet):
    """ViewSet para visualizar los métodos de pago disponibles."""
    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Permitir lectura a autenticados, escritura a admins

class TransaccionTarjetaClienteViewSet(viewsets.ModelViewSet):
    """ViewSet para que los clientes vean sus transacciones de pago."""
    serializer_class = TransaccionTarjetaClienteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Este viewset solo debe devolver las transacciones del usuario autenticado.
        Asumimos que Cliente tiene un campo 'user' que es OneToOneField/ForeignKey a settings.AUTH_USER_MODEL.
       """
        user = self.request.user
        if not user.is_authenticated:
            return TransaccionTarjetaCliente.objects.none()
        try:
            cliente_profile = Cliente.objects.get(usuario=user) # Cambiado 'user' por 'usuario'
            return TransaccionTarjetaCliente.objects.filter(cliente=cliente_profile)
        except Cliente.DoesNotExist:
            return TransaccionTarjetaCliente.objects.none()
        except AttributeError:
            return TransaccionTarjetaCliente.objects.none()

    def perform_create(self, serializer):
        """Asocia la nueva transacción con el perfil de Cliente del usuario autenticado."""
        user = self.request.user
        try:
            cliente_profile = Cliente.objects.get(usuario=user) # Cambiado 'user' por 'usuario'
            serializer.save(cliente=cliente_profile)
        except Cliente.DoesNotExist:
            raise ValidationError("El usuario actual no tiene un perfil de cliente asociado.")



# ---------------------------
# REGISTROS CONTABLES
# ---------------------------
class RegistroContableViewSet(viewsets.ModelViewSet):
    """ViewSet para la gestión de registros contables (solo administradores)."""
    queryset = RegistroContable.objects.all()
    serializer_class = RegistroContableSerializer
    permission_classes = [permissions.IsAdminUser] # O personal de contabilidad

# ---------------------------
# INTEGRACIÓN WEBPAY
# ---------------------------

class WebpayCreateTransactionView(APIView):
    """Inicia una transacción de pago con Webpay Plus."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        log_entry = None # Inicializar log_entry a None
        start_time = datetime.datetime.now() # Inicializar start_time

        pedido_id = request.data.get('pedido_id')
        if not pedido_id:
            return Response({"error": "Se requiere pedido_id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # --- Sección 1: Obtener Pedido y Configuración ---
            try:
                pedido = Pedido.objects.get(id=pedido_id, cliente=request.user)
            except Pedido.DoesNotExist:
                return Response({"error": "Pedido no encontrado o no pertenece al usuario"}, status=status.HTTP_404_NOT_FOUND)

            webpay_api_config = ApiConfig.objects.get(nombre_api="Webpay Plus - Integración", activo=True)

            # --- Sección 2: Preparar datos para Webpay ---
            timestamp_seconds_part = str(int(datetime.datetime.now().timestamp()))[-7:]
            buy_order = f"FMS{pedido.id}T{timestamp_seconds_part}"
            session_id = request.session.session_key or f"sess_{buy_order}"

            if pedido.total is None:
                print(f"ALERTA WebpayCreate: El pedido {pedido.id} tiene un total NULO.")
                return Response({"error": f"El pedido {pedido.id} no tiene un total válido para procesar el pago."}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                amount = int(pedido.total)
            except (TypeError, ValueError) as e_amount:
                print(f"ERROR WebpayCreate: No se pudo convertir pedido.total ('{pedido.total}') a entero para el pedido {pedido.id}. Error: {e_amount}")
                return Response({"error": "Error al procesar el monto del pedido para Webpay."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            base_return_url = f"{request.scheme}://{request.get_host()}"
            return_url = f"{base_return_url}/api/pagos/webpay/retorno/"

            # --- Sección 3: Crear Log Entry y Llamar a Transbank ---
            log_entry = ApiIntegrationLog( # Ahora webpay_api_config está garantizado que existe
                api_config=webpay_api_config,
                endpoint=f"{webpay_api_config.endpoint_url}/rswebpaytransaction/api/webpay/v1.2/transactions",
                metodo_http="POST",
                request_data={"buy_order": buy_order, "session_id": session_id, "amount": amount, "return_url": return_url}
            )
            
            # Configurar el SDK de Transbank para usar las credenciales de prueba genéricas
            options = WebpayOptions(
                IntegrationCommerceCodes.WEBPAY_PLUS, 
                IntegrationApiKeys.WEBPAY,
                IntegrationType.TEST  # Asegura que se usa el entorno de prueba
            )
            tx = Transaction(options)
            response_tbk = tx.create(buy_order, session_id, amount, return_url)

            print(f"Webpay DEBUG - Respuesta de tx.create: {response_tbk}")

            webpay_token_value = response_tbk.get('token')
            webpay_url_value = response_tbk.get('url')

            if not webpay_token_value or not webpay_url_value:
                raise Exception("La respuesta de Transbank no contiene 'token' o 'url'. Respuesta recibida: " + str(response_tbk))

            log_entry.response_data = {"token": webpay_token_value, "url_redirect": webpay_url_value} # Corregido 'url' a 'url_redirect' para consistencia
            log_entry.codigo_estado = 200
            log_entry.success = True
            
            pedido.webpay_token = webpay_token_value
            pedido.save(update_fields=['webpay_token'])

            return Response({"token": webpay_token_value, "url_redirect": webpay_url_value}, status=status.HTTP_200_OK)

        except ApiConfig.DoesNotExist:
            # Este error es específico y debería manejarse antes de intentar usar webpay_api_config
            print("ERROR WebpayCreate: Configuración de Webpay no encontrada o inactiva.")
            # No podemos crear log_entry si webpay_api_config no existe.
            return Response({"error": "Configuración de Webpay no encontrada o inactiva"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(f"Error general en WebpayCreateTransactionView: {e}")
            traceback.print_exc() # <--- ESTO IMPRIMIRÁ EL TRACEBACK COMPLETO EN TU CONSOLA
            
            if log_entry: # Si log_entry fue inicializado (es decir, webpay_api_config se encontró)
                log_entry.error_message = str(e)
                log_entry.success = False
            # else: log_entry es None, no se puede guardar detalles del error en él.
            
            return Response({"error": "Error al iniciar el pago con Webpay", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            if log_entry: # Solo guardar si log_entry fue creado exitosamente
                end_time = datetime.datetime.now()
                log_entry.duracion_ms = int((end_time - start_time).total_seconds() * 1000)
                log_entry.save()

class WebpayCommitTransactionView(APIView):
    """Maneja el retorno de Webpay después de un intento de pago (commit o aborto)."""
    # Webpay redirige aquí. No requiere autenticación de sesión de Django
    # ya que la validación se hace con el token_ws.
    # Sin embargo, el frontend que llame a esta URL después de la redirección
    # podría necesitar estar autenticado para mostrar una página de confirmación personalizada.
    # Por ahora, la dejamos abierta, pero el frontend debe manejar la sesión del usuario.
    permission_classes = [permissions.AllowAny] 

    def _reponer_stock_pedido(self, pedido_obj: Pedido):
        """
        Repone el stock de los productos de un pedido al inventario.
        Se usa cuando un pago falla o es cancelado después de que el stock fue inicialmente descontado.
        """
        if not pedido_obj:
            print("Error Interno: No se proporcionó un objeto de pedido para reponer stock.")
            return

        print(f"INFO: Iniciando reposición de stock para pedido ID: {pedido_obj.id}")
        try:
            if not pedido_obj.sucursal:
                print(f"ALERTA CRÍTICA: Pedido {pedido_obj.id} no tiene sucursal asignada. No se puede determinar la bodega para reponer stock.")
                # Considerar lanzar una excepción aquí si esto no debería ocurrir.
                # raise Exception(f"Pedido {pedido_obj.id} sin sucursal, no se puede reponer stock.") # No relanzar para no detener el flujo principal
                return # Salir si no hay sucursal

            # Asumimos que el tipo de bodega es consistente con la creación del pedido.
            bodega_origen = Bodega.objects.get(sucursal=pedido_obj.sucursal, tipo_bodega='TIENDA') 

            with transaction.atomic(): # Transacción interna para la reposición de stock
                for detalle in pedido_obj.detalles.all(): # Usar el related_name 'detalles'
                    producto = detalle.producto
                    cantidad_a_reponer = detalle.cantidad
                    
                    inventario_item, created = Inventario.objects.select_for_update().get_or_create(
                        producto=producto,
                        bodega=bodega_origen,
                        defaults={'cantidad': 0} 
                    )
                    
                    inventario_item.cantidad += cantidad_a_reponer
                    inventario_item.save(update_fields=['cantidad'])
                    
                    HistorialStock.objects.create(
                        producto=producto,
                        bodega=bodega_origen,
                        cantidad_cambiada=cantidad_a_reponer, # Positivo para entrada/reposición
                        motivo=f"Reposición por pago fallido/cancelado - Pedido #{pedido_obj.id}"
                    )
                    print(f"INFO: Stock repuesto para {producto.nombre_producto}: +{cantidad_a_reponer} en {bodega_origen.nombre_bodega}")
            print(f"INFO: Reposición de stock (intento) completada para pedido ID: {pedido_obj.id}")
        except Bodega.DoesNotExist:
            print(f"ERROR CRÍTICO: No se encontró bodega de tipo 'TIENDA' para la sucursal {pedido_obj.sucursal.nombre_sucursal} durante la reposición del pedido {pedido_obj.id}.")
            # No relanzar la excepción para no detener el flujo principal
        except Exception as e_repo:
            print(f"ERROR CRÍTICO: Error durante la reposición de stock para el pedido {pedido_obj.id}: {e_repo}")
            traceback.print_exc()
            # No relanzar la excepción

    def _process_transaction_commit(self, token_ws_value, tbk_token_value, tbk_orden_compra_value, source_method="POST"):
        """
        Lógica centralizada para procesar el commit o el resultado de una transacción Webpay.
        source_method es para logging y distinguir si la llamada vino de GET o POST.
        """
        print(f"WebpayCommit _process_transaction_commit: Iniciando desde {source_method}. token_ws='{token_ws_value}', TBK_TOKEN='{tbk_token_value}', TBK_ORDEN_COMPRA='{tbk_orden_compra_value}'")

        # Default redirect URL in case of very early or unhandled errors
        frontend_redirect_url = f"{FRONTEND_URL_BASE}/pago/resultado?status=error_inesperado_en_commit&source={source_method}"

        if not token_ws_value and not tbk_token_value:
            # This specific check might need adjustment based on what GET can provide
            if source_method == "GET" and not token_ws_value: # For GET, we only expect token_ws
                frontend_redirect_url = f"{FRONTEND_URL_BASE}/pago/resultado?status=error_token_webpay_faltante_get"
            elif source_method == "POST" and not token_ws_value and not tbk_token_value:
                frontend_redirect_url = f"{FRONTEND_URL_BASE}/pago/resultado?status=error_token_webpay_faltante_post"
            else: # If it's GET and tbk_token_value is present, it's an invalid scenario for this logic path
                frontend_redirect_url = f"{FRONTEND_URL_BASE}/pago/resultado?status=error_parametros_invalidos_get"
            
            print(f"WebpayCommit _process_transaction_commit: Error de token faltante. Redirigiendo a: {frontend_redirect_url}")
            return redirect(frontend_redirect_url)

        try:
            webpay_api_config = ApiConfig.objects.get(nombre_api="Webpay Plus - Integración", activo=True)
        except ApiConfig.DoesNotExist:
            print("ERROR WebpayCommit: Configuración de Webpay no encontrada.")
            return redirect(f"{FRONTEND_URL_BASE}/pago/resultado?status=error_configuracion_servidor")

        log_entry = ApiIntegrationLog(
            api_config=webpay_api_config,
            endpoint=f"{webpay_api_config.endpoint_url}/rswebpaytransaction/api/webpay/v1.2/transactions/{token_ws_value or tbk_token_value}",
            metodo_http="PUT", # SDK usa PUT para commit
            request_data={"token_ws": token_ws_value, "TBK_TOKEN": tbk_token_value, "source_method": source_method}
        )
        start_time = datetime.datetime.now()

        try:
            options = WebpayOptions(
                IntegrationCommerceCodes.WEBPAY_PLUS, 
                IntegrationApiKeys.WEBPAY,
                IntegrationType.TEST
            )
            tx = Transaction(options)
            pedido = None
            response_tbk = None

            if token_ws_value: # Flujo normal con token_ws (puede venir de GET o POST)
                print(f"WebpayCommit _process_transaction_commit: Intentando tx.commit con token_ws: {token_ws_value}")
                response_tbk = tx.commit(token_ws_value)
                # response_tbk es un diccionario, así que lo asignamos directamente
                log_entry.response_data = response_tbk 
                print(f"Webpay DEBUG - Respuesta completa de tx.commit: {response_tbk}")
                log_entry.codigo_estado = 200
                
                pedido = Pedido.objects.filter(webpay_token=token_ws_value).first()
                if not pedido:
                    print(f"ALERTA: Pedido no encontrado para webpay_token: {token_ws_value}")

                # Verificar si el pago fue aprobado usando las claves del diccionario
                # Comúnmente, un pago aprobado tiene response_tbk.get('response_code') == 0
                # El print anterior de response_tbk te ayudará a confirmar las claves exactas.
                is_payment_approved = response_tbk.get('response_code') == 0

                if is_payment_approved:
                    log_entry.success = True
                    with transaction.atomic():
                        if pedido:
                            estado_pagado, _ = EstadoPedido.objects.get_or_create(nombre_estado="Pagado", defaults={'descripcion': 'El pago del pedido ha sido confirmado.'})
                            pedido.estado_pedido = estado_pagado
                            pedido.save(update_fields=['estado_pedido'])
                            # El stock ya fue descontado en la creación del pedido. No se hace nada más con el stock aquí.
                            try:
                                metodo_pago_webpay = MetodoPago.objects.get(descripcion_pago__icontains="Webpay")
                                estado_trans_aprobado = EstadoTransaccion.objects.get(nombre_estado="Aprobada") # Coincidir con el dato "Aprobada"
                                
                                # Obtener el perfil de Cliente asociado al Usuario del pedido
                                try:
                                    cliente_profile = Cliente.objects.get(usuario=pedido.cliente)
                                except Cliente.DoesNotExist:
                                    print(f"ALERTA CRÍTICA: No se encontró perfil de Cliente para el usuario {pedido.cliente.nombre_usuario} (ID: {pedido.cliente.id}) del pedido {pedido.id}")
                                    # Decide cómo manejar esto: ¿lanzar un error para que la transacción se revierta?
                                    # Por ahora, lanzaremos la excepción para que transaction.atomic() haga rollback.
                                    raise Exception(f"Perfil de Cliente no encontrado para el usuario del pedido {pedido.id}")

                                # Intentar encontrar la TarjetaCliente usada, si existe
                                tarjeta_usada = None
                                ultimos_digitos_webpay = response_tbk.get('card_detail', {}).get('card_number', 'XXXX')[-4:]
                                if ultimos_digitos_webpay != 'XXXX':
                                    try:
                                        # Busca la tarjeta por cliente y últimos dígitos.
                                        # Podrías añadir más criterios si es necesario (ej. marca_tarjeta si Webpay la devuelve)
                                        tarjeta_usada = TarjetaCliente.objects.filter(cliente=cliente_profile, numero_tarjeta_ultimos_digitos=ultimos_digitos_webpay).first()
                                    except TarjetaCliente.DoesNotExist:
                                        pass # No se encontró una tarjeta guardada, está bien.
                                TransaccionTarjetaCliente.objects.create(
                                    cliente=cliente_profile, # Usar el perfil de Cliente obtenido
                                    metodo_pago=metodo_pago_webpay,
                                    monto_total=pedido.total, # Asegúrate que pedido.total sea correcto
                                    estado=estado_trans_aprobado, # Campo 'estado' en el modelo
                                    id_transaccion_pasarela=response_tbk.get('buy_order'), 
                                    # Asegúrate que estos nombres de argumentos coincidan EXACTAMENTE
                                    # con los nombres de los campos en tu modelo TransaccionTarjetaCliente
                                    pedido=pedido,  # Asumiendo que el campo en el modelo se llama 'pedido'
                                    codigo_autorizacion_pasarela=response_tbk.get('authorization_code'), # Asumiendo 'codigo_autorizacion_pasarela'
                                    ultimos_digitos_tarjeta=ultimos_digitos_webpay if ultimos_digitos_webpay != 'XXXX' else None,  # Asumiendo 'ultimos_digitos_tarjeta'
                                    tarjeta_cliente_referencia=tarjeta_usada # Asociar la tarjeta si se encontró
                                )
                            except (MetodoPago.DoesNotExist, EstadoTransaccion.DoesNotExist, Cliente.DoesNotExist) as e_lookup: raise e_lookup # Re-lanzar errores de lookup
                            except Exception as e_trans: raise e_trans # Re-lanzar otras excepciones
                    frontend_redirect_url = f"{FRONTEND_URL_BASE}/pago/resultado?status=aprobado&pedido_id={pedido.id if pedido else 'error_pedido_no_encontrado_en_commit'}&tbk_token={token_ws_value}"
                else: # No aprobado
                    log_entry.success = False
                    if pedido:
                        try:
                            # Paso 1: Actualizar estado del pedido (en su propia transacción)
                            with transaction.atomic():
                                estado_pago_fallido, _ = EstadoPedido.objects.get_or_create(
                                    nombre_estado="Pago Fallido", 
                                    #defaults={'descripcion': 'El pago del pedido falló.'}
                                )
                                pedido.estado_pedido = estado_pago_fallido
                                pedido.save(update_fields=['estado_pedido'])
                            
                            # Paso 2: Intentar reponer stock (DESPUÉS de que el estado se guardó)
                            self._reponer_stock_pedido(pedido)
                        except Exception as e_state_update:
                            print(f"ERROR CRÍTICO al actualizar estado o llamar a reposición para pedido {pedido.id} (pago fallido): {e_state_update}")
                            traceback.print_exc()
                            # Asegurarse de que el estado del pedido refleje el fallo si la reposición falla catastróficamente antes de la redirección
                            pedido.estado_pedido = estado_pago_fallido
                            pedido.save(update_fields=['estado_pedido'])
                    frontend_redirect_url = f"{FRONTEND_URL_BASE}/pago/resultado?status=rechazado&pedido_id={pedido.id if pedido else 'error_pedido_no_encontrado_en_commit'}&tbk_token={token_ws_value}&response_code={response_tbk.get('response_code', 'N/A')}"
            
            elif tbk_token_value: # Transacción abortada por el usuario (solo debería venir de POST)
                if source_method == "GET":
                    print("ALERTA WebpayCommit: TBK_TOKEN recibido en una solicitud GET, esto es muy inesperado y no se procesará como commit.")
                    frontend_redirect_url = f"{FRONTEND_URL_BASE}/pago/resultado?status=error_tbk_token_en_get&tbk_token={tbk_token_value}"
                else: # Es POST con TBK_TOKEN
                    log_entry.success = False
                    log_entry.error_message = "Transacción abortada por el usuario en Webpay (TBK_TOKEN recibido)."
                    log_entry.response_data = {"TBK_TOKEN": tbk_token_value, "TBK_ORDEN_COMPRA": tbk_orden_compra_value}
                    
                    print(f"INFO (Aborto POST): Recibido TBK_TOKEN='{tbk_token_value}', TBK_ORDEN_COMPRA='{tbk_orden_compra_value}'")

                    pedido_abortado = None
                    pedido_id_str = 'desconocido_en_aborto'
                    
                    # Intento 1 (Preferido): Buscar por webpay_token (que debería ser el TBK_TOKEN)
                    if tbk_token_value:
                        try:
                            pedido_abortado = Pedido.objects.filter(webpay_token=tbk_token_value).first()
                            if pedido_abortado:
                                print(f"INFO (Aborto POST): Pedido {pedido_abortado.id} encontrado usando webpay_token='{tbk_token_value}'.")
                            else:
                                print(f"ALERTA (Aborto POST): No se encontró pedido usando webpay_token='{tbk_token_value}'.")
                        except Exception as e_token_lookup:
                            print(f"ERROR (Aborto POST): Excepción al buscar pedido por webpay_token='{tbk_token_value}': {e_token_lookup}")
                            pedido_abortado = None # Asegurar que es None si hay error

                    # Intento 2 (Fallback si el Intento 1 falló y tenemos TBK_ORDEN_COMPRA): Parsear desde TBK_ORDEN_COMPRA
                    # Esto es menos robusto y depende del formato de buy_order. Usar con precaución.
                    if not pedido_abortado and tbk_orden_compra_value:
                        print(f"INFO (Aborto POST): Fallback - Intentando encontrar pedido desde TBK_ORDEN_COMPRA='{tbk_orden_compra_value}'.")
                        try:
                            # Asumiendo formato "FMS<ID_PEDIDO>T<TIMESTAMP>"
                            if tbk_orden_compra_value.startswith("FMS") and "T" in tbk_orden_compra_value:
                                id_part = tbk_orden_compra_value[3:].split("T")[0]
                                pedido_id_from_buy_order = int(id_part)
                                temp_pedido = Pedido.objects.filter(id=pedido_id_from_buy_order).first()
                                if temp_pedido:
                                    # Verificación adicional: ¿Coincide el tbk_token_value (si existe) con el webpay_token del pedido encontrado?
                                    if tbk_token_value and temp_pedido.webpay_token == tbk_token_value:
                                        pedido_abortado = temp_pedido
                                        print(f"INFO (Aborto POST Fallback): Pedido {pedido_abortado.id} encontrado y verificado usando TBK_ORDEN_COMPRA y coincidencia de token.")
                                    elif not tbk_token_value: # Si no teníamos TBK_TOKEN, confiamos en el ID de la orden de compra
                                        pedido_abortado = temp_pedido
                                        print(f"INFO (Aborto POST Fallback): Pedido {pedido_abortado.id} encontrado usando TBK_ORDEN_COMPRA (sin TBK_TOKEN para verificar).")
                                    else:
                                        print(f"ALERTA (Aborto POST Fallback): Pedido {temp_pedido.id} encontrado por TBK_ORDEN_COMPRA, pero su webpay_token ('{temp_pedido.webpay_token}') NO COINCIDE con el TBK_TOKEN recibido ('{tbk_token_value}'). Descartando.")
                                else:
                                    print(f"ALERTA (Aborto POST Fallback): No se encontró pedido con ID {pedido_id_from_buy_order} parseado desde TBK_ORDEN_COMPRA.")
                            else:
                                print(f"ALERTA (Aborto POST Fallback): Formato de TBK_ORDEN_COMPRA ('{tbk_orden_compra_value}') no reconocido para parseo.")
                        except (ValueError, IndexError, TypeError) as e_parse:
                            print(f"ERROR (Aborto POST Fallback): Excepción al parsear pedido_id desde TBK_ORDEN_COMPRA '{tbk_orden_compra_value}': {e_parse}")
                            pedido_abortado = None # Asegurar que es None si hay error

                    # Procesar si se encontró el pedido_abortado por cualquiera de los métodos
                    if pedido_abortado:
                        pedido_id_str = str(pedido_abortado.id)
                        estado_actualizado_con_exito_aborto = False
                        try:
                            # Paso 1: Actualizar estado del pedido (en su propia transacción)
                            with transaction.atomic():
                                estado_cancelado, _ = EstadoPedido.objects.get_or_create(
                                    nombre_estado="Cancelado", 
                                    #defaults={'descripcion': 'Pedido cancelado por el usuario o sistema.'}
                                )
                                print(f"INFO (Aborto POST): Actualizando pedido {pedido_abortado.id} a ESTADO: {estado_cancelado.nombre_estado} (Cancelado por usuario)")
                                pedido_abortado.estado_pedido = estado_cancelado
                                pedido_abortado.save(update_fields=['estado_pedido'])
                                estado_actualizado_con_exito_aborto = True
                                print(f"INFO (Aborto POST): Pedido {pedido_abortado.id} actualizado exitosamente a ESTADO: {pedido_abortado.estado_pedido.nombre_estado}")
                        except Exception as e_state_update_abort:
                            print(f"ERROR CRÍTICO (Aborto POST): al actualizar estado del pedido {pedido_abortado.id} a 'Cancelado': {e_state_update_abort}")
                            traceback.print_exc()

                        if estado_actualizado_con_exito_aborto:
                            print(f"INFO (Aborto POST): Intentando reponer stock para pedido {pedido_abortado.id} después de marcar como Cancelado.")
                            self._reponer_stock_pedido(pedido_abortado)
                        else:
                            print(f"ALERTA (Aborto POST): No se intentará reponer stock para pedido {pedido_abortado.id} porque la actualización de estado a 'Cancelado' falló.")
                    else:
                        print(f"ALERTA CRÍTICA (Aborto POST): No se pudo identificar el pedido para TBK_TOKEN='{tbk_token_value}' y TBK_ORDEN_COMPRA='{tbk_orden_compra_value}'. No se puede procesar la cancelación/reposición.")
                        pedido_id_str = f"token_{tbk_token_value}_o_oc_{tbk_orden_compra_value}_no_encontrado"
                        
                    frontend_redirect_url = f"{FRONTEND_URL_BASE}/pago/resultado?status=abortado&pedido_id={pedido_id_str}&tbk_token={tbk_token_value}"
            
            # else: # No token_ws and no tbk_token (ya manejado al inicio del método)
            #    pass

        except Exception as e:
            log_entry.error_message = str(e)
            log_entry.success = False
            print(f"Error al procesar transacción Webpay ({source_method}): {e}")
            traceback.print_exc()
            frontend_redirect_url = f"{FRONTEND_URL_BASE}/pago/resultado?status=error_confirmacion&source={source_method}"
        finally:
            end_time = datetime.datetime.now()
            log_entry.duracion_ms = int((end_time - start_time).total_seconds() * 1000)
            log_entry.save()
        
        print(f"WebpayCommit _process_transaction_commit: Redirigiendo finalmente a: {frontend_redirect_url}")
        return redirect(frontend_redirect_url)

    def get(self, request, *args, **kwargs):
        token_ws_from_get = request.GET.get('token_ws')
        tbk_token_from_get = request.GET.get('TBK_TOKEN') # Aunque es raro para GET
        tbk_orden_compra_from_get = request.GET.get('TBK_ORDEN_COMPRA') # Aunque es raro para GET

        print(f"WebpayCommit DEBUG: Se recibió una solicitud GET para /api/pagos/webpay/retorno/. Datos GET: {request.GET}")

        if token_ws_from_get:
            print(f"ALERTA WebpayCommit: token_ws ('{token_ws_from_get}') recibido vía GET. Intentando procesar.")
            # Para GET, solo procesamos si hay token_ws. No esperamos TBK_TOKEN en GET para un flujo de aborto.
            return self._process_transaction_commit(
                token_ws_value=token_ws_from_get, 
                tbk_token_value=None, # Ignorar tbk_token si viene en GET con token_ws
                tbk_orden_compra_value=None, # Ignorar tbk_orden_compra si viene en GET con token_ws
                source_method="GET"
            )
        elif tbk_token_from_get: # Si solo llega TBK_TOKEN por GET (muy inusual, pero por cubrir)
            print(f"ALERTA WebpayCommit: TBK_TOKEN ('{tbk_token_from_get}') recibido vía GET sin token_ws. Tratando como aborto.")
            return self._process_transaction_commit(
                token_ws_value=None,
                tbk_token_value=tbk_token_from_get,
                tbk_orden_compra_value=tbk_orden_compra_from_get,
                source_method="GET_ABORT" # Un source_method diferente para este caso raro
            )
        else:
            print("WebpayCommit DEBUG: GET sin token_ws ni TBK_TOKEN. Redirigiendo con error_metodo_invalido.")
            error_redirect_url = f"{FRONTEND_URL_BASE}/pago/resultado?status=error_metodo_invalido_o_sin_token_en_get"
            return redirect(error_redirect_url)

    def post(self, request, *args, **kwargs):
        token_ws = request.data.get('token_ws') # Webpay Plus envía token_ws
        tbk_token = request.data.get('TBK_TOKEN') # Para transacciones abortadas por el usuario
        tbk_orden_compra = request.data.get('TBK_ORDEN_COMPRA') # Para transacciones abortadas

        # Log inicial de la solicitud de retorno
        print(f"Webpay Commit Recibido - token_ws: {token_ws}, TBK_TOKEN: {tbk_token}, TBK_ORDEN_COMPRA: {tbk_orden_compra}")
        
        # Llamar a la lógica de commit compartida.
        return self._process_transaction_commit(
            token_ws_value=token_ws,
            tbk_token_value=tbk_token,
            tbk_orden_compra_value=tbk_orden_compra,
            source_method="POST"
        )