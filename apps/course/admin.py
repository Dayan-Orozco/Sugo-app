from django.contrib import admin
from .models import *

# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_display = ("name", "created_at", "status", "percentaje", "lessons", "enable", "user")
    search_fields = ("name",)
    ordering = ("name",)
admin.site.register(Course, CourseAdmin)