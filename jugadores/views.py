from django.shortcuts import get_object_or_404, render
from .models import Jugador


def detalle_jugador(request, jugador_id):

    jugador = get_object_or_404(
        Jugador.objects.select_related("equipo"),
        id=jugador_id
    )

    goles = jugador.goles.count()

    tarjetas_amarillas = jugador.tarjetas.filter(
        tipo="AMARILLA"
    ).count()

    tarjetas_rojas = jugador.tarjetas.filter(
        tipo="ROJA"
    ).count()

    return render(
        request,
        "jugadores/detalle_jugador.html",
        {
            "jugador": jugador,
            "goles": goles,
            "tarjetas_amarillas": tarjetas_amarillas,
            "tarjetas_rojas": tarjetas_rojas,
        }
    )