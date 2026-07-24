from equipos.models import Equipo
from info.models import Partido
from estadisticas.models import Gol
from django.db.models import Count, Q
from .models import Tarjeta



def calcular_tabla():

    equipos = Equipo.objects.all()

    partidos_terminados = Partido.objects.filter(
        terminado=True
    )

    tabla = []

    for equipo in equipos:

        datos = {
            "equipo": equipo,
            "pj": 0,
            "pg": 0,
            "pe": 0,
            "pp": 0,
            "gf": 0,
            "gc": 0,
            "dg": 0,
            "puntos": 0,
        }

        for partido in partidos_terminados:

            if partido.equipo_local == equipo:

                datos["pj"] += 1
                datos["gf"] += partido.goles_local
                datos["gc"] += partido.goles_visitante

                if partido.goles_local > partido.goles_visitante:
                    datos["pg"] += 1
                    datos["puntos"] += 3

                elif partido.goles_local == partido.goles_visitante:
                    datos["pe"] += 1
                    datos["puntos"] += 1

                else:
                    datos["pp"] += 1


            elif partido.equipo_visitante == equipo:

                datos["pj"] += 1
                datos["gf"] += partido.goles_visitante
                datos["gc"] += partido.goles_local

                if partido.goles_visitante > partido.goles_local:
                    datos["pg"] += 1
                    datos["puntos"] += 3

                elif partido.goles_visitante == partido.goles_local:
                    datos["pe"] += 1
                    datos["puntos"] += 1

                else:
                    datos["pp"] += 1

        datos["dg"] = datos["gf"] - datos["gc"]

        tabla.append(datos)

    tabla.sort(
        key=lambda equipo: (
            equipo["puntos"],
            equipo["dg"],
            equipo["gf"]
        ),
        reverse=True
    )

    return tabla

def calcular_goleadores():

    goleadores = (
        Gol.objects
        .values(
            "jugador",
            "jugador__nombre",
            "jugador__equipo__nombre",
        )
        .annotate(total_goles=Count("id"))
        .order_by("-total_goles", "jugador__nombre")
    )

    return goleadores


def calcular_tarjetas():

    tarjetas = (
        Tarjeta.objects
        .values(
            "jugador",
            "jugador__nombre",
            "jugador__equipo__nombre",
        )
        .annotate(
            amarillas=Count(
                "id",
                filter=Q(tipo="AMARILLA")
            ),
            rojas=Count(
                "id",
                filter=Q(tipo="ROJA")
            ),
        )
        .order_by(
            "-rojas",
            "-amarillas",
            "jugador__nombre"
        )
    )

    return tarjetas