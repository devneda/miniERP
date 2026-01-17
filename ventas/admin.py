from django.contrib import admin
from .models import Pedido, LineaPedido, EstadoPedido

class LineaPedidoInline(admin.TabularInline):
    model = LineaPedido
    extra = 0
    # Hacemos los campos snapshot de solo lectura para que se vea que son automáticos
    readonly_fields = ('precio_unitario', 'tipo_iva', 'descripcion')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'estado', 'fecha_pedido', 'total_neto')
    inlines = [LineaPedidoInline]
    readonly_fields = ('total_bruto', 'total_iva', 'total_neto') # Totales calculados, solo lectura

admin.site.register(EstadoPedido)
# Por simplicidad, registramos LineaPedido también
admin.site.register(LineaPedido)