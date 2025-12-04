from django import forms
from .models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator

class LoginForm(forms.Form):
    country = forms.ChoiceField(
        choices=User.COUNTRY_CHOICES,
        label="🌍 País",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        label="📱 Nro de Teléfono",
        max_length=10,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        validators=[
            MinLengthValidator(7, "El teléfono debe tener mínimo 7 dígitos"),
            MaxLengthValidator(10, "El teléfono debe tener máximo 10 dígitos"),
        ]
    )
    password  = forms.CharField(
        label="🔑 Pin",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            "maxlength": "4",
            "minlength": "4", 
            "pattern": "[0-9]{4}", 
            "inputmode": "numeric",
        }),
        validators=[
            MinLengthValidator(4, "El PIN debe tener mínimo 4 dígitos"),
            MaxLengthValidator(4, "El PIN debe tener máximo 4 dígitos"),
        ]
    )

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "document", "country", "phone", "password", "telegram_number"]  # is_active eliminado
        labels = {
            "first_name": "👤 Nombre",
            "last_name": "👥 Apellidos",
            "document": "🪪 Documento / Identificación",
            "country": "🌍 País",
            "phone": "📱 Nro de Teléfono",
            "password": "🔑 Pin",
            "telegram_number": "📱 Telegram",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "document": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Este documento solo se usará para verificaciones de la cuenta",
                    "pattern": "[0-9]+",        # solo números
                    "inputmode": "numeric",     # teclado numérico en móviles
                }
            ),
            "country": forms.Select(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={
                "class": "form-control", 
                "placeholder": "XXXxxxxXXX Con este iniciaras Sesión"
            }),      
            "password": forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Tu PIN será tu clave",
                "maxlength": "4",
                "minlength": "4",
                "pattern": "[0-9]{4}",
                "inputmode": "numeric",
            }),
            "telegram_number": forms.TextInput(attrs={
                "class": "form-control", 
                "placeholder": "XXXxxxxXXX o @thecrazyagency"
            }),
        }