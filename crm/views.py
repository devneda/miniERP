from django.shortcuts import render
from django.views.generic import ListView
from .models import Oportunidad
from django.db.models import Sum

def dashboard_crm(request):
    """Vista para mostrar el resumen del CRM y el KPI de conversión"""
    total_opps = Oportunidad.objects.count()
    ganadas = Oportunidad.objects.filter(etapa='ganada').count()
    perdidas = Oportunidad.objects.filter(etapa='perdida').count()
    valor_total = Oportunidad.objects.aggregate(total=Sum('valor_estimado'))['total'] or 0
    
    # Cálculo de la Tasa de Conversión (KPI)
    total_cerradas = ganadas + perdidas
    tasa_conversion = (ganadas / total_cerradas * 100) if total_cerradas > 0 else 0

    context = {
        'total_opps': total_opps,
        'ganadas': ganadas,
        'valor_total': valor_total,
        'tasa_conversion': round(tasa_conversion, 2)
    }
    return render(request, 'crm/dashboard.html', context)

class OportunidadListView(ListView):

    model = Oportunidad
    template_name = 'crm/oportunidad_list.html'
    context_object_name = 'oportunidades'

    def get_queryset(self):
        queryset = super().get_queryset()
        etapa = self.request.GET.get('etapa')
        if etapa:
            queryset = queryset.filter(etapa=etapa)
        return queryset.order_by('-fecha_cierre')
