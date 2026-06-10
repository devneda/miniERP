from django.views.generic import ListView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Pedido

class PedidoListView(ListView):
    model = Pedido
    template_name = 'ventas/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por búsqueda de nombre de cliente
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(cliente__nombre__icontains=search)
        
        return queryset.order_by('-fecha_pedido')

class PedidoDeleteView(DeleteView):
    model = Pedido
    success_url = reverse_lazy('pedido_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "El pedido ha sido eliminado correctamente.")
        return super().delete(request, *args, **kwargs)
