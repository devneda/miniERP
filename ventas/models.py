from django.db import models
from core.models import Cliente, Producto
from decimal import Decimal

class Pedido(models.Model):
    class Status(models.TextChoices):
        BORRADOR = 'borrador', 'Borrador'
        CONFIRMADO = 'confirmado', 'Confirmado'
        PROCESANDO = 'procesando', 'Procesando'
        ENVIADO = 'enviado', 'Enviado'
        ENTREGADO = 'entregado', 'Entregado'
        CANCELADO = 'cancelado', 'Cancelado'

    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT, related_name='pedidos')
    estado = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.BORRADOR
    )
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    iva_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=21.00)
    total_bruto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_neto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_aplicado = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['cliente', 'fecha_pedido'], name='idx_pedido_cli_fecha'),
            models.Index(fields=['cliente'], name='idx_pedido_cliente'),
        ]

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.nombre}"

    def calcular_totales(self):
        """Calcula base, IVA y total sumando las líneas."""
        base = sum(linea.total_price for linea in self.lineas.all())
        self.total_bruto = Decimal(base)
        self.total_iva = self.total_bruto * (Decimal(str(self.iva_porcentaje)) / 100)
        self.total_neto = self.total_bruto + self.total_iva
        self.save()

    def confirmar_pedido(self):
        """Lógica de transición de estado."""
        if self.lineas.count() == 0:
            raise ValueError("No se puede confirmar un pedido sin líneas.")
        if self.estado != self.Status.BORRADOR:
            raise ValueError("Solo se pueden confirmar pedidos en estado borrador.")
        self.estado = self.Status.CONFIRMADO
        self.save()
class LineaPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='lineas')
    producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    
    descripcion = models.CharField(max_length=255) 
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_iva = models.DecimalField(max_digits=4, decimal_places=2)
    
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.precio_unitario * self.cantidad

    def save(self, *args, **kwargs):
        if not self.id: 
            self.descripcion = self.producto.nombre
            self.precio_unitario = self.producto.precio_base
            self.tipo_iva = self.producto.tipo_iva
        super().save(*args, **kwargs)
        self.pedido.calcular_totales()

    def __str__(self):
        return f"{self.cantidad} x {self.descripcion}"