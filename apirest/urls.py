from django.urls import path
from .views import autenticar,obtener_equipos_en_bodega,obtener_productos, actualizar_estado_guia_despacho
from .views import consultar_productos_disponibles, reservar_producto, obtener_guias_de_despacho 

urlpatterns = [
    path('autenticar/<tipousu>/<username>/<password>', autenticar, name="autenticar"),
    path('obtener_equipos_en_bodega', obtener_equipos_en_bodega, name='obtener_equipos_en_bodega'),
    path('obtener_productos', obtener_productos, name='obtener_productos'),
    path('consultar_productos_disponibles', consultar_productos_disponibles, name='consultar_productos_disponibles'),
    path('reservar_producto', reservar_producto, name='reservar_producto'),
    path('obtener_guias_de_despacho', obtener_guias_de_despacho, name='obtener_guia_de_despacho'),
    path('actualizar_estado_guia_despacho', actualizar_estado_guia_despacho, name='actualizar_estado_guia_despacho'),
]