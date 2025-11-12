from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from apps.user.models import *
from apps.sugo.models import *

@login_required
def home(request):
    user = request.user
    plataformas = [
        {"nombre": "sugo", "imagen": "img/sugo-logo.png", "url": "dashboard_sugo"},
        {"nombre": "meyo", "imagen": "img/meyo-logo.png", "url": "home"},
        {"nombre": "salsa", "imagen": "img/salsa-logo.png", "url": "home"},
    ]
    data = []

    for p in plataformas:
        estado = "no asociada"
        if p == "sugo":
            # Buscamos si existe un registro para este usuario y plataforma
            existe = Streamer.objects.filter(user=user).exists()
            if existe:
                estado = "asociada"

        data.append({
            "nombre": p["nombre"],
            "estado": estado,
            "imagen": p["imagen"],
            "url": p["url"],
        })
    
    return render(request, "index.html", {"plataformas": data})
