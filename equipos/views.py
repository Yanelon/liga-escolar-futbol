from django.shortcuts import get_object_or_404, render
from .models import Equipo


def lista_equipos(request):

    equipos = Equipo.objects.all().order_by("nombre")

    return render(
        request,
        "equipos/lista_equipos.html",
        {
            "equipos": equipos
        }
    )


def detalle_equipo(request, equipo_id):

    equipo = get_object_or_404(
        Equipo.objects.prefetch_related("jugadores"),
        id=equipo_id
    )

    jugadores = equipo.jugadores.all().order_by(
        "numero",
        "nombre"
    )

    return render(
        request,
        "equipos/detalle_equipo.html",
        {
            "equipo": equipo,
            "jugadores": jugadores,
        }
    )
