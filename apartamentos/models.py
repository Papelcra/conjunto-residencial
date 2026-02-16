# apartamentos/models.py

from django.db import models
from django.conf import settings


class Apartamento(models.Model):
    # Estados de ocupación / situación comercial
    ESTADO_VIVIENDA = (
        ('residiendo', 'Residiendo (propietario viviendo)'),
        ('arrendado', 'Arrendado (alquilado)'),
        ('en_venta', 'En venta'),
        ('desocupado', 'Desocupado / Vacío'),
        ('en_obra_mantenimiento', 'En obra o mantenimiento'),
        ('bloqueado', 'Bloqueado / Embargado / Prohibido uso'),
    )

    # Identificador principal del apartamento
    # Ejemplos: 101, 202-A, 1503, PH-05, etc.
    identificador = models.CharField(
        max_length=20,
        unique=True,
        help_text="Número, código o referencia única del apartamento (ej: 101, 1503, PH-02)",
        verbose_name="Identificador / Número de apartamento"
    )

    # Opcional: si aún quieres separar torre o bloque
    bloque_o_torre = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="Torre / Bloque",
        help_text="Ej: A, B, C, Norte, Sur... (opcional)"
    )

    # Área en metros cuadrados (útil para administración, cuotas, etc.)
    area_m2 = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Área (m²)"
    )

    # Estado actual de la vivienda
    estado = models.CharField(
        max_length=30,
        choices=ESTADO_VIVIENDA,
        default='desocupado',
        verbose_name="Estado de la vivienda"
    )

    # Relación con el residente / ocupante principal actual
    # Solo aplica si está residiendo o arrendado
    ocupante_actual = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='apartamentos_ocupados',
        verbose_name="Ocupante / Residente actual",
        limit_choices_to={'rol': 'residente'},  # solo usuarios con rol residente
        help_text="Persona que vive o arrienda actualmente (si aplica)"
    )

    # Datos adicionales útiles
    piso = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name="Piso"
    )

    notas = models.TextField(
        blank=True,
        verbose_name="Notas / Observaciones",
        help_text="Ej: remodelado 2024, tiene mascota, problemas con parqueadero, etc."
    )

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Apartamento"
        verbose_name_plural = "Apartamentos"
        ordering = ['identificador']
        indexes = [
            models.Index(fields=['identificador']),
            models.Index(fields=['estado']),
        ]

    def __str__(self):
        if self.bloque_o_torre:
            return f"{self.identificador} - {self.bloque_o_torre} ({self.get_estado_display()})"
        return f"{self.identificador} ({self.get_estado_display()})"

    def esta_ocupado(self):
        return self.estado in ('residiendo', 'arrendado')

    def tiene_ocupante(self):
        return self.ocupante_actual is not None