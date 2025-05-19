from django.shortcuts import render
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser # O tu permiso de administrador personalizado
from ..models import Venta # Asegúrate de que Venta esté definido en tus modelos de informes_app
import datetime

# Create your views here.

class VentasMensualesAPIView(APIView):
    permission_classes = [IsAdminUser] # Solo administradores pueden acceder

    def get(self, request, *args, **kwargs):
        # Opcional: Obtener filtros de fecha del request.query_params
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        queryset = Venta.objects.all()

        if start_date_str:
            try:
                start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha_venta__gte=start_date)
            except ValueError:
                return Response({"error": "Formato de fecha de inicio inválido. Usar YYYY-MM-DD."}, status=400)

        if end_date_str:
            try:
                end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha_venta__lte=end_date)
            except ValueError:
                return Response({"error": "Formato de fecha de fin inválido. Usar YYYY-MM-DD."}, status=400)

        ventas_por_mes = queryset.annotate(
            mes_anio_db=TruncMonth('fecha_venta') # Trunca la fecha al primer día del mes
        ).values(
            'mes_anio_db' # Agrupa por este mes truncado
        ).annotate(
            total_ventas=Sum('total_venta'),
            numero_ventas=Count('id')
        ).order_by('mes_anio_db')

        # Formatear la salida para que sea más amigable para el frontend
        data_formateada = [
            {
                "mes_anio": item['mes_anio_db'].strftime('%Y-%m') if item['mes_anio_db'] else 'N/A', # Formato YYYY-MM
                "total_ventas": item['total_ventas'] or 0,
                "numero_ventas": item['numero_ventas'] or 0
            }
            for item in ventas_por_mes
        ]
        return Response(data_formateada)