from django.shortcuts import render
from django.http import JsonResponse
from . import models
from django.forms.models import model_to_dict
import json
from datetime import datetime as dt
from .utils import RequestHandler


class JsonRequestHandler(RequestHandler):
    def default(self, request):
        return JsonResponse({"message": "Not implemented"}, status=501)


class CuentasHandler(JsonRequestHandler):

    def get(self, request):
        data = [model_to_dict(obj) for obj in models.Cuenta.objects.all()]
        return JsonResponse(data, safe=False)

    def post(self, request):
        valores_cuenta = json.loads(request.body)
        cuenta = models.Cuenta()
        cuenta.nombre = valores_cuenta["nombreCuenta"]
        cuenta.tipo = models.Cuenta.TipoCuenta(valores_cuenta["tipoCuenta"])
        cuenta.monto = 0.0
        cuenta.save()
        return JsonResponse(model_to_dict(cuenta))


class TransaccionesHandler(JsonRequestHandler):

    def get(self, request):
        data = [models.TransaccionDTO(obj).as_json() for obj in models.Transaccion.objects.all()]
        return JsonResponse(data, safe=False)

    def post(self, request):
        print(request.GET["type"])

        v_transaccion = json.loads(request.body)
        cuentaOrigen = models.Cuenta.objects.get(id=v_transaccion["cuentaOrigen"])
        cuentaDestino = models.Cuenta.objects.get(id=v_transaccion["cuentaDestino"])
        monto = v_transaccion["monto"]
        fecha = v_transaccion["fecha"]
        fecha = dt.strptime(fecha, "%Y-%m-%d").date()
        transaccion = models.Transaccion()
        transaccion.origen = cuentaOrigen
        transaccion.destino = cuentaDestino
        transaccion.monto = monto
        transaccion.fecha = fecha
        transaccion.concepto = v_transaccion["concepto"]
        transaccion.save()
        cuentaDestino.setMonto(monto)
        cuentaDestino.save()
        cuentaOrigen.setMonto(-monto)
        cuentaOrigen.save()
        return JsonResponse(model_to_dict(transaccion), safe=False)


cuentasHandler = CuentasHandler()
transaccionHandler = TransaccionesHandler()


