from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate
from core.models import PerfilUsuario
from django.db import connection

@csrf_exempt
@api_view(['GET'])
def autenticar(request, tipousu, username, password):
    user = authenticate(username=username, password=password)
    if user:
        perfil = PerfilUsuario.objects.get(user=user)
        nombre = f'{user.first_name} {user.last_name}'
        tipo = perfil.tipousu
        if tipo in [tipousu, 'Administrador']:
            return JsonResponse({'Autenticado': True, 'NombreUsuario': nombre, 'TipoUsuario': tipo, 'Mensaje': ''})
        msg = f'La cuenta de usuario {nombre} es del perfil {tipo}, por lo que no puede ingresar al sistema'
    else:
        nombre, tipo, msg = '', '', 'La cuenta o la contraseña no coinciden con un usuario válido'
    return JsonResponse({'Autenticado': False, 'NombreUsuario': nombre, 'TipoUsuario': tipo, 'Mensaje': msg})
