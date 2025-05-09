from rest_framework import serializers
from marketing_app.models import Promocion, ProductoPromocion, Notificacion, ClienteNotificacion

# ---------------------------
# PROMOCIONES
# ---------------------------
class PromocionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocion
        fields = '__all__'

class ProductoPromocionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoPromocion
        fields = '__all__'

# ---------------------------
# NOTIFICACIONES
# ---------------------------
class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = '__all__'

class ClienteNotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClienteNotificacion
        fields = '__all__'