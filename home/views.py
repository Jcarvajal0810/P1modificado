from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Prenda
from home.services.interfaces import CarritoServiceInterface
from home.services.carrito_service import CarritoService

# Inyección de dependencia para el servicio de carrito
carrito_service: CarritoServiceInterface = CarritoService()

def home(request):
    # Obtenemos los valores de los filtros
    searchPrenda = request.GET.get("searchPrenda")
    precio = request.GET.get("precio")
    estado = request.GET.get("estado")
    talla = request.GET.get("talla")
    
    # Usamos el método por_filtros del manager
    filtros = {
        'nombre': searchPrenda,
        'talla': talla,
        'estado': estado,
    }
    
    if precio:
        try:
            filtros['precio_max'] = int(precio)
        except ValueError:
            # Si el precio no es un número válido, no aplicamos ese filtro
            pass
    
    # Aplicamos los filtros usando el manager
    prendas = Prenda.objects.por_filtros(**filtros)
    
    # Obtener el carrito del usuario usando el servicio
    prendas_en_carrito = []
    total = 0
    if request.user.is_authenticated:
        prendas_en_carrito = carrito_service.get_prendas(request.user)
        total = carrito_service.get_total(request.user)
    
    return render(request, 'home.html', {
        'searchPrenda': searchPrenda,
        'prendas': prendas,
        'precio': precio,
        'prendas_en_carrito': prendas_en_carrito,
        'total': total
    })

def registro(request):
    return render(request, 'registro.html')

def process_registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, 'registro.html', {'username': username, 'first_name': first_name, 'last_name': last_name, 'email': email})
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Nombre de usuario ya existe")
            return render(request, 'registro.html', {'username': username, 'first_name': first_name, 'last_name': last_name, 'email': email})
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo ya está registrado")
            return render(request, 'registro.html', {'username': username, 'first_name': first_name, 'last_name': last_name, 'email': email})

        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        user.save()
        login(request, user)
        messages.success(request, "Registro exitoso")
        return redirect('home')
    else:
        return redirect('registro')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Inicio de sesión exitoso")
                return redirect('home')
            else:
                messages.error(request, "El usuario o la contraseña no son válidos")
        else:
            messages.error(request, "El usuario o la contraseña no son válidos")
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "Sesión cerrada exitosamente")
    return redirect('home')

def agregar_al_carrito(request, prenda_id):
    if request.user.is_authenticated:
        mensaje = carrito_service.add_prenda(request.user, prenda_id)
        messages.success(request, mensaje)
    else:
        messages.error(request, "Debes iniciar sesión para agregar prendas al carrito.")
    return redirect('home')

def ver_carrito(request):
    if request.user.is_authenticated:
        prendas_en_carrito = carrito_service.get_prendas(request.user)
        total = carrito_service.get_total(request.user)
        return render(request, 'carrito.html', {'prendas_en_carrito': prendas_en_carrito, 'total': total})
    else:
        messages.error(request, "Debes iniciar sesión para ver tu carrito.")
        return redirect('home')
    
def limpiar_carrito(request):
    if request.user.is_authenticated:
        carrito_service.clear(request.user)
        messages.success(request, "El carrito se ha limpiado exitosamente.")
    else:
        messages.error(request, "Debes iniciar sesión para limpiar tu carrito.")
    return redirect('home')