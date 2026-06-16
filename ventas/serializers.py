from rest_framework import serializers
from core.models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    stock = serializers.SerializerMethodField()
    class Meta:
        model = Producto
        fields = ['id', 'sku', 'nombre', 'precio_base', 'tipo_iva', 'stock']
    
    def get_stock(self, obj):
        return obj.stock
