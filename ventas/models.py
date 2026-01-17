from django.db import models
from core.models import Cliente, Producto

class EstadoPedido(models.Model):
    """Tabla maestra para los estados: BORRADOR, CONFIRMADO..."""
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT, related_name='pedidos')
    estado = models.ForeignKey(EstadoPedido, on_delete=models.RESTRICT, default=1)     
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total_bruto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_neto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['cliente', 'fecha_pedido'], name='idx_pedido_cli_fecha'),
            models.Index(fields=['cliente'], name='idx_pedido_cliente'),
        ]

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.nombre}"

class LineaPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='lineas')
    producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    
    # --- SNAPSHOT (Datos congelados en el momento de la venta) ---
    # Guardamos copia de estos datos por si el producto cambia en el futuro
    descripcion = models.CharField(max_length=255) 
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2) # El precio que tenía al comprar
    tipo_iva = models.DecimalField(max_digits=4, decimal_places=2) # El IVA que tenía al comprar
    # -------------------------------------------------------------
    
    cantidad = models.DecimalField(max_digits=10, decimal_places=2) # Ahora permite decimales (ej: 1.5 kg)

    def save(self, *args, **kwargs):
        # Al guardar, si no tenemos los datos del snapshot, los copiamos del producto
        if not self.id: 
            self.descripcion = self.producto.nombre
            self.precio_unitario = self.producto.precio_base
            self.tipo_iva = self.producto.tipo_iva
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.descripcion}"