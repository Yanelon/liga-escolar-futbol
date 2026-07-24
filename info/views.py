from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from .models import Jornada, Partido
from estadisticas.models import Gol, Tarjeta


def jornadas(request):
    jornadas = (
        Jornada.objects
        .prefetch_related(
            "partidos__equipo_local",
            "partidos__equipo_visitante",
        )
        .order_by("numero")
    )

    return render(
        request,
        "torneo/jornadas.html",
        {
            "jornadas": jornadas,
        }
    )

def detalle_partido(request, partido_id):

    partido = get_object_or_404(
        Partido,
        id=partido_id
    )

    goles = (
        Gol.objects
        .filter(partido=partido)
        .select_related("jugador")
        .order_by("minuto", "id")
    )

    tarjetas = (
        Tarjeta.objects
        .filter(partido=partido)
        .select_related("jugador")
        .order_by("id")
    )

    contexto = {
        "partido": partido,
        "goles": goles,
        "tarjetas": tarjetas,
    }

    return render(
        request,
        "torneo/detalle_partido.html",
        contexto
    )