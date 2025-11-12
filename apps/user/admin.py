from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from apps.user.models import *  # Asegúrate de importar tu modelo

class CustomUserAdmin(BaseUserAdmin):
    model = User

    # Campos visibles en el listado de usuarios
    list_display = ("username", "email", "is_active", "telegram_number", "country", "get_groups")

    # Campos que puedes buscar
    search_fields = ("username", "email", "telegram_number", )

    # Campos para orden
    ordering = ("username", "country",)
    
    # filtros     
    list_filter = ("country", "groups", "is_active", )

    # Campos adicionales en el formulario de edición
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Información adicional", {
            "fields": ("country", "document", "telegram_number"),
        }),
    )

    # Campos adicionales en el formulario de creación
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Información adicional", {
            "fields": ("country", "document", "telegram_number"),
        }),
    )


    # Para mostrar los grupos del usuario
    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])
    get_groups.short_description = "Grupos"

# Registrar el modelo y usar la configuración personalizada
admin.site.register(User, CustomUserAdmin)
