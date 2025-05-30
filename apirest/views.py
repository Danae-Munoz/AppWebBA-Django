from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate
from core.models import PerfilUsuario
from django.db import connection
from datetime import datetime
import requests


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


@csrf_exempt
@api_view(['GET'])
def obtener_equipos_en_bodega(request):
    if request.method == 'GET':
        cursor = connection.cursor()

        # Ejecutar el procedimiento almacenado
        cursor.execute("EXEC SP_OBTENER_EQUIPOS_EN_BODEGA")

        # Obtener los resultados 
        results = cursor.fetchall()

        # Convertir los resultados en una lista de diccionarios
        data = []
        for row in results: 
            idprod = row[0]
            nomprod = row[1]
            descprod = row[2]
            precio = row[3]
            imagen = row[4]
            cantidad = row[5]
            disponibilidad = row[6]

            data.append({
                'idprod': idprod,
                'nomprod': nomprod,
                'descprod': descprod,
                'precio': precio,
                'imagen': imagen,
                'cantidad': cantidad,
                'disponibilidad': disponibilidad,
            })

        return JsonResponse(data, safe=False)

def obtener_valor_dolar_observado():
    usuario = 'est.cardenas@duocuc.cl'  # ← Reemplaza esto
    contrasena = 'Ximena20.'  # ← Reemplaza esto
    fecha_actual = datetime.now().strftime('%Y-%m-%d')

    url = f"https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user={usuario}&pass={contrasena}&firstdate={fecha_actual}&timeseries=F073.TCO.PRE.Z.D"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        valor_dolar = float(data['Series']['Obs'][0]['value'])
        return valor_dolar
    except Exception as e:
        print(f"Error al obtener valor dólar: {e}")
        return None



@csrf_exempt
@api_view(['GET'])
def obtener_productos(request):
    if request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute("EXEC SP_OBTENER_PRODUCTOS")
        results = cursor.fetchall()

        valor_dolar = obtener_valor_dolar_observado()
        if not valor_dolar:
            return JsonResponse({'error': 'No se pudo obtener el valor del dólar desde el Banco Central.'}, status=500)

        data = []
        for row in results:
            precio_pesos = row[3]
            precio_dolares = round(precio_pesos / valor_dolar, 2)
            data.append({
                'idprod': row[0],
                'nomprod': row[1],
                'descprod': row[2],
                'precio':  row[3],
                'precio_dolares': precio_dolares,
                'imagen': row[4]
            })

        return JsonResponse(data, safe=False)

