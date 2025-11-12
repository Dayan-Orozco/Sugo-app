from django import forms
from .models import User

class LoginForm(forms.Form):
    country = forms.ChoiceField(
        choices=User.COUNTRY_CHOICES,
        label="🌍 País",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    document = forms.IntegerField(
        label="🪪 Documento / Identificación",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "document", "country", "telegram_number"]  # is_active eliminado
        labels = {
            "first_name": "👤 Nombre",
            "last_name": "👥 Apellidos",
            "email": "📧 Dirección de correo electrónico",
            "document": "🪪 Documento / Identificación",
            "country": "🌍 País",
            "telegram_number": "📱 Telegram",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "document": forms.NumberInput(attrs={"class": "form-control"}),
            "country": forms.Select(attrs={"class": "form-control"}),
            "telegram_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "57XXXXXXXXXX o @thecrazyagency"}),
        }