from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from equipos.models import Equipo


class Jugador(models.Model):
    nombre = models.CharField(
        max_length=100
    )

    apellidos = models.CharField(
        max_length=150
    )

    numero = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(99),
        ]
    )

    posicion = models.CharField(
        max_length=50,
        blank=True
    )

    edad = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(5),
            MaxValueValidator(100),
        ]
    )

    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name="jugadores"
    )

    foto = models.ImageField(
        upload_to="jugadores/",
        blank=True,
        null=True
    )

    class Meta:
        ordering = [
            "equipo__nombre",
            "numero",
            "apellidos",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["equipo", "numero"],
                name="numero_unico_por_equipo"
            )
        ]

    def clean(self):
        super().clean()

        if self.nombre:
            self.nombre = self.nombre.strip().title()

        if self.apellidos:
            self.apellidos = self.apellidos.strip().title()

        if self.posicion:
            self.posicion = self.posicion.strip().title()

        if self.equipo_id and self.numero:
            jugador_repetido = Jugador.objects.exclude(
                pk=self.pk
            ).filter(
                equipo_id=self.equipo_id,
                numero=self.numero
            ).exists()

            if jugador_repetido:
                raise ValidationError({
                    "numero": (
                        f"El número {self.numero} ya está ocupado "
                        f"en el equipo {self.equipo}."
                    )
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"#{self.numero} "
            f"{self.nombre} {self.apellidos} "
            f"({self.equipo})"
        )