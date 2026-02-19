from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2', 'rol', 'telefono', 'documento')
        widgets = {
            'rol': forms.Select(choices=Usuario.ROLES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = "Mínimo 8 caracteres."
        self.fields['password2'].help_text = "Repite la contraseña."