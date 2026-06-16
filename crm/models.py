from django.db import models
from core.models import Cliente

class Oportunidad(models.Model):
    class Etapa(models.TextChoices):
        PROSPECCION = 'prospeccion', 'Prospección'
        PROPUESTA = 'propuesta', 'Propuesta'
        NEGOCIACION = 'negociacion', 'Negociación'
        CERRADA_GANADA = 'ganada', 'Cerrada Ganada'
        CERRADA_PERDIDA = 'perdida', 'Cerrada Perdida'

    titulo = models.CharField(max_length=255, verbose_name="Título")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='oportunidades')
    valor_estimado = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor Estimado")
    etapa = models.CharField(
        max_length=20, 
        choices=Etapa.choices, 
        default=Etapa.PROSPECCION
    )
    fecha_creacion = models.DateField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_cierre = models.DateField(verbose_name="Fecha de Cierre")
    hora_cierre = models.TimeField(null=True, blank=True, verbose_name="Hora de Cierre")
    dias_abierta = models.IntegerField(default=0, verbose_name="Días Abierta")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titulo} - {self.cliente.nombre}"

    class Meta:
        verbose_name_plural = "Oportunidades"
