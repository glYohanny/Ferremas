from rest_framework import serializers
from finanzas_app.models import TipoCambio, ConversionDivisa

# ---------------------------
# TIPO DE CAMBIO
# ---------------------------
class TipoCambioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCambio
        fields = '__all__'

# ---------------------------
# CONVERSIÓN DIVISA
# ---------------------------
class ConversionDivisaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionDivisa
        fields = '__all__'