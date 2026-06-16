from django.urls import path
from . import views
from .api_views import ProductoListView

urlpatterns = [
    path('pedidos/', views.PedidoListView.as_view(), name='pedido_list'),
    path('pedidos/eliminar/<int:pk>/', views.PedidoDeleteView.as_view(), name='pedido_delete'),
    path('api/productos/', ProductoListView.as_view(), name='api_producto_list')
]
