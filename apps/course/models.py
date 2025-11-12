from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.user.models import *

# Create your models here.
class Course(models.Model):
    STATUS_CHOICES = [
        ('complete', 'Completado'),
        ('inprocess', 'En Proceso'),
        ('notapproved', 'No aprovado'),
        ('notstarted', 'No inciado'),
    ]
    name = models.CharField("Nombre", max_length=150)
    photo = models.ImageField("Foto", upload_to='course/',)
    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True)
    status = models.CharField("Estado", max_length=50, choices=STATUS_CHOICES, default='notstarted')
    percentaje = models.IntegerField("Avance de Curso", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])   
    lessons = models.IntegerField("Lecciones", default=0)     
    enable = models.BooleanField("Habilitado/Inhabilitado", default=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Creado por", blank=True)

    def __str__(self):
        return f"{self.name} ({self.id})"

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ["-created_at"]

class Lesson(models.Model):
    STATUS_CHOICES = [
        ('complete', 'Completado'),
        ('inprocess', 'En Proceso'),
        ('notapproved', 'No aprobado'),
        ('notstarted', 'No iniciado'),
    ]
    course = models.ForeignKey(
        "Course", on_delete=models.CASCADE, related_name='lesson_set', verbose_name="Curso"
    )
    title = models.CharField("Título de la lección", max_length=150)
    content = models.TextField("Contenido", blank=True)
    video_url = models.URLField("Video", blank=True)
    order = models.PositiveIntegerField("Orden en el curso", default=1)
    status = models.CharField("Estado", max_length=50, choices=STATUS_CHOICES, default='notstarted')
    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.course.name}"

    class Meta:
        verbose_name = "Lección"
        verbose_name_plural = "Lecciones"
        ordering = ["order"]
