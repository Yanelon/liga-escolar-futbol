from django.shortcuts import render

from .utils import (
    calcular_tabla,
    calcular_goleadores,
    calcular_tarjetas,
)


def inicio_estadisticas(request):
    return render(
        request,
        "estadisticas/inicio_estadisticas.html"
    )


def tabla_general(request):

    tabla = calcular_tabla()

    contexto = {
        "tabla": tabla
    }

    return render(
        request,
        "estadisticas/tabla_general.html",
        contexto
    )


def tabla_goleadores(request):

    goleadores = calcular_goleadores()

    contexto = {
        "goleadores": goleadores
    }

    return render(
        request,
        "estadisticas/tabla_goleadores.html",
        contexto
    )


def tabla_disciplinaria(request):

    tarjetas = calcular_tarjetas()

    contexto = {
        "tarjetas": tarjetas
    }

    return render(
        request,
        "estadisticas/tabla_disciplinaria.html",
        contexto
    )