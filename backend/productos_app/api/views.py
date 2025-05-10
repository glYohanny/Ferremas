from rest_framework import viewsets, permissions
from productos_app.models import Categoria as Category, Producto as Product
from .serializers import CategoriaSerializer, ProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all() # Uses the imported Product model
    serializer_class = ProductoSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Optionally restricts the returned products based on a query parameter.
        If your Product model has an 'owner' field linked to your custom Usuario model
        (which uses 'nombre_usuario' as USERNAME_FIELD), you might filter by that.

        Example: If Product has an 'owner' (ForeignKey to Usuario) and you want to filter
        by the owner's 'nombre_usuario' using a 'owner_username' query parameter:
        """
        queryset = self.queryset
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