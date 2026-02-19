from django import forms
from .models import Pago


class NotificarPagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['monto', 'fecha_pago', 'periodo', 'comprobante']
        widgets = {
            'fecha_pago': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'comprobante': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*,application/pdf'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'periodo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Enero 2026'}),
        }

    def clean_comprobante(self):
        file = self.cleaned_data.get('comprobante')
        if file:
            if not (file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf'))):
                raise forms.ValidationError("Solo se permiten imágenes (.png, .jpg, .jpeg) o PDF.")
        return file