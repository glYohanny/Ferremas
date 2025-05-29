from django.urls import path, include
from rest_framework.routers import DefaultRouter
from finanzas_app.api.views import TipoCambioViewSet, ConversionDivisaViewSet

# Crear router para ViewSets
router = DefaultRouter()
router.register(r'tipos-cambio', TipoCambioViewSet)
router.register(r'conversiones', ConversionDivisaViewSet)

# URLs de la aplicación
urlpatterns = [
    path('', include(router.urls)),
]