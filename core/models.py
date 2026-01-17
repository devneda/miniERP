from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    nif = models.CharField(max_length=30, unique=True, verbose_name="CIF/NIF")
    direccion = models.TextField(blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['nif'], name='idx_cliente_nif_unico'),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.nif})"

class Producto(models.Model):
    sku = models.CharField(max_length=100, unique=True, verbose_name="SKU")
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)    
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Base (Sin IVA)")
    tipo_iva = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="IVA (ej: 0.21)") # 0.21 para 21%
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['sku'], name='idx_producto_sku_unico'),
            models.Index(fields=['nombre'], name='idx_producto_nombre'),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.sku})"
    
    @property
    def precio_pvp(self):
        """Calcula el precio con IVA al vuelo para mostrarlo si hace falta"""
        return self.precio_base * (1 + self.tipo_iva)