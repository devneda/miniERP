from django.db import models
from django.core.exceptions import ValidationError
from core.models import Cliente, Producto

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('BORRADOR', 'Borrador'),
        ('CONFIRMADO', 'Confirmado'),
        ('FACTURADO', 'Facturado'),
        ('COBRADO', 'Cobrado'),
    ]

    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT, related_name='pedidos')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='BORRADOR')

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.nombre} - {self.estado}"
    
class LineaPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='lineas')
    producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(cantidad__gt=0), name='cantidad_positiva')
        ]

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Pedido {self.pedido.id}"