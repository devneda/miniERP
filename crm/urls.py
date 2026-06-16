from django.urls import path
from . import views

urlpatterns = [
    path('oportunidades/', views.OportunidadListView.as_view(), name='oportunidad_list'),
    path('dashboard/', views.dashboard_crm, name='crm_dashboard'),
]
