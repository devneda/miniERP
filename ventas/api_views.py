from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .models import Producto
from .serializers import ProductoSerializer
from .permissions import EsStaffOSoloLectura

class ProductoListView(generics.ListCreateAPIView):
    """
    GET /api/productos/ --> Lista todos los productos.
    POST /api/productos/ --> Crea un nuevo producto (solo para staff).
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [EsStaffOSoloLectura]