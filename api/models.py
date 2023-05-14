from django.db import models
from django.utils.translation import gettext_lazy as _
from math import fabs


# Create your models here.
class Cuenta(models.Model):
    class TipoCuenta(models.TextChoices):
        INGRESO_EGRESO = 'IE', _('Ingreso y Gasto')
        INGRESO = 'I', _('Ingreso')
        GASTO = 'E', _('Gasto')

    nombre = models.CharField(max_length=60)
    monto = models.FloatField()
    tipo = models.CharField(max_length=3, default=TipoCuenta.INGRESO_EGRESO, choices=TipoCuenta.choices)

    def setMonto(self, monto):
        if self.tipo == Cuenta.TipoCuenta.INGRESO:
            self.monto += fabs(monto)
        elif self.tipo == Cuenta.TipoCuenta.GASTO:
            self.monto -= fabs(monto)
        else:
            self.monto += monto


class Transaccion(models.Model):
    origen = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='cuenta_origen')
    destino = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='cuenta_destino')
    fecha = models.DateField()
    monto = models.FloatField()
    concepto = models.TextField()


class TransaccionDTO:

    def __init__(self, transaccion):
        self.destino = transaccion.destino
        self.origen = transaccion.origen
        self.fecha = transaccion.fecha
        self.monto = transaccion.monto
        self.id = transaccion.id
        self.concepto = transaccion.concepto

    def as_json(self):
        return {
            'id': self.id,
            'origen': {
                'id': self.origen.id,
                'nombre': self.origen.nombre
            },
            'destino': {
                'id': self.destino.id,
                'nombre': self.destino.nombre
            },
            'fecha': str(self.fecha),
            'monto': self.monto,
            'concepto': self.concepto
        }


