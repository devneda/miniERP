from django.urls import path
from . import views

urlpatterns = [
    path('pedidos/', views.PedidoListView.as_view(), name='pedido_list'),
    path('pedidos/eliminar/<int:pk>/', views.PedidoDeleteView.as_view(), name='pedido_delete'),
]
