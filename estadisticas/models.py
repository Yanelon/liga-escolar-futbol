from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from info.models import Partido
from jugadores.models import Jugador


class Gol(models.Model):

    partido = models.ForeignKey(
        Partido,
        on_delete=models.CASCADE,
        related_name="goles"
    )

    jugador = models.ForeignKey(
        Jugador,
        on_delete=models.CASCADE,
        related_name="goles"
    )

    minuto = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(130),
        ]
    )

    class Meta:
        ordering = [
            "partido",
            "minuto",
        ]

        verbose_name = "Gol"
        verbose_name_plural = "Goles"

    def clean(self):
        super().clean()

        if not self.partido_id or not self.jugador_id:
            return

        equipos_del_partido = {
            self.partido.equipo_local_id,
            self.partido.equipo_visitante_id,
        }

        if self.jugador.equipo_id not in equipos_del_partido:
            raise ValidationError({
                "jugador": (
                    "El jugador seleccionado no pertenece a ninguno "
                    "de los equipos que participan en este partido."
                )
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.jugador} - "
            f"{self.partido} - "
            f"Minuto {self.minuto or 'sin registrar'}"
        )


class Tarjeta(models.Model):

    TIPOS = [
        ("AMARILLA", "Amarilla"),
        ("ROJA", "Roja"),
    ]

    partido = models.ForeignKey(
        Partido,
        on_delete=models.CASCADE,
        related_name="tarjetas"
    )

    jugador = models.ForeignKey(
        Jugador,
        on_delete=models.CASCADE,
        related_name="tarjetas"
    )

    tipo = models.CharField(
        max_length=10,
        choices=TIPOS
    )

    def clean(self):
        super().clean()

        if not self.partido_id or not self.jugador_id:
            return

        equipos_del_partido = {
            self.partido.equipo_local_id,
            self.partido.equipo_visitante_id,
        }

        if self.jugador.equipo_id not in equipos_del_partido:
            raise ValidationError({
                "jugador": (
                    "El jugador seleccionado no pertenece a ninguno "
                    "de los equipos que participan en este partido."
                )
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.jugador} - {self.get_tipo_display()}"