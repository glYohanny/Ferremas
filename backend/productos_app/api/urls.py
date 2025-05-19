from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProductoViewSet, product_count_view

# Crear router para ViewSets
router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'producto', ProductoViewSet, basename='producto') # Tu endpoint existente para productos

# URLs de la aplicación
urlpatterns = [
    path('', include(router.urls)),
    # Ruta para el nuevo endpoint de conteo de productos
    path('count/', product_count_view, name='product-count'),
    # Rutas adicionales específicas no manejadas por el router
]