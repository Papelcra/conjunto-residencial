from django import forms
from .models import Reserva, ZonaComun


# ==============================
# FORMULARIO DE RESERVA
# ==============================

class ReservaForm(forms.ModelForm):

    class Meta:
        model = Reserva
        fields = ["zona", "fecha", "hora_inicio", "hora_fin"]

        widgets = {
            "zona": forms.Select(attrs={
                "class": "form-select"
            }),
            "fecha": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "hora_inicio": forms.TimeInput(attrs={
                "type": "time",
                "class": "form-control"
            }),
            "hora_fin": forms.TimeInput(attrs={
                "type": "time",
                "class": "form-control"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Mostrar solo zonas activas
        self.fields["zona"].queryset = ZonaComun.objects.filter(activa=True)

    def clean(self):
        cleaned_data = super().clean()

        zona = cleaned_data.get("zona")
        fecha = cleaned_data.get("fecha")
        hora_inicio = cleaned_data.get("hora_inicio")
        hora_fin = cleaned_data.get("hora_fin")

        # Solo validar si todos los campos existen
        if zona and fecha and hora_inicio and hora_fin:
            reserva = Reserva(
                zona=zona,
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin
            )

            try:
                reserva.clean()
            except forms.ValidationError as e:
                self.add_error(None, e)

        return cleaned_data


# ==============================
# FORMULARIO DE ZONA COMÚN
# ==============================

class ZonaComunForm(forms.ModelForm):

    class Meta:
        model = ZonaComun
        fields = ["nombre", "descripcion", "activa"]

        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: Salón Social"
            }),
            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Descripción opcional"
            }),
            "activa": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }