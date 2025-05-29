from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView # TokenObtainPairView ya no se importa directamente aquí
from django.conf import settings
from django.conf.urls.static import static
from usuarios_app.api.views import CustomTokenObtainPairView # Importar tu vista personalizada

urlpatterns = [
    
    path('admin/', admin.site.urls),
    
    # Incluir las URLs de cada aplicación
    path('api/usuarios/', include('usuarios_app.api.urls')),
    path('api/geografia/', include('geografia_app.api.urls')),
    path('api/sucursales/', include('sucursales_app.api.urls')),
    path('api/productos/', include('productos_app.api.urls')),
    path('api/inventario/', include('inventario_app.api.urls')),
    path('api/pedidos/', include('pedidos_app.api.urls')),
    path('api/pagos/', include('pagos_app.api.urls')),
    path('api/marketing/', include('marketing_app.api.urls')),
    path('api/integraciones/', include('integraciones_app.api.urls')),
    path('api/finanzas/', include('finanzas_app.api.urls')),
    path('api/informes/', include('informes_app.api.urls')), 
    
    # Authentication URLs (opcionales)
    path('api-auth/', include('rest_framework.urls')),
    
    # Para Django Rest Framework con token auth (opcional)
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'), # Usar tu vista personalizada
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

# Servir archivos multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
