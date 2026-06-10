from django.test import TestCase
from core.models import Cliente, Producto
from .models import Pedido, LineaPedido
from decimal import Decimal

class PedidoLogicTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombre="Cliente Test",
            nif="12345678Z",
            email="test@empresa.com"
        )
        self.producto = Producto.objects.create(
            sku="PROD-TEST",
            nombre="Producto Test",
            precio_base=Decimal('100.00'),
            tipo_iva=Decimal('0.21'),
            stock=10
        )

    def test_calculo_total_iva(self):
        pedido = Pedido.objects.create(cliente=self.cliente, iva_porcentaje=21)
        
        LineaPedido.objects.create(
            pedido=pedido, 
            producto=self.producto, 
            cantidad=1
        )
        
        pedido.calcular_totales()
        
        self.assertEqual(pedido.total_bruto, Decimal('100.00'))
        self.assertEqual(pedido.total_iva, Decimal('21.00'))
        self.assertEqual(pedido.total_neto, Decimal('121.00'))

    def test_confirmar_pedido_sin_lineas(self):
        pedido = Pedido.objects.create(cliente=self.cliente)
        with self.assertRaises(ValueError):
            pedido.confirmar_pedido()

    def test_transicion_estado_confirmado(self):
        pedido = Pedido.objects.create(cliente=self.cliente)
        LineaPedido.objects.create(pedido=pedido, producto=self.producto, cantidad=1)
        
        pedido.confirmar_pedido()
        self.assertEqual(pedido.estado, Pedido.Status.CONFIRMADO)
