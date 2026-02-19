from django import forms
from .models import Usuario
from django.contrib.auth.hashers import make_password


class CrearUsuarioForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput
    )

    class Meta:
        model = Usuario
        fields = ["username", "first_name", "last_name", "email",
                  "documento", "telefono", "rol", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        user.is_staff = False  # no entra al admin real
        user.is_superuser = False
        if commit:
            user.save()
        return user
