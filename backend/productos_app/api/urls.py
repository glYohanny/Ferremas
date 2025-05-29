from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProductoViewSet, product_count_view, MarcaViewSet, ProductosConStockView # Importar la nueva vista

# Crear router para ViewSets
router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'marcas', MarcaViewSet) # Registrar el nuevo ViewSet para Marcas
router.register(r'producto', ProductoViewSet, basename='producto') # Tu endpoint existente para productos
# URLs de la aplicación
urlpatterns = [
    path('', include(router.urls)),
    # Ruta para el nuevo endpoint de conteo de productos
    path('count/', product_count_view, name='product-count'),
    # Nueva ruta para productos con stock (usada por el catálogo)
    path('productos-con-stock/', ProductosConStockView.as_view(), name='productos-con-stock-list'),
    # Rutas adicionales específicas no manejadas por el router
]