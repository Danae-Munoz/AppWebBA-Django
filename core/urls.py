from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from .views import home, administrar_productos, tienda, ficha, iniciar_pago_servicio,retorno_pago_servicio 
from .views import iniciar_sesion, registrar_usuario, cerrar_sesion, ingresar_solicitud_servicio, ver_facturas
from .views import perfil_usuario, iniciar_pago, pago_exitoso, obtener_solicitudes_de_servicio

urlpatterns = [
    path('administrar_productos/<action>/<id>', administrar_productos, name="administrar_productos"),
    path('cambiar_password/', auth_views.PasswordChangeView.as_view(template_name='core/cambiar_password.html', success_url='/password_cambiada'), name='cambiar_password'),
    path('ficha/<id>', ficha, name="ficha"),
    path('', home, name="home"),
    path('iniciar_pago/<id>', iniciar_pago, name="iniciar_pago"),
    path('iniciar_sesion/', iniciar_sesion, name="iniciar_sesion"),
    path('obtener_solicitudes_de_servicio/', obtener_solicitudes_de_servicio, name="obtener_solicitudes_de_servicio"),
    path('pago_exitoso/', pago_exitoso, name="pago_exitoso"),
    path('password_cambiada/', TemplateView.as_view(template_name='core/password_cambiada.html'), name='password_cambiada'),
    path('perfil_usuario/', perfil_usuario, name="perfil_usuario"),
    path('registrar_usuario/', registrar_usuario, name="registrar_usuario"),
    path('tienda', tienda, name="tienda"),
    path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
    path('ingresar_solicitud_servicio/', ingresar_solicitud_servicio, name='ingresar_solicitud_servicio'),
    path('iniciar_pago_servicio/', iniciar_pago_servicio, name='iniciar_pago_servicio'),
    path('retorno_pago_servicio/', retorno_pago_servicio, name='retorno_pago_servicio'),
    path('ver_facturas/<str:rut>/', ver_facturas, name='ver_facturas'),

]