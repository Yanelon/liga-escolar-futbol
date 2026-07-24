from django.shortcuts import render

from equipos.models import Equipo
from jugadores.models import Jugador
from info.models import Jornada, Partido


def inicio(request):

    proximo_partido = (
        Partido.objects
        .filter(terminado=False)
        .order_by("fecha", "hora")
        .first()
    )

    contexto = {
        "total_equipos": Equipo.objects.count(),
        "total_jugadores": Jugador.objects.count(),
        "total_jornadas": Jornada.objects.count(),
        "total_partidos": Partido.objects.count(),
        "proximo_partido": proximo_partido,
    }

    return render(
        request,
        "home/home.html",
        contexto
    )