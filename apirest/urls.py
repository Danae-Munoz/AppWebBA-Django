from django.urls import path
from .views import autenticar,obtener_equipos_en_bodega,obtener_productos
from .views import consultar_productos_disponibles, reservar_producto 

urlpatterns = [
    path('autenticar/<tipousu>/<username>/<password>', autenticar, name="autenticar"),
    path('obtener_equipos_en_bodega', obtener_equipos_en_bodega, name='obtener_equipos_en_bodega'),
    path('obtener_productos', obtener_productos, name='obtener_productos'),
    path('consultar_productos_disponibles', consultar_productos_disponibles, name='consultar_productos_disponibles'),
    path('reservar_producto', reservar_producto, name='reservar_producto'),
]