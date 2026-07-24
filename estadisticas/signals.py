from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from info.models import Partido

from .models import Gol


def actualizar_marcador(partido):
    goles_local = partido.goles.filter(
        jugador__equipo_id=partido.equipo_local_id
    ).count()

    goles_visitante = partido.goles.filter(
        jugador__equipo_id=partido.equipo_visitante_id
    ).count()

    Partido.objects.filter(
        pk=partido.pk
    ).update(
        goles_local=goles_local,
        goles_visitante=goles_visitante,
    )


@receiver(post_save, sender=Gol)
def actualizar_marcador_al_guardar(sender, instance, **kwargs):
    actualizar_marcador(instance.partido)


@receiver(post_delete, sender=Gol)
def actualizar_marcador_al_eliminar(sender, instance, **kwargs):
    actualizar_marcador(instance.partido)