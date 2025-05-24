from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from .models import Producto, PerfilUsuario
from urllib.parse import urlencode
from .forms import ProductoForm, IniciarSesionForm
from .forms import RegistrarUsuarioForm, PerfilUsuarioForm
#from .error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from django.db import connection
import random
from datetime import date
import requests

def home(request):
    return render(request, "core/home.html")

def iniciar_sesion(request):
    data = {"mesg": "", "form": IniciarSesionForm()}

    if request.method == "POST":
        form = IniciarSesionForm(request.POST)
        if form.is_valid:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    tipousu = PerfilUsuario.objects.get(user=user).tipousu
                    if tipousu != 'Bodeguero':
                        return redirect(home)
                    else:
                        data["mesg"] = "¡La cuenta o la password no son correctos!"    
                else:
                    data["mesg"] = "¡La cuenta o la password no son correctos!"
            else:
                data["mesg"] = "¡La cuenta o la password no son correctos!"
    return render(request, "core/iniciar_sesion.html", data)

def cerrar_sesion(request):
    logout(request)
    return redirect(home)

def tienda(request):
    productos = Producto.objects.exclude(idprod__in=[9, 10, 11]).order_by('idprod')
    data = {"list": productos}
    return render(request, "core/tienda.html", data)

# https://www.transbankdevelopers.cl/documentacion/como_empezar#como-empezar
# https://www.transbankdevelopers.cl/documentacion/como_empezar#codigos-de-comercio
# https://www.transbankdevelopers.cl/referencia/webpay
# https://www.transbankdevelopers.cl/referencia/webpay#ambientes-y-credenciales

# Tipo de tarjeta   Detalle                        Resultado
# ---------------   -----------------------------  ------------------------------
# VISA              4051885600446623
#                   CVV 123
#                   cualquier fecha de expiración  Genera transacciones aprobadas.
# AMEX              3700 0000 0002 032
#                   CVV 1234
#                   cualquier fecha de expiración  Genera transacciones aprobadas.
# MASTERCARD        5186 0595 5959 0568
#                   CVV 123
#                   cualquier fecha de expiración  Genera transacciones rechazadas.
# Redcompra         4051 8842 3993 7763            Genera transacciones aprobadas (para operaciones que permiten débito Redcompra y prepago)
# Redcompra         4511 3466 6003 7060            Genera transacciones aprobadas (para operaciones que permiten débito Redcompra y prepago)
# Redcompra         5186 0085 4123 3829            Genera transacciones rechazadas (para operaciones que permiten débito Redcompra y prepago)

@csrf_exempt
def ficha(request, id):
    data = {"mesg": "", "producto": None}

    # Cuando el usuario hace clic en el boton COMPRAR, se ejecuta el METODO POST del
    # formulario de ficha.html, con lo cual se redirecciona la página para que
    # llegue a esta VISTA llamada "FICHA". A continuacion se verifica que sea un POST 
    # y se valida que se trate de un usuario autenticado que no sea de estaff, 
    # es decir, se comprueba que la compra sea realizada por un CLIENTE REGISTRADO.
    # Si se tata de un CLIENTE REGISTRADO, se redirecciona a la vista "iniciar_pago"
    if request.method == "POST":
        if request.user.is_authenticated and not request.user.is_staff:
            return redirect(iniciar_pago, id)
        else:
            # Si el usuario que hace la compra no ha iniciado sesión,
            # entonces se le envía un mensaje en la pagina para indicarle
            # que primero debe iniciar sesion antes de comprar
            data["mesg"] = "¡Para poder comprar debe iniciar sesión como cliente!"

    # Si visitamos la URL de FICHA y la pagina no nos envia un METODO POST, 
    # quiere decir que solo debemos fabricar la pagina y devolvera al browser
    # para que se muestren los datos de la FICHA
    data["producto"] = Producto.objects.get(idprod=id)
    return render(request, "core/ficha.html", data)

@csrf_exempt
def iniciar_pago(request, id):
    print("Webpay Plus Transaction.create")
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = request.user.username

    producto = Producto.objects.get(idprod=id)
    precio_producto = producto.precio
    precio_instalacion = 25000
    total_pagar = precio_producto + precio_instalacion

    return_url = request.build_absolute_uri('/pago_exitoso/')

    # Guardar producto comprado en sesión
    request.session['producto_comprado_id'] = producto.idprod

    # Transacción de prueba Webpay
    tx = Transaction(WebpayOptions(
        commerce_code="597055555532",
        api_key="579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
        integration_type="TEST"
    ))
    response = tx.create(buy_order, session_id, total_pagar, return_url)
    print(response['token'])

    perfil = PerfilUsuario.objects.get(user=request.user)

    context = {
        "buy_order": buy_order,
        "session_id": session_id,
        "return_url": return_url,
        "token_ws": response['token'],
        "url_tbk": response['url'],
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "rut": perfil.rut,
        "dirusu": perfil.dirusu,
        "producto": producto,
        "precio_producto": precio_producto,
        "precio_instalacion": precio_instalacion,
        "total_pagar": total_pagar,
    }

    return render(request, "core/iniciar_pago.html", context)

@csrf_exempt
def pago_exitoso(request):
    if request.method == "GET":
        token = request.GET.get("token_ws")
        print("commit for token_ws: {}".format(token))

        tx = Transaction(options=WebpayOptions(
            commerce_code="597055555532",
            api_key="579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
            integration_type="TEST"
        ))

        response = tx.commit(token=token)
        print("response: {}".format(response))

        user = User.objects.get(username=response['session_id'])
        perfil = PerfilUsuario.objects.get(user=user)

        try:
            idprod_comprado = request.session.pop("producto_comprado_id", None)
            if not idprod_comprado:
                raise Exception("No se encontró el producto comprado en sesión.")

            producto = Producto.objects.get(idprod=idprod_comprado)
            fecha_actual = date.today()

            with connection.cursor() as cursor:
                # Crear factura de compra
                cursor.execute("EXEC SP_CREAR_FACTURA %s, %s, %s, %s, %s", [
                    perfil.rut,
                    producto.idprod,
                    fecha_actual,
                    f"Compra de equipo: {producto.nomprod}",
                    producto.precio
                ])

                # Crear factura de instalación
                cursor.execute("EXEC SP_CREAR_FACTURA %s, %s, %s, %s, %s", [
                    perfil.rut,
                    10,  # ID del servicio de instalación
                    fecha_actual,
                    "Instalación de equipo nuevo",
                    25000
                ])
                nrofac_instalacion = cursor.fetchone()[0]

                # Seleccionar técnico aleatorio
                cursor.execute("SELECT rut FROM PerfilUsuario WHERE tipousu = 'Técnico'")
                tecnicos = cursor.fetchall()
                if not tecnicos:
                    raise Exception("No hay técnicos disponibles.")
                ruttec = random.choice(tecnicos)[0]

                # Crear solicitud de instalación
                cursor.execute("EXEC SP_CREAR_SOLICITUD_SERVICIO %s, %s, %s, %s, %s, %s", [
                    nrofac_instalacion,
                    "Instalación",
                    "Instalación de equipo nuevo comprado por el cliente.",
                    fecha_actual,
                    ruttec,
                    10
                ])

        except Exception as e:
            return render(request, "core/error_pago.html", {
                "mensaje": f"Ocurrió un error al procesar la solicitud de instalación: {str(e)}"
            })

        context = {
            "buy_order": response['buy_order'],
            "session_id": response['session_id'],
            "amount": response['amount'],
            "response": response,
            "token_ws": token,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "rut": perfil.rut,
            "dirusu": perfil.dirusu,
            "precio_producto": producto.precio,
            "precio_instalacion": 25000,
            "response_code": response['response_code']
        }

        return render(request, "core/pago_exitoso.html", context)
    else:
        return redirect("home")

@csrf_exempt
def administrar_productos(request, action, id):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(home)

    data = {"mesg": "", "form": ProductoForm, "action": action, "id": id, "formsesion": IniciarSesionForm}

    if action == 'ins':
        if request.method == "POST":
            form = ProductoForm(request.POST, request.FILES)
            if form.is_valid:
                try:
                    form.save()
                    data["mesg"] = "¡El producto fue creado correctamente!"
                except:
                    data["mesg"] = "¡No se puede crear dos vehículos con el mismo ID!"

    elif action == 'upd':
        objeto = Producto.objects.get(idprod=id)
        if request.method == "POST":
            form = ProductoForm(data=request.POST, files=request.FILES, instance=objeto)
            if form.is_valid:
                form.save()
                data["mesg"] = "¡El producto fue actualizado correctamente!"
        data["form"] = ProductoForm(instance=objeto)

    elif action == 'del':
        try:
            Producto.objects.get(idprod=id).delete()
            data["mesg"] = "¡El producto fue eliminado correctamente!"
            return redirect(administrar_productos, action='ins', id = '-1')
        except:
            data["mesg"] = "¡El producto ya estaba eliminado!"

    data["list"] = Producto.objects.all().order_by('idprod')
    return render(request, "core/administrar_productos.html", data)

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            rut = request.POST.get("rut")
            tipousu = request.POST.get("tipousu")
            dirusu = request.POST.get("dirusu")
            PerfilUsuario.objects.update_or_create(user=user, rut=rut, tipousu=tipousu, dirusu=dirusu)
            return redirect(iniciar_sesion)
    form = RegistrarUsuarioForm()
    return render(request, "core/registrar_usuario.html", context={'form': form})

def perfil_usuario(request):
    data = {"mesg": "", "form": PerfilUsuarioForm}

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.email = request.POST.get("email")
            user.save()
            perfil = PerfilUsuario.objects.get(user=user)
            perfil.rut = request.POST.get("rut")
            perfil.tipousu = request.POST.get("tipousu")
            perfil.dirusu = request.POST.get("dirusu")
            perfil.save()
            data["mesg"] = "¡Sus datos fueron actualizados correctamente!"

    perfil = PerfilUsuario.objects.get(user=request.user)
    form = PerfilUsuarioForm()
    form.fields['first_name'].initial = request.user.first_name
    form.fields['last_name'].initial = request.user.last_name
    form.fields['email'].initial = request.user.email
    form.fields['rut'].initial = perfil.rut
    form.fields['tipousu'].initial = perfil.tipousu
    form.fields['dirusu'].initial = perfil.dirusu
    data["form"] = form
    return render(request, "core/perfil_usuario.html", data)

def obtener_solicitudes_de_servicio(request):
    tipousu = PerfilUsuario.objects.get(user=request.user).tipousu
    data = {'tipousu': tipousu }
    return render(request, "core/obtener_solicitudes_de_servicio.html", data)

# Nuevo
@csrf_exempt
def ingresar_solicitud_servicio(request):
    if request.method == 'POST':
        if not request.user.is_staff:
            data = {
                'tipo': request.POST.get('tipo'),
                'descripcion': request.POST.get('descripcion'),
                'fecha': request.POST.get('fecha'),
                'hora': request.POST.get('hora'),  # ⬅️ Nuevo campo
                'precio': 25000
            }
            request.session['solicitud_data'] = data
            return redirect('iniciar_pago_servicio')  # Redirige solo cuando se guarda bien
        else:
            return render(request, "core/ingresar_solicitud_servicio.html", {
                "mesg": "¡Debe iniciar sesión como cliente!"
            })
    return render(request, "core/ingresar_solicitud_servicio.html")

@csrf_exempt
@login_required
def iniciar_pago_servicio(request):
    data = request.session.get('solicitud_data')

    if not data:
        return render(request, "core/iniciar_pago_servicio.html", {
            "estado": "error",
            "mensaje": "No hay datos de solicitud en sesión."
        })

    estado = request.session.pop('pago_estado', None)

    print("Webpay Plus Transaction.create")
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = request.user.username
    amount = data['precio']
    return_url = request.build_absolute_uri('/retorno_pago_servicio/')

    tx = Transaction(WebpayOptions(
        commerce_code="597055555532",
        api_key="579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
        integration_type="TEST"
    ))
    response = tx.create(buy_order, session_id, amount, return_url)

    perfil = PerfilUsuario.objects.get(user=request.user)

    return render(request, "core/iniciar_pago_servicio.html", {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": return_url,
        "response": response,
        "token_ws": response['token'],
        "url_tbk": response['url'],
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "rut": perfil.rut,
        "dirusu": perfil.dirusu,
        "tipo": data['tipo'],
        "descripcion": data['descripcion'],
        "fecha": data['fecha'],
        "hora": data['hora'],  # ⬅️ Nuevo campo
        "precio": data['precio'],
        "estado": estado['estado'] if estado else None,
        "mensaje": estado['mensaje'] if estado else None
    })

@csrf_exempt
def retorno_pago_servicio(request):
    if request.method == 'GET':
        token = request.GET.get("token_ws")
        print("commit for token_ws: {}".format(token))

        tx = Transaction(WebpayOptions(
            commerce_code="597055555532",
            api_key="579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
            integration_type="TEST"
        ))
        response = tx.commit(token=token)
        print("response: {}".format(response))

        if response['status'] != 'AUTHORIZED':
            request.session['pago_estado'] = {
                'estado': 'error',
                'mensaje': 'Transacción rechazada por Webpay o no autorizada.'
            }
            return redirect('iniciar_pago_servicio')

        user = User.objects.get(username=response['session_id'])
        perfil = PerfilUsuario.objects.get(user=user)

        data = request.session.get('solicitud_data')
        if not data:
            request.session['pago_estado'] = {
                'estado': 'error',
                'mensaje': 'No se encontró la solicitud en sesión.'
            }
            return redirect('iniciar_pago_servicio')

        try:
            with connection.cursor() as cursor:
                monto = int(data['precio'])
                tiposol = data['tipo']
                rutcli = perfil.rut
                idprod = 9 if tiposol == 'Mantención' else 10

                cursor.execute("EXEC SP_CREAR_FACTURA %s, %s, %s, %s, %s", [
                    rutcli,
                    idprod,
                    data['fecha'],
                    f"Servicio: {tiposol}",
                    monto
                ])
                nrofac = cursor.fetchone()[0]

                cursor.execute("SELECT rut FROM PerfilUsuario WHERE tipousu = 'Técnico'")
                tecnicos = cursor.fetchall()
                if not tecnicos:
                    request.session['pago_estado'] = {
                        'estado': 'error',
                        'mensaje': 'No hay técnicos disponibles.'
                    }
                    return redirect('iniciar_pago_servicio')

                ruttec = random.choice(tecnicos)[0]

                cursor.execute("EXEC SP_CREAR_SOLICITUD_SERVICIO %s, %s, %s, %s, %s, %s, %s", [
                    nrofac,
                    tiposol,
                    data['descripcion'],
                    data['fecha'],
                    data['hora'],  # ⬅️ Nuevo parámetro
                    ruttec,
                    idprod
                ])

            request.session['pago_estado'] = {
                'estado': 'exito',
                'mensaje': '¡Su Solicitud de Servicio ha sido generada con éxito!'
            }
            return redirect('iniciar_pago_servicio')

        except Exception as e:
            request.session['pago_estado'] = {
                'estado': 'error',
                'mensaje': f'Ocurrió un error al procesar la solicitud: {str(e)}'
            }
            return redirect('iniciar_pago_servicio')
    else:
        return redirect('home')

@login_required
def facturas_view (request, rut):
    """
    Vista para mostrar facturas según tipo de usuario:
    - Cliente: solo sus facturas (rutcli = su RUT).
    - Administrador: todas las facturas (ignora el RUT).
    """
    try:
        usuario = PerfilUsuario.objects.get(user=request.user)
    except PerfilUsuario.DoesNotExist:
        raise Http404("Perfil de usuario no encontrado.")

    es_admin = usuario.tipousu == "Administrador"

    # Seguridad: un cliente no puede ver facturas de otro cliente
    if not es_admin and rut != usuario.rut:
        raise Http404("No puedes ver facturas de otro usuario.")

    # Ejecutar SP con 2 parámetros: rut y tipousu
    with connection.cursor() as cur:
        cur.execute("EXEC SP_OBTENER_FACTURAS %s, %s", [usuario.rut, usuario.tipousu])
        columns = [col[0] for col in cur.description]
        facturas = [dict(zip(columns, row)) for row in cur.fetchall()]

    # Ejecutar SP para obtener guías de despacho
    with connection.cursor() as cur:
        cur.execute("EXEC SP_OBTENER_GUIAS_DE_DESPACHO")
        columns = [col[0] for col in cur.description]
        guias = {
            (row[columns.index("nrofac")], row[columns.index("idprod")]):
            dict(zip(columns, row))
            for row in cur.fetchall()
        }

    # Asociar guía (si existe) a cada factura
    for f in facturas:
        f["guia"] = guias.get((f["nrofac"], f["idprod"]))

    context = {
        "facturas": facturas,
        "es_admin": es_admin,
    }

    return render(request, "core/facturas.html", context)