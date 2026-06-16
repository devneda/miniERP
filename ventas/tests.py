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

    def test_recalculo_al_borrar_linea(self):
        pedido = Pedido.objects.create(cliente=self.cliente, iva_porcentaje=21)
        linea1 = LineaPedido.objects.create(pedido=pedido, producto=self.producto, cantidad=1) # 100€
        linea2 = LineaPedido.objects.create(pedido=pedido, producto=self.producto, cantidad=2) # 200€
        
        self.assertEqual(pedido.total_neto, Decimal('363.00'))
        
        linea1.delete()
        
        pedido.refresh_from_db()
        
        self.assertEqual(pedido.total_neto, Decimal('242.00'))

    def test_descuento_stock_al_confirmar(self):
        # 1. Crear pedido y línea
        pedido = Pedido.objects.create(cliente=self.cliente)
        LineaPedido.objects.create(pedido=pedido, producto=self.producto, cantidad=3)
        
        # Stock inicial es 10
        self.assertEqual(self.producto.stock, 10)
        
        # 2. Confirmar pedido
        pedido.confirmar_pedido() # Esto cambia estado a 'confirmado' y dispara el post_save
        
        # 3. Verificar stock del producto
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 7) # 10 - 3 = 7
        
        # 4. Verificar que stock_aplicado es True
        pedido.refresh_from_db()
        self.assertTrue(pedido.stock_aplicado)


