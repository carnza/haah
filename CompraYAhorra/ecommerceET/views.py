from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from django.http import HttpResponse
from django.conf import settings


def index_view(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            messages.error(request, "Correo electrónico no encontrado.")
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"¡Bienvenido, {user.username}!")
            return redirect('index')  # Redirigir a la página principal
        else:
            messages.error(request, "Contraseña incorrecta.")
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validaciones
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return render(request, 'register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return render(request, 'register.html')

        # Crear usuario
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, '¡Tu cuenta ha sido creada exitosamente!')

    return render(request, 'register.html')

def agregar_al_carrito(request):
    """Agrega un producto al carrito usando la sesión."""
    if request.method == 'POST':
        import json
        datos = json.loads(request.body)
        product_id = datos.get('product_id')
        product_name = datos.get('product_name')
        product_price = float(datos.get('product_price'))
        product_quantity = 1  

        carrito = request.session.get('carrito', {})

        if product_id in carrito:
            carrito[product_id]['quantity'] += product_quantity
            carrito[product_id]['total_price'] = carrito[product_id]['quantity'] * product_price
        else:
            carrito[product_id] = {
                'name': product_name,
                'price': product_price,
                'quantity': product_quantity,
                'total_price': product_price * product_quantity
            }

        # Guardar el carrito actualizado en la sesión
        request.session['carrito'] = carrito

        return JsonResponse({'status': 'success', 'carrito': carrito})

def ver_carrito(request):
    """Muestra el carrito de compras."""
    carrito = request.session.get('carrito', {})
    total = sum(item['total_price'] for item in carrito.values())
    return render(request, 'carrito.html', {'carrito': carrito, 'total': total})

def direccion_envio(request):
    if request.method == 'POST':
        # Extraer datos del formulario
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        ciudad = request.POST.get('ciudad')
        estado = request.POST.get('estado')
        codigo_postal = request.POST.get('codigo_postal')
        telefono = request.POST.get('telefono')

        # Aquí podrías guardar los datos en la base de datos si es necesario

        # Redirigir a la página de pago
        return redirect('procesar_pago')  # Actualizaremos esta URL más adelante

    return render(request, 'direccion_envio.html')


def iniciar_pago(request):
    # Detalles de la compra
    buy_order = "orden123"  # Número único
    session_id = "session123"
    amount = 19990  # Monto total en pesos
    return_url = request.build_absolute_uri("/pago-exitoso/")  # Redirige aquí tras el pago

    try:
        # Crear transacción
        transaction = Transaction()
        response = transaction.create(
            buy_order=buy_order,
            session_id=session_id,
            amount=amount,
            return_url=return_url,
        )

        # Redirigir al formulario de pago de Transbank
        return redirect(response["url"] + "?token_ws=" + response["token"])
    except Exception as e:
        return HttpResponse(f"Error al iniciar la transacción: {str(e)}", status=500)



def pago_exitoso(request):
    token = request.GET.get("token_ws")
    try:
        # Confirmar la transacción con Transbank
        transaction = Transaction()
        response = transaction.commit(token)

        # Renderizar la plantilla de éxito con los detalles de la transacción
        return render(request, "pago_exitoso.html", {"response": response})
    except Exception as e:
        return HttpResponse(f"Error al confirmar la transacción: {str(e)}", status=500)


def pago_fallido(request):
    return render(request, "pago_fallido.html")



def logout_view(request):
    logout(request)
    return redirect('index')

def aliexpress_view(request):
    return render(request, 'aliexpress.html')

