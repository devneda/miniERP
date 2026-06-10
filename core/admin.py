from django.contrib import admin
from .models import Cliente, Producto
from ventas.forms import ProductoForm, ClienteForm

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    form = ClienteForm

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    form = ProductoForm