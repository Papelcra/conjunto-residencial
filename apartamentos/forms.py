from django import forms
from .models import Apartamento


class ApartamentoForm(forms.ModelForm):
    class Meta:
        model = Apartamento
        fields = [
            'identificador',
            'bloque_o_torre',
            'piso',
            'area_m2',
            'estado',
            'ocupante_actual',
            'notas',
        ]
        widgets = {
            'notas': forms.Textarea(attrs={'rows': 3}),
            'ocupante_actual': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añadimos clases bootstrap a todos los campos
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})