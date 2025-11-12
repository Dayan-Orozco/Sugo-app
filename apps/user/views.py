from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout as auth_logout
from rest_framework.authtoken.models import Token
from .forms import *
from django.contrib.auth import login as auth_login, authenticate
from .models import *
from django.db.models import Q, Sum
from django.core.paginator import Paginator
import openpyxl
import csv
from io import TextIOWrapper
from django.contrib import messages
from django.utils.dateparse import parse_datetime, parse_date
import pytz
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.utils.http import urlencode

def home(request):
    print("request", request)
    return HttpResponse("<h1>Hola mundo</h1>")

def logout(request):
    auth_logout(request)  # Cierra la sesión
    return redirect('login')  # Redirige al login

def login(request):
    token_value = None
    next_url = request.GET.get('next', 'home')  # Por defecto ir a 'home'
    # Si ya está logueado, enviarlo directamente
    if request.user.is_authenticated:
        return redirect(next_url)
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            country = form.cleaned_data['country']
            document = form.cleaned_data['document']

            user = authenticate(request, country=country, document=document)
            if user:
                if not user.is_active:
                    messages.warning(request, "Espera la activación de tu usuario por el Jefe")
                else:
                    auth_login(request, user)  # Mantener sesión
                    token, created = Token.objects.get_or_create(user=user)
                    token_value = token.key
                    return redirect(next_url)  # Enviar a donde pedía ?next= o home
            else:
                messages.error(request, "Datos incorrectos")
    else:
        form = LoginForm()

    return render(request, 'user/login.html', {'form': form, 'token': token_value})

def register(request):    
    next_url = request.GET.get('next', 'home')  # Por defecto ir a 'home'
    # Si ya está logueado, enviarlo directamente
    if request.user.is_authenticated:
        return redirect(next_url)
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():           
            document = form.cleaned_data.get("document")
            email = form.cleaned_data.get("email")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            country = form.cleaned_data.get("country")
            # Validaciones de campos obligatorios
            if not first_name:
                form.add_error("first_name", "Queremos saber tu nombre para darte la bienvenida 😊")
            if not last_name:
                form.add_error("last_name", "Por favor ingresa tus apellidos para continuar.")
            if not document:
                form.add_error("document", "Por favor ingresa tu documento para continuar.")
            if not country:
                form.add_error("country", "Selecciona tu país para asociarte correctamente.")
            # Validación: documento ya registrado
            if User.objects.filter(document=document).exists():
                messages.error(request, "Este documento ya está registrado. Si ya tienes cuenta, inicia sesión.")
            # Validación: correo ya registrado
            elif email and User.objects.filter(email=email).exists():
                messages.error(request, "Este correo ya está registrado. Intenta recuperar tu acceso o usa otro.")
            else:
                user = form.save(commit=False)
                # Generar username automáticamente
                base_username = f"{user.first_name.strip().lower()}.{user.last_name.strip().lower()}"
                username = base_username
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                user.username = username

                user.is_active = False  # No activo hasta que admin lo habilite
                user.save()
                messages.success(request, "🎉 Tu cuenta fue creada exitosamente. Espera aprobación para iniciar sesión.")
                return redirect("login")  # O página de éxito
    else:
        form = UserRegisterForm()

    return render(request, "user/register.html", {"form": form})

# listar Usuarias
def list_user(request):
    # Redirigir si el usuario pertenece al grupo "Streamer"
    if request.user.groups.exists() and request.user.groups.all()[0].name == "Streamer":
        return redirect('home') 
    # Parámetros de búsqueda y orden
    query = request.GET.get('q', '')
    start_date_param = request.GET.get('start_date')
    end_date_param = request.GET.get('end_date')
    order_by = request.GET.get('order_by', 'date_joined')  # campo por defecto
    direction = request.GET.get('direction', 'desc')  # 'asc' o 'desc'
    # Definir orden
    order = order_by if direction == 'asc' else f'-{order_by}'


    users = User.objects.filter().order_by(order)
    
    if query:
        users = users.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query) |
            Q(document__icontains=query) |
            Q(id__icontains=query)
        )

    if start_date_param:
        # Si no viene fecha final, poner la de hoy
        if not end_date_param:
            end_date_param = now().date().isoformat()  # pasamos a string

        users = users.filter(
            created__date__gte=parse_date(start_date_param),
            date_joined__date__lte=parse_date(end_date_param)
        )
    # Columnas para mostrar en la tabla
    columns = [
        ('id', 'ID'),
        ('username', 'Usuario'),
        ('document', 'Documento'),
        ('first_name', 'Nombre'),
        ('telegram_number', 'Telegram'),
        ('email', 'E-mail'),
        ('status', 'Estado'),
        ('country', 'Pais'),
        ('date_joined', 'Fecha de Registro'),
    ]
    # Paginación
    print(users)
    for u in users:
        print(u.email, u.telegram_number)

    paginator = Paginator(users, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Cálculo de pendientes
    pending = users.filter(date_joined__isnull=True)
    total = users.count() - pending.count()

    return render(request, 'user/list.html', {
        'page_obj': page_obj,
        'query': query,
        'order_by': order_by,
        'direction': direction,
        'total': total,
        'pending': pending.count(),
        'columns': columns,
    })

# VISTA PARA ACTIVAR UN USUARIO
def activate_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_active = True
    user.save()
    messages.success(request, "Usuario activado correctamente.")
    return redirect('user_list') 

# Editar Usuarias
def edit_user(request, username):# Editar Usuarias
    user = get_object_or_404(User, username=username)
    print("User", user)
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, instance=user)
        if form.is_valid():        
            document = form.cleaned_data.get("document")
            email = form.cleaned_data.get("email")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            country = form.cleaned_data.get("country")
            # Validaciones de campos obligatorios
            if not first_name:
                form.add_error("first_name", "Queremos saber tu nombre para darte la bienvenida 😊")
            if not last_name:
                form.add_error("last_name", "Por favor ingresa tus apellidos para continuar.")
            if not document:
                form.add_error("document", "Por favor ingresa tu documento para continuar.")
            if not country:
                form.add_error("country", "Selecciona tu país para asociarte correctamente.")
           
            user = form.save(commit=False)
            # Generar username automáticamente
            raw_username = f"{user.first_name.strip().lower()}.{user.last_name.strip().lower()}"
            base_username = raw_username.replace(" ", ".")
            username = base_username
            if user.username == username:      
                print("No guarda username ya estaba igual")              
            else:
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                user.username = username
                print("Guardando username")
                user.save()           

            messages.success(request, "Usuarioa/o Modificado con Exito.")
            form.save()
            return redirect('user_list')
    else:
        form = UserRegisterForm(instance=user)
    return render(request, 'user/edit.html', {'form': form})
