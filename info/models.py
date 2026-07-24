from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from equipos.models import Equipo


class Jornada(models.Model):
    numero = models.PositiveIntegerField(
        unique=True
    )

    class Meta:
        ordering = ["numero"]

    def __str__(self):
        return f"Jornada {self.numero}"


class Partido(models.Model):
    jornada = models.ForeignKey(
        Jornada,
        on_delete=models.CASCADE,
        related_name="partidos"
    )

    equipo_local = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name="partidos_local"
    )

    equipo_visitante = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name="partidos_visitante"
    )

    fecha = models.DateField()

    hora = models.TimeField()

    cancha = models.CharField(
        max_length=100,
        blank=True
    )

    goles_local = models.PositiveIntegerField(
        default=0
    )

    goles_visitante = models.PositiveIntegerField(
        default=0
    )

    terminado = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = [
            "jornada__numero",
            "fecha",
            "hora",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "jornada",
                    "equipo_local",
                    "equipo_visitante",
                ],
                name="partido_unico_por_jornada"
            )
        ]

        verbose_name = "Partido"
        verbose_name_plural = "Partidos"

    def clean(self):
        super().clean()

        if (
            self.equipo_local_id
            and self.equipo_visitante_id
            and self.equipo_local_id == self.equipo_visitante_id
        ):
            raise ValidationError({
                "equipo_visitante": (
                    "El equipo local y el visitante deben ser diferentes."
                )
            })

        if (
            self.jornada_id
            and self.equipo_local_id
            and self.equipo_visitante_id
        ):
            partido_repetido = Partido.objects.exclude(
                pk=self.pk
            ).filter(
                jornada_id=self.jornada_id
            ).filter(
                Q(
                    equipo_local_id=self.equipo_local_id,
                    equipo_visitante_id=self.equipo_visitante_id,
                )
                |
                Q(
                    equipo_local_id=self.equipo_visitante_id,
                    equipo_visitante_id=self.equipo_local_id,
                )
            ).exists()

            if partido_repetido:
                raise ValidationError(
                    "Estos equipos ya tienen un partido registrado "
                    "en esta jornada."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.equipo_local} "
            f"{self.goles_local} - {self.goles_visitante} "
            f"{self.equipo_visitante}"
        )