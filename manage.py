#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    from apps.user.models import User
    from django.contrib.auth.models import Group
    print("Cargo main")
    print(Group.objects.all())
    print(User.objects.all())
    if not User.objects.all() or not Group.objects.all():
        print("Iniciando el sistema SUGO-APP")
        create_data()

def create_data():
    from apps.user.models import User
    from django.contrib.auth.models import Group
    from rest_framework.authtoken.models import Token   
    
    # Pedir datos por consola
    print("=== Creación de usuario ===")
    country = input("Ingrese el código del país (col, ven, mex, bol, per, arg, ecu, crc): ").strip().lower()
    document = input("Ingrese el número de documento: ").strip()
    username = input("Ingrese su usuario: ").strip()
    email = input("Ingrese su correo: ").strip()
    password = input("Ingrese una contraseña: ").strip()

    print("Creando Grupos")
    # Crear o recuperar el grupo (Administrador o Usuario)
    grupo, creado = Group.objects.get_or_create(name="Jefe")
    Group.objects.get_or_create(name="Admin")
    Group.objects.get_or_create(name="Streamers")
    print("Grupos creados")
    # Crear el usuario
    usuario = User.objects.create_user(username=username, password=password, email=email, is_staff=True, is_superuser=True, country=country, document=document)
    print("Usuario Creado")
    # Asignar grupo al usuario
    usuario.groups.add(grupo)
    print("Grupo asignado")        
    # Crear token de autenticación para el usuario
    token, creado = Token.objects.get_or_create(user=usuario)
    print("Token Creado")
    return {
        "usuario": usuario.username,
        "grupo": grupo.name,
        "token": token.key
    }


if __name__ == '__main__':
    main()
