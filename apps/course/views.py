from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import CourseForm
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

# def home(request):
#     return render(request, 'index.html')

################################################################ CURSOS ################################################################

def list_course(request):  # Listar Cursos
    if request.user.groups.exists() and request.user.groups.first().name == "Streamer":
        return redirect('home')

    query = request.GET.get('q', '')
    start_date_param = request.GET.get('start_date')
    end_date_param = request.GET.get('end_date')
    order_by = request.GET.get('order_by', 'created_at')  # campo por defecto
    direction = request.GET.get('direction', 'desc')  # 'asc' o 'desc'

    # Ordenar
    order = order_by if direction == 'asc' else f'-{order_by}'
    courses = Course.objects.filter(enable=True).order_by(order)

    # Filtro por nombre
    if query:
        courses = courses.filter(Q(name__icontains=query))

    # Filtro por fecha de creación
    if start_date_param:
        if not end_date_param:
            end_date_param = now().date().isoformat()
        courses = courses.filter(
            created_at__date__gte=parse_date(start_date_param),
            created_at__date__lte=parse_date(end_date_param)
        )

    # Columnas para mostrar en la tabla
    columns = [
        ('id', 'ID'),
        ('name', 'Nombre'),
        ('status', 'Estado'),
        ('percentaje', 'Avance'),
        ('lessons', 'Lecciones'),
        ('created_at', 'Fecha de creación'),
        ('enable', '¿Habilitado?'),
        ('user', 'Creado por'),
    ]

    paginator = Paginator(courses, 50)
    pending = courses.filter(percentaje=0)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    total = courses.count() - pending.count()

    return render(request, 'course/course-list.html', {
        'page_obj': page_obj,
        'query': query,
        'order_by': order_by,
        'direction': direction,
        'total': total,
        'pending': pending.count(),
        'columns': columns,
    })
