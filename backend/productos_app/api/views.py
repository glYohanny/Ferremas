from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.generics import ListAPIView # Importar ListAPIView
from productos_app.models import Categoria as Category, Producto as Product, Marca # Usar Product directamente
# from inventario_app.models import Inventario # Ya no es necesario importar Inventario aquí para esta vista
# from inventario_app.api.serializers import InventarioSerializer # Ya no se usa directamente en esta vista
from .serializers import CategoriaSerializer, ProductoSerializer, MarcaSerializer # Usaremos ProductoSerializer
from django.db.models import Sum, F, ExpressionWrapper, DecimalField

# --- IMPORTANTE: Ajusta estas importaciones a tus modelos reales ---
# Asumimos que tienes estos modelos en una app llamada 'pedidos_app' y 'sucursales_app'
# Si se llaman diferente o están en otra app, debes cambiarlo.
try:
    from pedidos_app.models import DetallePedido, Pedido, EstadoPedido
    from sucursales_app.models import Sucursal # Necesario para el nombre de la sucursal
    PEDIDOS_APP_AVAILABLE = True
except ImportError:
    PEDIDOS_APP_AVAILABLE = False
    # En un entorno de producción, podrías querer loggear este warning
    print("ADVERTENCIA: No se pudieron importar modelos de Pedido/DetallePedido/Sucursal. El informe de ventas no funcionará.")

class ProductoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    # queryset = Product.objects.all() # Comentamos o eliminamos la definición a nivel de clase
    serializer_class = ProductoSerializer
    # Considera ajustar los permisos. AllowAny podría no ser adecuado para toda la info de producto.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Ejemplo: lectura para todos, escritura para autenticados

    def get_queryset(self):
        """
        Obtiene el queryset base y opcionalmente lo filtra.
        """
        # Siempre obtenemos el queryset base directamente de la base de datos aquí
        queryset = Product.objects.all()

        # Mantenemos tu lógica de filtrado opcional (si la necesitas)
        # Si no estás usando el filtro 'owner_username', puedes incluso simplificar más
        # y solo retornar Product.objects.all()
        owner_username = self.request.query_params.get('owner_username', None)
        if owner_username is not None:
            # This assumes your Product model has an 'owner' field (ForeignKey to your User model)
            # and your User model's USERNAME_FIELD is 'nombre_usuario'.
            queryset = queryset.filter(owner__nombre_usuario=owner_username)
        return queryset

    @action(detail=True, methods=['get'], url_path='informe-ventas', permission_classes=[permissions.IsAdminUser]) # Ejemplo de permiso más restrictivo
    def informe_ventas(self, request, pk=None):
        if not PEDIDOS_APP_AVAILABLE:
            return Response(
                {"error": "La funcionalidad de informe de ventas no está disponible debido a la falta de modelos de pedidos o sucursales."},
                status=503 # Service Unavailable
            )

        product = self.get_object() # Obtiene la instancia del producto (pk es el ID del producto)

        try:
            # --- ¡¡¡IMPORTANTE: Asegúrate que 'Pagado' o 'Completado' sea el nombre exacto de tu estado de pedido!!! ---
            estado_pedido_valido_para_venta = EstadoPedido.objects.get(nombre_estado="Pagado") # O "Completado", etc.
        except EstadoPedido.DoesNotExist:
            return Response({"error": "El estado de pedido para ventas ('Pagado' o 'Completado') no está configurado en el sistema."}, status=500)

        # Filtrar detalles de pedidos para este producto y pedidos en estado válido
        detalles_vendidos = DetallePedido.objects.filter(
            producto=product,
            pedido__estado_pedido=estado_pedido_valido_para_venta
        )

        # 1. Totales Generales
        agregados_totales = detalles_vendidos.aggregate(
            total_unidades=Sum('cantidad'),
            total_ingresos=Sum(ExpressionWrapper(F('cantidad') * F('precio_unitario'), output_field=DecimalField()))
        )
        total_unidades_vendidas = agregados_totales['total_unidades'] or 0
        total_ingresos_generados = agregados_totales['total_ingresos'] or 0.00

        # 2. Desglose por Sucursal
        # --- ¡¡¡CRÍTICO!!! Esto asume que tu modelo 'Pedido' tiene un campo ForeignKey 'sucursal' ---
        # Si 'Pedido' no tiene un campo 'sucursal', este desglose no funcionará directamente.
        # Necesitarías añadir 'sucursal = models.ForeignKey(Sucursal, ...)' a tu modelo Pedido.
        ventas_por_sucursal_qs = detalles_vendidos.values(
            'pedido__sucursal__id',  # Asume Pedido.sucursal.id
            'pedido__sucursal__nombre_sucursal'  # Asume Pedido.sucursal.nombre_sucursal
        ).annotate(
            unidades_vendidas_sucursal=Sum('cantidad'),
            ingresos_generados_sucursal=Sum(ExpressionWrapper(F('cantidad') * F('precio_unitario'), output_field=DecimalField()))
        ).order_by('pedido__sucursal__nombre_sucursal')

        desglose_sucursales = []
        for item in ventas_por_sucursal_qs:
            if item['pedido__sucursal__id'] is not None: # Solo incluir si hay sucursal asociada
                desglose_sucursales.append({
                    "sucursal_id": item['pedido__sucursal__id'],
                    "nombre_sucursal": item['pedido__sucursal__nombre_sucursal'],
                    "unidades_vendidas": item['unidades_vendidas_sucursal'],
                    "ingresos_generados": item['ingresos_generados_sucursal'] or 0.00
                })
        
        informe = {
            "producto_id": product.id,
            "nombre_producto": product.nombre_producto,
            "unidades_vendidas_total": total_unidades_vendidas,
            "ingresos_generados_total": float(total_ingresos_generados), # Convertir Decimal a float para JSON
            "desglose_por_sucursal": desglose_sucursales
        }

        return Response(informe)

class CategoriaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Ejemplo

class MarcaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows brands to be viewed or edited.
    """
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Ejemplo

@api_view(['GET'])
def product_count_view(request):
    """
    Un endpoint simple para obtener el conteo total de productos.
    """
    try:
        count = Product.objects.count()
        return Response({'total_productos': count})
    except Exception as e:
        # Considera registrar el error 'e' si tienes un sistema de logging configurado
        return Response({'error': 'Ocurrió un error al contar los productos.'}, status=500)

# ---------------------------
# VISTA PARA PRODUCTOS CON INFORMACIÓN DE STOCK POR SUCURSAL
# ---------------------------
class ProductosConStockView(ListAPIView):
    """
    Vista para listar todos los productos activos.
    Si se proporciona sucursal_id en los query params, el ProductoSerializer
    incluirá el stock específico para esa sucursal en cada producto.
    """
    serializer_class = ProductoSerializer # Cambiar a ProductoSerializer
    permission_classes = [permissions.AllowAny] # O ajusta según necesites (ej. IsAuthenticated)

    def get_queryset(self):
        """
        Retorna el queryset base de todos los productos.
        Si tu modelo Producto tiene un campo 'activo', puedes filtrar aquí:
        return Product.objects.filter(activo=True).order_by('nombre_producto')
        """
        return Product.objects.all().order_by('nombre_producto') # Devuelve todos los productos

    def get_serializer_context(self):
        """
        Añade 'sucursal_id' del query params al contexto del serializador.
        Esto permite al ProductoSerializer calcular 'stock_sucursal_seleccionada'.
        """
        context = super().get_serializer_context()
        sucursal_id = self.request.query_params.get('sucursal_id')
        context['sucursal_id'] = int(sucursal_id) if sucursal_id and sucursal_id.isdigit() else None
        return context