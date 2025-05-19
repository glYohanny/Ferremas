from django.urls import path
from informes_app.api.views import VentasMensualesAPIView # Ajusta la importación si tu views.py está en otro lugar

urlpatterns = [
    path('ventas-mensuales/', VentasMensualesAPIView.as_view(), name='api-informe-ventas-mensuales'),
    # Aquí añadirás más URLs para otros informes
]