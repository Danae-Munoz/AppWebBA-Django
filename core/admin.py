from django.contrib import admin
from .models import PerfilUsuario, Producto, Factura, SolicitudServicio
from .models import GuiaDespacho, StockProducto, AnwoStockProducto

# Register your models here.

admin.site.register(PerfilUsuario)
admin.site.register(Producto)
admin.site.register(Factura)
admin.site.register(SolicitudServicio)
admin.site.register(GuiaDespacho)
admin.site.register(StockProducto)
admin.site.register(AnwoStockProducto)