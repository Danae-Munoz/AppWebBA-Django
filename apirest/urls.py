from django.urls import path
from .views import autenticar

urlpatterns = [
    path('autenticar/<tipousu>/<username>/<password>', autenticar, name="autenticar"),
    #path('obtener_equipos_en_bodega', obtener_equipos_en_bodega, name='obtener_equipos_en_bodega'),
    #path('obtener_productos', obtener_productos, name='obtener_productos'),
]