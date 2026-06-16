import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Pedido, LineaPedido

logger = logging.getLogger(__name__)

@receiver(post_delete, sender=LineaPedido)
def actualizar_pedido_al_borrar_linea(sender, instance, **kwargs):
    """Recalcula los totales del pedido cuando una línea es eliminada"""
    instance.pedido.calcular_totales()

@receiver(post_save, sender=Pedido)
def reducir_stock_al_confirmar(sender, instance, created, **kwargs):
    """Resta stock de los productos cuando un pedido pasa a CONFIRMADO"""
    if instance.estado == Pedido.Status.CONFIRMADO and not instance.stock_aplicado:
        for linea in instance.lineas.all():
            if linea.producto.stock < linea.cantidad:
                error_msg = f"Stock insuficiente para {linea.producto.nombre}. Requerido: {linea.cantidad}, Disponible: {linea.producto.stock}"
                logger.error(error_msg)
                raise ValueError(error_msg)

        for linea in instance.lineas.all():
            producto = linea.producto
            producto.stock -= int(linea.cantidad)
            producto.save()
        
        Pedido.objects.filter(pk=instance.pk).update(stock_aplicado=True)
