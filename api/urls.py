from django.urls import path
from . import views
urlpatterns = [
    path('cuentas/', views.cuentasHandler.handle),
    path('transacciones/', views.transaccionHandler.handle)
]