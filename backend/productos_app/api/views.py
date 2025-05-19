from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from productos_app.models import Categoria as Category, Producto as Product
from .serializers import CategoriaSerializer, ProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    # queryset = Product.objects.all() # Comentamos o eliminamos la definición a nivel de clase
    serializer_class = ProductoSerializer
    permission_classes = [permissions.AllowAny]

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

class CategoriaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.AllowAny] # Permite el acceso a cualquier usuario (autenticado o no)

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